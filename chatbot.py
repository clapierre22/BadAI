# BadAI class file, potential additional chatbot functionality. 
# Note: Split into the different bots i.e., PersonalAssistant, HR Chatbot, Internal Processor, etc.
# LM: 7/7/24 - Calvin LaPierre

class BadAI:
    # Base AI chatbot class
    def __init__(self):
        print("Initializing BadAI Security Chatbot...\n")
        self.attacks = {
            "cross_prompt_injection": None,
            "hallucinations": None,
            "data_leak": None
        }
        print("Initializing BadAI Attacks...\n")
        self.load_attacks()

    def chat_init(self):
        #Initialize the chat functionality
        print("Initializing BadAI Chat Function...\n")
        print("Welcome to the BadAI Security Chatbot!\n")
        print("Type 'exit' to end the conversation.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("BadAI: Goodbye!")
                break
            self.process_input(user_input)

    def process_input(self, user_input):
        print("BadAI is Processing Input...\n")
        if "cross prompt injection" in user_input.lower():
            print("BadAI: Initiating Cross Prompt Injection Attack...\n")
        elif "hallucination" in user_input.lower():
            print("BadAI: Initiating Halucination...\n")
        elif "data leak" in user_input.lower():
            print("BadAI: Initiating Data Leak...\n")
        else:
            print("BadAI: I'm sorry, I didn't understand that.\n")