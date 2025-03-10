from interpreter import interpreter
import logging
import sys

#logging.basicConfig(stream=sys.stdout, encoding='UTF-8', level=logging.DEBUG, force=True)
logging.basicConfig(level=logging.DEBUG, filename="debug.txt", filemode="a")


interpreter.llm.context_window = 128000
interpreter.llm.max_tokens = 16384
#interpreter.llm.max_output
interpreter.max_output = 2800
#interpreter.llm.max_budget
