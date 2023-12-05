from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"


if __name__ =='__main__s':
    app.run(debug=True)
