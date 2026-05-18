from locust import HttpUser, task, between
import uuid
import random


class DeviceStatsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post("/user/", json={"name": f"load_user_{uuid.uuid4()}"})
        self.user_id = response.json()["id"]

        response = self.client.post("/device/", json={"name": f"load_device_{uuid.uuid4()}", "user_id": self.user_id})
        self.device_id = response.json()["id"]

        for _ in range(5):
            self.client.post(
                f"/reading/{self.device_id}",
                json={"x": random.uniform(0, 100), "y": random.uniform(0, 100), "z": random.uniform(0, 100)},
            )

    @task(5)
    def add_reading(self):
        self.client.post(
            f"/reading/{self.device_id}",
            json={"x": random.uniform(0, 100), "y": random.uniform(0, 100), "z": random.uniform(0, 100)},
        )

    @task(3)
    def get_device_stats(self):
        self.client.get(f"/stats/device/{self.device_id}")

    @task(2)
    def get_user_stats(self):
        self.client.get(f"/stats/user/{self.user_id}/aggregated")

    @task(1)
    def get_readings_history(self):
        self.client.get(f"/reading/{self.device_id}?limit=50")
