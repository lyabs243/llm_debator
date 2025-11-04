# enum models
from enum import Enum
from clients import ModelClient

class Model(Enum):
    def __init__(self, model_name: str, model_key: str):
        self.model_name = model_name
        self.model_key = model_key

    GPT_4_1_MINI = ("gpt-4.1-mini", "openai")
    GPT_4_1 = ("gpt-4.1", "openai")
    GPT_5_MINI = ("gpt-5-mini", "openai")
    GPT_5 = ("gpt-5", "openai")

    GEMINI_2_5_FLASH = ("gemini-2.5-flash", "gemini")
    GEMINI_2_5_PRO = ("gemini-2.5-pro", "gemini")

    GROQ_LLAMA_3_1 = ("llama-3.1-8b-instant", "groq")
    GROQ_LLAMA_3_3 = ("llama-3.3-70b-versatile", "groq")
    GROQ_GPT_OSS_20 = ("openai/gpt-oss-20b", "groq")
    GROQ_GPT_OSS_120 = ("openai/gpt-oss-120b", "groq")

class ModelConversation:
    def __init__(self, model: Model, messages: list[dict] = None):
        self.model = model
        self.messages = messages if messages is not None else []
        self.client = ModelClient.from_provider(model.model_key)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def send(self, message: str) -> str | None:
        """Send a new message"""
        self.add_message(role="user", content=message)

        client = self.client.client
        model = self.model.model_name

        try:
            response = client.chat.completions.create(
                model=model,
                messages=self.messages,
                max_completion_tokens=200,
            )
            answer = response.choices[0].message.content

            self.add_message(role="assistant", content=answer)
            return answer
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
