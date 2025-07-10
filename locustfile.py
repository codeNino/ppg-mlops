from locust import HttpUser, task, between

class UploadTestUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def upload_existing_csv(self):
        # Open the CSV file from your directory
        with open("./PPG_Raw_Dataset/RawData/signal_01_0001.csv", "rb") as f:
            files = {
                "signal": ("sample.csv", f, "text/csv")
            }

            data = {
                "age": 30,
                "gender": "Female",
                "height" : 107,
                "weight" : 65
            }

            response = self.client.post(
                "/upload",
                files=files,
                data=data
            )

            if response.status_code != 200:
                print("Upload failed:", response.status_code, response.text)
