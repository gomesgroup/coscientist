import openai
import logging
from tools import StopIteration

class Coscientist:
    def __init__(self, tools, config):
        self.config = config
        self.history = []

        self.tools = {
            tool.command_name: tool for tool in tools
        }
        self.commands_string = ', '.join([f'`{k}`' for k in self.tools])

        detailed_tool_prompts = '\n\n'.join([tool.prompt for tool in tools])

        self.history.append(
            self.message_to_oai_format(
                self.config['prompt'].replace('{{COMMANDS}}', detailed_tool_prompts), 'assistant'
            )
        )

        self.log_last_history_message()

    def log_history_message(self, message: dict) -> None:
        logging.info(f'{message["role"]}: {message["content"]}')

    def log_last_history_message(self) -> None:
        self.log_history_message(self.history[-1])

    def get_next_message(self) -> str:
        response = openai.ChatCompletion.create(
            model=self.config['model'],
            messages=self.history
        ).choices[0].message.content
        self.history.append(self.message_to_oai_format(response, 'assistant'))
        self.log_history_message(self.history[-1])

        return response

    def count_calls(self, message: str) -> int:
        return sum([message.count(tool) for tool in self.tools])

    def error_no_calls(self):
        self.history.append(self.message_to_oai_format(
            "You haven't provided any command. Remember that you should follow the format: [" +
            self.commands_string + "] + <your input>", 'user'))
        self.log_last_history_message()

    def error_too_many_calls(self):
        self.history.append(self.message_to_oai_format(
            "Provide only one command at a time, wait for the answer and then run the next command.", 'user'))
        self.log_last_history_message()

    def message_to_oai_format(self, message: str, role: str) -> dict:
        return {
            # "type": "message",
            "role": role,
            "content": message
        }

    def run(self, prompt: str, max_steps: int = 10) -> None:
        self.history.append(self.message_to_oai_format(prompt, 'user'))

        for i in range(max_steps):
            message = self.get_next_message()
            number_of_calls = self.count_calls(message)

            if number_of_calls == 0:
                self.error_no_calls()
                continue

            if number_of_calls > 1:
                self.error_too_many_calls()
                continue

            # Extracting single line; in real implementation multiple lines are supported

            lines = message.split('\n')
            for line in lines:
                if any([line.startswith(tool + ' ') for tool in self.tools]):
                    tool, argument = line.split(' ', 1)

                    try:
                        tool_output = self.tools[tool](argument)

                        self.history.append(self.message_to_oai_format(tool_output, 'user'))
                        self.log_last_history_message()

                    except StopIteration:
                        return
