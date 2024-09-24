from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
from flask_cors import CORS
import threading
import time
import os

app = Flask(__name__)

# Enable CORS and configure it to handle all routes
CORS(app)

# API endpoint and credentials for Plainly API
PLAINLY_API_URL = "https://api.plainlyvideos.com/api/v2/renders"
API_USERNAME = "0CG5AqfItJaK8mQTDtCQLCOo1iPny0B8"  # Replace with your actual username
API_PASSWORD = ""  # Replace with your actual password

# Webhook URL of this server
WEBHOOK_URL = "https://weebhookplainlyrender.onrender.com/webhook"  # Update with your server URL

# Dictionary to keep track of render statuses and results
render_results = {}

# Lock for thread-safe access to render_results
results_lock = threading.Lock()

def wait_for_render_completion(render_id):
    """Wait for render completion and update the result in the render_results dictionary."""
    wait_time = 0
    while wait_time < 120:  # Wait up to 120 seconds (2 minutes) for the render to complete
        with results_lock:
            if render_id in render_results and render_results[render_id].get('status') == 'completed':
                return render_results[render_id]['video_url']
            elif render_id in render_results and render_results[render_id].get('status') == 'failed':
                return None
        time.sleep(5)  # Wait for 5 seconds before checking again
        wait_time += 5
    return None

@app.route('/submit_render', methods=['POST'])
def submit_render():
    """Handles incoming render requests from the frontend."""
    data = request.json
    template_id = data.get('templateId')
    render_id = data.get('renderId')
    parameters = data.get('parameters')

    # Check if required fields are provided
    if not template_id or not render_id or not parameters:
        return jsonify({"error": "Missing templateId, renderId, or parameters"}), 400

    # Payload for Plainly API request
    payload = {
        "projectId": render_id,
        "templateId": template_id,
        "parameters": parameters,
        "webhook": {
            "url": WEBHOOK_URL,  # Webhook URL to receive render status updates
            "onFailure": True,
            "onInvalid": True
        }
    }

    # Headers for the API request
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request to Plainly API
        response = requests.post(
            PLAINLY_API_URL,
            json=payload,
            headers=headers,
            auth=HTTPBasicAuth(API_USERNAME, API_PASSWORD)
        )

        # Check if the request was successful
        if response.status_code in [200, 201]:
            with results_lock:
                render_results[render_id] = {'status': 'pending', 'video_url': None}

            # Start a thread to wait for the render completion
            rendered_video_url = wait_for_render_completion(render_id)

            if rendered_video_url:
                return jsonify({"message": "Render request successfully completed", "video_url": rendered_video_url}), 200
            else:
                return jsonify({"error": "Render failed or timed out"}), 500

        else:
            # Log additional error information
            return jsonify({"error": f"Failed with status code {response.status_code}", "details": response.text}), 500
    except requests.exceptions.RequestException as e:
        # Log the exact exception message
        print(f"RequestException: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint to receive render status updates from Plainly API."""
    try:
        # Attempt to get the request data as JSON
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        render_id = data.get('projectId')
        video_url = data.get('output')

        # Update render results based on webhook response
        with results_lock:
            if render_id in render_results:
                if video_url:
                    render_results[render_id] = {'status': 'completed', 'video_url': video_url}
                else:
                    render_results[render_id] = {'status': 'failed', 'video_url': None}

        return jsonify({"message": "Webhook received successfully"}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
