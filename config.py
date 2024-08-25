# config.py
class Settings:
    class Chat:
        def __init__(self, langchain_verbose: bool):
            self.langchain_verbose = langchain_verbose

    class Together:
        def __init__(self, model: str, api_token: str, temperature: float, top_p: float, repetition_penalty: float):
            self.model = model
            self.api_token = api_token
            self.temperature = temperature
            self.top_p = top_p
            self.repetition_penalty = repetition_penalty

    def __init__(self, chat: Chat, together: Together):
        self.chat = chat
        self.together = together
