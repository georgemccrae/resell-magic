from flask import Flask, request, jsonify, render_template
from scraper import search_magic_trick

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    results = search_magic_trick(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
