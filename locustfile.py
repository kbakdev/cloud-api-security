from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def get_api(self):
        self.client.get("/api")

    @task(2)
    def post_api(self):
        self.client.post("/api", json={"key": "value"})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
