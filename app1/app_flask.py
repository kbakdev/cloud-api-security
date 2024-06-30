from flask import Flask, request, jsonify
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@app.route('/api', methods=['GET', 'POST'])
def api():
    time.sleep(0.1)  # Simulating moderate scalability
    if request.method == 'POST':
        data = request.json
        return jsonify(data), 201
    return jsonify({"message": "Hello from Flask App!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
