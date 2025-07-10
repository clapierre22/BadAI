# BadAI main file and startup script
# LM: 7/7/24 - Calvin LaPierre

from chatbot import BadAI

def main():
    chatbot = BadAI()
    print("Welcome to the BadAI Security Chatbot!")
    print("Type 'exit' to end the conversation.")
    
    chatbot.chat_init()

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Ending the chat. Goodbye!")
            break
        chatbot.process_input(user_input)

if __name__ == "__main__":
    main()