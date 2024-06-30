from bottle import Bottle, request, response
import time
import json

app = Bottle()

@app.route('/api', method=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = json.loads(request.body.read())
        time.sleep(0.1)  # Simulating moderate scalability
        response.content_type = 'application/json'
        return data
    else:
        time.sleep(0.1)  # Simulating moderate scalability
        return {"message": "Hello from Bottle App!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
