from locust import HttpUser, task

class GetMahasiswa(HttpUser):

    @task
    def get_vanessa(self):
        #self.client.get("/read/1906350793")
        self.client.get("/read/1906350793/1")