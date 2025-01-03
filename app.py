from flask import Flask, render_template, request
from twitter_trending import fetch_twitter_trends
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch_trends", methods=["GET"])
def fetch_trends():
    result = fetch_twitter_trends()
    if result:
        return jsonify({
            "status": "success",
            "data": result
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch trending topics."
        }), 500

if __name__ == "__main__":
    # Enable debug mode for development
    app.run(debug=True)
