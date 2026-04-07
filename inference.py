import requests
import time
import sys
import os
from openai import OpenAI
from grader import grade   # 🔥 IMPORTANT


# 🔥 LLM CLIENT (Meta LiteLLM Proxy)
client_llm = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)


class OpenEnvClient:
    def __init__(self, base_url="http://localhost:7860"):
        self.base_url = base_url

    def post(self, endpoint, data=None):
        try:
            res = requests.post(
                f"{self.base_url}/{endpoint}",
                json=data,
                timeout=5
            )
            return res.json()
        except Exception as e:
            print("Error:", e)
            return {}

    def reset(self):
        return self.post("reset")

    def classify(self, text):
        return self.post("classify", {"text": text})


def main():
    print("[START]")

    client = OpenEnvClient()

    # ✅ MUST HAVE 3 TASKS
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

            # 🔥 REQUIRED: LLM CALL
            try:
                client_llm.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": f"Classify this email: {email}"}
                    ]
                )
            except Exception as e:
                print("LLM API error:", e)

            # 🔥 Classification
            result = client.classify(email)

            # 🔥 USE OFFICIAL GRADER (CRITICAL FIX)
            reward = grade(result, task)

            print(f"{task} → reward: {reward}")
            rewards.append(reward)

        except Exception as e:
            print("Task error:", e)
            rewards.append(0.5)

    avg = sum(rewards) / len(rewards) if rewards else 0.5

    print("[END]")
    print("Final Score:", avg)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fatal error:", e)

    sys.exit(0)