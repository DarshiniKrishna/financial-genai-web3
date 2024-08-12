from flask import Flask, render_template, request, jsonify
import google.generativeai as palm
import os

api = os.getenv("MAKERSUITE_API_TOKEN")
model = {"model": "models/chat-bison-001"}
palm.configure(api_key=api)

if not api:
    raise ValueError("MAKERSUITE_API_TOKEN environment variable is not set")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    q = request.form.get("q")
    return render_template("main.html", r=q)

@app.route("/makersuite", methods=["GET", "POST"])
def makersuite():
    return render_template("makersuite.html")

@app.route("/makersuite_1", methods=["GET", "POST"])
def makersuite_1():
    try:
        q = "Can you help me prepare my tax return?"
        r = palm.chat(**model, messages=q)
        print(f"API Response: {r}")
        response_text = getattr(r, 'last', 'No response available')
        return render_template("makersuite_1_reply.html", r=response_text)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while processing your request. Please try again later.", 500

@app.route("/makersuite_gen", methods=["GET", "POST"])
def makersuite_gen():
    try:
        q = request.form.get("q")
        r = palm.chat(**model, messages=q)
        print(f"API Response: {r}")
        response_text = getattr(r, 'last', 'No response available')
        return render_template("makersuite_gen_reply.html", r=response_text)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while processing your request. Please try again later.", 500

if __name__ == "__main__":
    app.run(debug=True)
