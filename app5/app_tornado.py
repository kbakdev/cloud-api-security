import tornado.ioloop
import tornado.web
import time
import json

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        time.sleep(0.1)  # Simulating moderate scalability
        self.write({"message": "Hello from Tornado App!"})

    async def post(self):
        data = json.loads(self.request.body)
        time.sleep(0.1)  # Simulating moderate scalability
        self.write(data)

def make_app():
    return tornado.web.Application([
        (r"/api", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
