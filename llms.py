import requests
import json

class LLMs:

# --- Example Usage ---

    def deepseek(self, text: str, model: str, key: str) -> str:
        """
        Calls DeepSeek chat completion API
        """
        url = "https://api.deepseek.com/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                content = (
                    data["choices"][0]["message"]["content"]
                    .replace("```", "")
                    .replace("sparql", "")
                )
                return content
            else:
                print(f"Error: {response.status_code}")
                try:
                    error_message = response.json()["error"]["message"]
                    return f"Failed: {error_message}"
                except Exception:
                    return f"Failed: {response.text}"

        except Exception as e:
            return f"Failed to fetch answer from DeepSeek: {str(e)}"

    def chatgpt(self, text: str, model: str, key: str) -> str:
        """
        Calls OpenAI Chat Completion API (GPT-4o etc.)
        """
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],
            "temperature": 0.5,
            "max_completion_tokens": 8000
        }

        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                content = (
                    data["choices"][0]["message"]["content"]
                    .replace("```", "")
                    .replace("sparql", "")
                )
                return content
            else:
                print(f"Error: {response.status_code}")
                try:
                    error_message = response.json()["error"]["message"]
                    return f"Failed: {error_message}"
                except Exception:
                    return f"Failed: {response.text}"

        except Exception as e:
            return f"Failed to fetch answer from OpenAI: {str(e)}"
        

      