# q_bot.py
from q_responses import get_response

QUIT_COMMAND = "quit"


def query_chatbot(question):
    return get_response(question)


def main_loop():
    while True:
        player_question = input("Ask Q a question: ")
        if player_question.lower() == QUIT_COMMAND:
            break
        print(f"Q: {query_chatbot(player_question)}")


# Example interaction
if __name__ == "__main__":
    main_loop()
