from interpreter import interpreter
import logging
import sys

#interpreter.llm.supports_vision = True
interpreter.llm.model = "gpt-4o"
#interpreter.llm.api_key = ""

#interpreter.llm.supports_functions = True
#interpreter.llm.context_window = 110000
#interpreter.llm.max_tokens = 4096
#interpreter.auto_run = True
#interpreter.loop = True

#logging.basicConfig(stream=sys.stdout, encoding='UTF-8', level=logging.ERROR, force=True)
#logging.basicConfig(stream=sys.stderr, encoding='UTF-8', level=logging.ERROR, force=True)
#logging.basicConfig(level=logging.DEBUG, filename="debug.txt", filemode="a", force=True)

print(interpreter.messages)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
myapp_file_handler = logging.FileHandler('debug.txt')
myapp_file_handler.setLevel(logging.DEBUG)
simple_formatter = logging.Formatter('LOGGER: %(asctime)s: %(message)s')
myapp_file_handler.setFormatter(simple_formatter)
logger.addHandler(myapp_file_handler)

completions_org = interpreter.llm.completions
def completions_mine(**params):
    logger.debug("###################################################################")
    #print(params["model"])
    #logger.debug(params["messages"])
    logger.debug("messages length: " + str(len(str(params["messages"]))))
    logger.debug(params)
    response = completions_org(**params)
    #logger.debug(response) 
    resplist = list(response)
    #logger.debug(resplist)
    for chunk in resplist:
         #print(chunk)
         if "usage" in chunk and chunk["usage"] != None:
             logger.debug(chunk["usage"])
         if "choices" in chunk and len(chunk["choices"]) != 0:
            content = chunk["choices"][0]["delta"].get("content", "")
            if content != None:
                logger.debug(content)
    return resplist

interpreter.llm.completions = completions_mine

interpreter.chat("list files")
