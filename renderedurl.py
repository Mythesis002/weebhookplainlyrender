from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Webhook listener
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log raw request data to check if it's JSON
        raw_data = request.data
        print(f"Raw webhook data: {raw_data}")

        # Check if Content-Type is 'application/json'
        content_type = request.headers.get('Content-Type')
        print(f"Content-Type: {content_type}")

        # Attempt to get the request data as JSON
        data = request.get_json()

        if data is None:
            print("Invalid JSON payload")
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Print the received data for debugging purposes
        print(f"Received webhook data (JSON): {data}")

        # Check if the render was successful and contains the output URL
        if 'output' in data and data['output']:  # Checking if 'output' is present and not empty
            rendered_video_url = data['output']  # Directly get the 'output' as it is a string URL
            print(f"Rendered video URL: {rendered_video_url}")
            return jsonify({
                "message": "Webhook received successfully",
                "video_url": rendered_video_url
            }), 200
        else:
            print(f"Render failed or output not yet available: {data}")
            return jsonify({
                "message": "Render failed or no output available",
                "data_received": data  # Include the received data in the response for easier debugging
            }), 400

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
