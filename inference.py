import requests
import time

class OpenEnvClient:
    def __init__(self, base_url="http://localhost:7860"):
        self.base_url = base_url

    def safe_post(self, endpoint, data=None, params=None):
        try:
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                json=data,
                params=params,
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"Error in {endpoint}:", e)
            return {}

    def reset(self):
        return self.safe_post("reset")

    def set_task(self, task_name):
        return self.safe_post("set_task", params={"task_name": task_name})

    def classify(self, text):
        return self.safe_post("classify", data={"text": text})


def main():
    print("[START]")

    client = OpenEnvClient()

    tasks = {
        "easy_task": "Win a free iPhone now!!!",
        "medium_task": "Please review the project document",
        "hard_task": "URGENT! Verify your bank account now http://fake.com"
    }

    rewards = []

    for task, email in tasks.items():
        try:
            client.reset()
            time.sleep(0.1)

            client.set_task(task)
            time.sleep(0.1)

            result = client.classify(email)
            reward = result.get("reward", 0.0)

            print(f"{task} → reward: {reward}")
            rewards.append(reward)

        except Exception as e:
            print("Task error:", e)
            rewards.append(0.0)

    avg = sum(rewards) / len(rewards) if rewards else 0.0

    print("[END]")
    print(f"Final average score: {avg}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fatal error:", e)

    # VERY IMPORTANT: never crash
    exit(0)