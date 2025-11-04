from model_debator import ModelDebator
from IPython.display import Markdown, display

class ModelDebate:
    def __init__(
        self,
        debator_a: ModelDebator,
        debator_b: ModelDebator,
        topic: str,
        turns: int = 5,
        initial_message: str = "Hello",
        log=True
    ):
        self.debator_a = debator_a
        self.debator_b = debator_b
        self.topic = topic
        self.turns = turns
        self.initial_message = initial_message
        self.log = log
        self.init_debaters()

    # init debaters messages
    def init_debaters(self):
        prompt_a = ModelDebate.generate_system_prompt(self.topic, self.debator_a, self.debator_b)
        prompt_b = ModelDebate.generate_system_prompt(self.topic, self.debator_b, self.debator_a)

        self.debator_a.conversation.add_message(role="system", content=prompt_a)
        self.debator_b.conversation.add_message(role="system", content=prompt_b)

    # class method to generate a debator system prompt
    @classmethod
    def generate_system_prompt(cls, topic: str, debator: ModelDebator, opponent: ModelDebator) -> str:
        return f"""
            You are an expert debater engaged in a structured debate on the topic: "{topic}"

            YOUR POSITION: {debator.debate_for}

            Respect the tone: {debator.tone.description}

            The position of your opponent is: {opponent.debate_for} and his tone is {opponent.tone.title}.

            GUIDELINES:
            - Present strong, well-reasoned arguments supporting your position
            - Address and counter your opponent's points directly
            - Use evidence, logic, and persuasive language
            - Maintain your specified tone throughout the debate
            - Stay on topic
            - Answer in few sentences, 2 - 3 sentences maximum.

            Remember: Your goal is to convincingly defend your position while respectfully engaging with opposing views.
        """

    def log_message(self, message:str):
        if self.log:
            display(Markdown(message))

    async def debate(self):
        self.log_message(f"========= {self.topic} =========")

        self.log_message(f"Debater A: **{self.debator_a.model.model_name}** For: {self.debator_a.debate_for}\nTone: {self.debator_a.tone.title}\n")

        self.log_message(f"Debater B: **{self.debator_b.model.model_name}** For: {self.debator_b.debate_for}\nTone: {self.debator_b.tone.title}\n")

        response_a = self.initial_message
        self.log_message(f"**{self.debator_a.model.model_name}**: {response_a}")
        response_b = await self.debator_b.send_message(message=self.initial_message,)
        self.log_message(f"\n{self.debator_b.model.model_name}: {response_b}")
        

        for _ in range(self.turns):
            response_a = await self.debator_a.send_message(message=response_b,)
            self.log_message(f"**{self.debator_a.model.model_name}**: {response_a}")

            response_b = await self.debator_b.send_message(message=response_a,)
            self.log_message(f"\n**{self.debator_b.model.model_name}**: {response_b}")