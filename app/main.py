from app.services.bot import ResearchCollaboratorBot

def main():
    bot = ResearchCollaboratorBot()
    
    print("Research Collaborator Finder Bot")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        response = bot.process_message(user_input)
        print(f"\nBot: {response}")

if __name__ == "__main__":
    main()