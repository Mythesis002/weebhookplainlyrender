from flask import Flask, request, jsonify

app = Flask(__name__)

# Route for handling webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Get the data from the request
        data = request.json
        print("Webhook received:", data)
        
        # You can extract the rendered video URL from the data
        rendered_video_url = data.get('output', {}).get('url')
        if rendered_video_url:
            print("Rendered Video URL:", rendered_video_url)
        else:
            print("Video is still processing or there was an error.")
        
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed"}), 400

if __name__ == '__main__':
    app.run(port=1000)
