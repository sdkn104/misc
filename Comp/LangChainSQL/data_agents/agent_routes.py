# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import random
import sys
import os
import mimetypes
import re
import json
import traceback
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')

#import flask
#from flask import request, session, jsonify, Blueprint, current_app, Response, stream_with_context
import logging

import json
import html
import pandas as pd
from pprint import pprint, pformat

from data_agents.agent_py_data_rec import PythonDataRecAgent
from data_agents.agent_interactive_explore import InteractiveExploreAgent

#from data_agents.agent_report_gen import ReportGenAgent
from data_agents.client_utils import Client


# Get logger for this module (logging config done in app.py)
logger = logging.getLogger(__name__)
custom_logger = logging.getLogger("app")

def get_client(model_config):
    for key in model_config:
        model_config[key] = model_config[key].strip()
    client = Client(
        model_config["endpoint"],
        model_config["model"],
        model_config["api_key"] if "api_key" in model_config else None,
        html.escape(model_config["api_base"]) if "api_base" in model_config else None,
        model_config["api_version"] if "api_version" in model_config else None)

    return client

def derive_data(input_tables, model_config, instruction, prev_messages=[], max_repair_attempts=1, agent_coding_rules=""):

    logger.info("# request data: ")

    client = get_client(model_config)
    language = "python"

    logger.info("== input tables ===>")
    for table in input_tables:
        logger.info(f"===> Table: {table['name']} (first 5 rows)")
        logger.info(table['rows'][:5])

    logger.info("== user spec ===")
    logger.info(instruction)

    agent = PythonDataRecAgent(client=client, exec_python_in_subprocess=False, agent_coding_rules=agent_coding_rules)

    print("=== run start")
    print(instruction, prev_messages)
    results = agent.run(input_tables, instruction, n=1, prev_messages=prev_messages)
    custom_logger.info("@@@ result of agent.run():")
    custom_logger.info(pformat(results, width=120))
    print("=== run results")
    print(results[0]["status"])
    #print(results[0]["code"])
    print(results[0]["refined_goal"])

    repair_attempts = 0
    while results[0]['status'] == 'error' and repair_attempts < max_repair_attempts: # try up to n times
        error_message = results[0]['content']
        new_instruction = f"We run into the following problem executing the code, please fix it:\n\n{error_message}\n\nPlease think step by step, reflect why the error happens and fix the code so that no more errors would occur."

        prev_dialog = results[0]['dialog']
        print("=== followup start")
        print(new_instruction)
        results = agent.followup(input_tables, prev_dialog, [], new_instruction, n=1)
        print("=== followup results")
        print(results[0]["status"])
        #print(results[0]["code"])
        print(results[0]["refined_goal"])

        repair_attempts += 1
        
    return results

def get_recommendation_questions(input_tables, model_config, prev_messages=[], max_repair_attempts=1, agent_exploration_rules="", 
                                 start_question=None, exploration_thread=None, current_chart=None, current_data_sample=None):
    def generate():
        logger.info("# get recommendation questions request")

        client = get_client(model_config)

        agent = InteractiveExploreAgent(client=client, agent_exploration_rules=agent_exploration_rules)
        
        try:
            for chunk in agent.run(input_tables, start_question=start_question, 
                                   exploration_thread=exploration_thread, current_data_sample=current_data_sample, current_chart=current_chart, mode="interactive"):
                yield chunk
        except Exception as e:
            logger.error(e)
            error_data = { 
                "content": "unable to process recommendation questions request" 
            }
            yield 'error: ' + json.dumps(error_data) + '\n'

    print("@@ get_recommendation_questions")
    response = generate()
    a = [res for res in response]
    b = "".join(a)
    results = re.split(r'\r?\ndata: ', re.sub(r"^data: ", "", b))
    results = [json.loads(r) for r in results]
    #print("\n=== run results")
    #pprint(results)
    return results


import pandas as pd

def read_csv(file_path, name="average-price-data", attached_metadata=""):
    df = pd.read_csv(file_path)

    return {
        "attached_metadata": attached_metadata,
        "name": name,
        "rows": df.to_dict(orient="records")
    }

