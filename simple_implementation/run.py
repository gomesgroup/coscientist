import logging

logging.basicConfig(level=logging.INFO)

from coscientist import Coscientist
from tools import SimpleExpressionExecutor, GetRandomNumber, Stop

tools = [
    SimpleExpressionExecutor('CALCULATE'),
    GetRandomNumber('RANDOM'),
    Stop('STOP')
]

config = {
    "model": "gpt-4-0314",
    "prompt": """You're an assistant and you will be able to perform the following actions:

{{COMMANDS}}

After you got the message, do the action, ask for results and do other actions. Reason every step you're doing. You cannot ask user for any additional information, so perform steps, you think are the most likely to be appropriate.
Your message must end with corresponding command (e.g., PYTHON) and input for that command. Each message may contain only one command.

Example message:
I'm going to do this because of that

COMMAND <input>
"""
}

coscientist = Coscientist(tools, config)
coscientist.run(
    prompt="Generate random number and calculate it's square toot",
    max_steps=10
)
