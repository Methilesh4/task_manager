from flask import Flask, request, render_template, redirect
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def render():
    return  render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)
