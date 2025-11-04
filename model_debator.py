from enum import Enum
from model_conversation import ModelConversation, Model

class MessageTone(Enum):
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    FORMAL = ("Formal", "Professional and structured communication with proper grammar, sophisticated vocabulary, and respectful tone")
    INFORMAL = ("Informal", "Casual and relaxed communication using contractions, colloquial language, and everyday expressions")
    FRIENDLY = ("Friendly", "Warm and approachable communication that builds rapport and uses positive, encouraging language")
    PROFESSIONAL = ("Professional", "Business-like communication focused on clarity, efficiency, and maintaining professional boundaries")
    HUMOROUS = ("Humorous", "Light-hearted and entertaining communication incorporating jokes, puns, and witty remarks, use some emoticons 😊")
    SARCASTIC = ("Sarcastic", "Ironic and mocking communication using exaggerated statements and subtle criticism")
    TROLLING = ("Trolling", "Provocative and disruptive communication intended to elicit reactions, often using inflammatory language and controversial topics")    

class ModelDebator:
    def __init__(self, model: Model, debate_for: str, tone: MessageTone = MessageTone.FORMAL):
        self.model = model
        self.tone = tone
        self.debate_for = debate_for
        self.conversation = ModelConversation(model=self.model)

    async def send_message(self, message: str,) -> str:
        # Send a message to the model and get the response
        response = await self.conversation.send(message)
        return response