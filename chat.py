import os
import builtins
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class Chat:
    '''
    >>> chat = Chat()
    >>> isinstance(chat.send_message('my name is bob', temperature=0.0), str)
    True
    >>> isinstance(chat.send_message('what is my name?', temperature=0.0), str)
    True
    '''

    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
        self.messages = [
            {
                "role": "system",
                "content": "Write the output in 1-2 sentences. Talk like pirate."
            },
        ]

    def send_message(self, message, temperature=0.8):
        self.messages.append({
            "role": "user",
            "content": message
        })

        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model="llama-3.1-8b-instant",
            temperature=temperature,
        )

        result = chat_completion.choices[0].message.content

        self.messages.append({
            "role": "assistant",
            "content": result
        })

        return result


def repl():
    '''
    >>> def monkey_input(prompt, user_inputs=['hello', 'goodbye']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> old_input = builtins.input
    >>> old_send_message = Chat.send_message
    >>> builtins.input = monkey_input
    >>> Chat.send_message = lambda self, message, temperature=0.8: 'mock response'
    >>> repl()
    chat> hello
    mock response
    chat> goodbye
    mock response
    <BLANKLINE>
    >>> builtins.input = old_input
    >>> Chat.send_message = old_send_message
    '''
    import readline
    chat = Chat()
    try:
        while True:
            user_input = input('chat> ')
            response = chat.send_message(user_input)
            print(response)
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()