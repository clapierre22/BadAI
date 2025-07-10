from chatbot import BadAI

class attack:
    # Base class for all attacks
    def __init__(self, chatbot, id):
        self.chatbot = chatbot
        self.id = id

    def execute(self):
        raise NotImplementedError("Subclasses should implement this method")

    def valid_attack(self):
        raise NotImplementedError("Subclasses should implement this method")

class xpi_attack(attack):
    # Cross Prompt Injection Attack
    def __init__(self, chatbot, id):
        super().__init__(chatbot, id)

    def execute(self):
        pass

    def valid_attack(self):
        return False
    
class hallucination:
    def __init__(self, chatbot, id):
        super().__init__(chatbot, id)

    def execute(self):
        pass

    def valid_attack(self):
        return False