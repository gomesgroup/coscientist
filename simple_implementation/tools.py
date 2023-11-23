import random


class StopIteration(Exception):
    def __init__(self):
        super().__init__()
        self.message = 'Execution stopped by model.'


class SimpleExpressionExecutor:
    def __init__(self, command_name: str) -> None:
        self.command_name = command_name
        self.prompt = f"""{self.command_name} python expression
This tools lets you execute simple expressions. Here is a simple example:
{command_name} 1 + 1

You can use any Python expression, but remember to use the correct syntax."""

    def __call__(self, input: str) -> str:
        try:
            return str(eval(input))
        except Exception as e:
            return str(e)


class GetRandomNumber:
    def __init__(self, command_name: str) -> None:
        self.command_name = command_name
        self.prompt = f"""{self.command_name} number
This tools lets you generate a random number. Here is a simple example:
{command_name} 1 10

The command above will generate a random number between 1 and 10."""

    def __call__(self, input: str) -> str:
        input = input.split(' ')

        if len(input) != 2:
            return 'Invalid input. Please provide two numbers.'

        low = int(input[0])
        high = int(input[1])

        return str(random.randint(low, high))


class Stop:
    def __init__(self, command_name: str) -> None:
        self.command_name = command_name
        self.prompt = f"""{self.command_name} stop
This tools lets you stop the conversation if you think that the task is completed.
It is useful when the user continues to ask for commands."""

    def __call__(self, input: str) -> str:
        raise StopIteration()
