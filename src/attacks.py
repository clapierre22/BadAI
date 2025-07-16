import json, os

def load_attack_commands(json_path):
    with open(json_path, 'r') as file:
        commands = json.load(file)
            
    return [phrase['command'].lower() for phrase in commands.get('attack_commands', [])]

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
        
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Commands.JSON')
        json_path = os.path.abspath(json_path)
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found at {json_path}")
        self.attack_phrases = load_attack_commands(json_path)
        print(self.attack_phrases)

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