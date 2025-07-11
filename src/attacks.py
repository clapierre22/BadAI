
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
    # Cross Prompt Injection Attack, detect the admin command and execute it
    def __init__(self, chatbot, id):
        super().__init__(chatbot, id)

    def execute(self):
        pass

    def valid_attack(self):
        return False
    
class hallucination(attack):
    # If prompt is not in training data, hallucinate a response
    def __init__(self, chatbot, id):
        super().__init__(chatbot, id)

    def execute(self):
        pass

    def valid_attack(self):
        return False
    
class data_leak(attack):
    # When the user does not ask outright for data, but rather asks a questions that would require a data leak to answer
    def __init__(self, chatbot, id):
        super().__init__(chatbot, id)

    def execute(self):
        pass

    def valid_attack(self):
        return False