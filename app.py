from flask import Flask, request, jsonify
from scraper import search_magic_trick

app = Flask(__name__)

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    results = search_magic_trick(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
