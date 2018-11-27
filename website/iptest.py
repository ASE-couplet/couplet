from flask import Flask, render_template, request
# Initialize the Flask application
app = Flask(__name__)
# Default route, print user's IP
@app.route('/')
def index():
  ip = request.remote_addr
  return render_template('index.html', user_ip=ip)
if __name__ == '__main__':
  app.run(
        host="127.0.0.1",
        port=int("8000")
  )