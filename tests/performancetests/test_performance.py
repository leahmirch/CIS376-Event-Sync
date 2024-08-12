from locust import HttpUser, TaskSet, task, between, HttpLocust

class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def login(self):
        try:
            response = self.client.post("/login", data={"username": "testuser", "password": "testpassword"})
            if response.status_code == 200:
                print("Logged in successfully")
            else:
                print(f"Failed to log in: {response.status_code}")
                print(f"Response content: {response.text}")
        except Exception as e:
            print(f"Exception during login: {str(e)}")

    @task(2)
    def view_events(self):
        response = self.client.get("/api/events")
        if response.status_code == 404:
            print("Events not found")

    @task(1)
    def create_event(self):
        response = self.client.post("/api/events", json={
            "name": "Performance Test Event",
            "description": "This is a performance test event",
            "date": "2024-08-13 14:00",
            "location": "Test Location"
        })
        if response.status_code != 201:
            print(f"Failed to create event: {response.status_code}")
            print(f"Response content: {response.text}")

    @task(1)
    def view_specific_event(self):
        response = self.client.get("/api/events/1")
        if response.status_code == 404:
            print("Specific event not found")

    @task(1)
    def update_event(self):
        response = self.client.put("/api/events/1", json={
            "name": "Updated Performance Test Event",
            "description": "This event has been updated in a performance test",
            "date": "2024-08-13 15:00",
            "location": "Updated Location"
        })
        if response.status_code != 200:
            print(f"Failed to update event: {response.status_code}")
            print(f"Response content: {response.text}")

    @task(1)
    def delete_event(self):
        response = self.client.delete("/api/events/1")
        if response.status_code != 200:
            print(f"Failed to delete event: {response.status_code}")
            print(f"Response content: {response.text}")

    @task(1)
    def logout(self):
        response = self.client.get("/logout")
        if response.status_code != 302:
            print(f"Failed to log out: {response.status_code}")
            print(f"Response content: {response.text}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    host = "http://localhost:5000"
