from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Webhook listener
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log raw request data to check the received payload
        raw_data = request.data
        print(f"Raw webhook data: {raw_data}")

        # Log the Content-Type to confirm it's JSON
        content_type = request.headers.get('Content-Type')
        print(f"Content-Type: {content_type}")

        # Attempt to parse the request data as JSON
        data = request.get_json()

        if data is None:
            print("Invalid JSON payload received.")
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Log the JSON data to understand its structure
        print(f"Received webhook data (JSON): {data}")

        # Attempt to extract the status and render URL fields
        render_status = data.get('status')
        render_url = data.get('renderUrl') or data.get('output')

        # Log the render status and URL
        print(f"Render Status: {render_status}")
        print(f"Rendered Video URL: {render_url}")

        # Check if the rendering was successful and if URL is available
        if render_status == 'completed' and render_url:
            return jsonify({
                "message": "Render completed successfully",
                "video_url": render_url
            }), 200
        else:
            # Log what was actually received if the URL isn't present
            print(f"Render not completed or URL not provided: {data}")
            return jsonify({
                "message": "Render not completed or failed",
                "data_received": data
            }), 400

    except Exception as e:
        # Log any exception that occurs during processing
        print(f"Error processing webhook: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from environment, default to 5000
    app.run(host='0.0.0.0', port=port)
