from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Webhook listener
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Attempt to get the request data as JSON
        data = request.get_json()

        # If data is None, it means the payload is not in JSON format
        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Print the raw data for debugging purposes
        print(f"Received webhook data: {data}")

        # Check if the render was successful and contains the output URL
        if 'output' in data and 'url' in data['output']:
            rendered_video_url = data['output']['url']
            print(f"Rendered video URL: {rendered_video_url}")
            return jsonify({"message": "Webhook received successfully", "video_url": rendered_video_url}), 200
        else:
            print(f"Render failed or output not yet available: {data}")
            return jsonify({"message": "Render failed or no output available"}), 400

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Server error"}), 500

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Webhook listener
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Attempt to get the request data as JSON
        data = request.get_json()

        # If data is None, it means the payload is not in JSON format
        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Print the raw data for debugging purposes
        print(f"Received webhook data: {data}")

        # Check if the render was successful and contains the output URL
        if 'output' in data and 'url' in data['output']:
            rendered_video_url = data['output']['url']
            print(f"Rendered video URL: {rendered_video_url}")
            return jsonify({"message": "Webhook received successfully", "video_url": rendered_video_url}), 200
        else:
            print(f"Render failed or output not yet available: {data}")
            return jsonify({"message": "Render failed or no output available"}), 400

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Server error"}), 500

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Webhook listener
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Attempt to get the request data as JSON
        data = request.get_json()

        # If data is None, it means the payload is not in JSON format
        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Print the raw data for debugging purposes
        print(f"Received webhook data: {data}")

        # Check if the render was successful and contains the output URL
        if 'output' in data and 'url' in data['output']:
            rendered_video_url = data['output']['url']
            print(f"Rendered video URL: {rendered_video_url}")
            return jsonify({"message": "Webhook received successfully", "video_url": rendered_video_url}), 200
        else:
            print(f"Render failed or output not yet available: {data}")
            return jsonify({"message": "Render failed or no output available"}), 400

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)

