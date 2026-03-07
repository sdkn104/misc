
# Data Agent that generates goals and visuals

import os
import pandas as pd
from pathlib import Path
from data_agents.agent_routes import derive_data, get_recommendation_questions
import logging
from data_agents.visual_engine import show_vega_lite_chart
from pprint import pprint, pformat


#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
# 標準出力
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
# ファイル出力
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
#logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.info("==============================================================================================")
logger.info(" START")
logger.info("==============================================================================================")

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python py_csv_agent.py <csv_file_path>")
        return
    csv_file = sys.argv[1]

    # read CSV
    table = read_csv(csv_file)
    print(f"Loaded table {table['name']} with {len(table['rows'])} rows")

    # Model
    model_config={"endpoint": "azure", 
                  "model": os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"), 
                  "api_key": os.environ.get("AZURE_OPENAI_API_KEY") , 
                  "api_base": os.environ.get("AZURE_OPENAI_ENDPOINT"), 
                  "api_version": os.environ.get("OPENAI_API_VERSION")
    }

    # explore goals
    instruction_exp = "データの内容から、データ分析者が知りたいことを考えて、10個のquestionを考えてください"
    goals = get_recommendation_questions(input_tables=[table], model_config=model_config, 
                                         start_question=instruction_exp, prev_messages=[], max_repair_attempts=1)
    pprint(goals)

    for goal in goals:

        # Generate Goal and Transformation
        instruction = "データの内容から、データ分析者が知りたいことを考えて、そのために必要な可視化をしてください"
        instruction = goal["instruction"]
        results = derive_data(input_tables=[table], model_config=model_config, 
                            instruction=instruction)
        
        if results[0]["status"] != "ok":
            print("======= NOT ok, skip!")
            continue

        # Visual
        vega_lite = results[0]["refined_goal"]["vega_lite"]
        derived_table = results[0]["content"]
        if not isinstance(vega_lite, dict) or not isinstance(derived_table, dict):
            print("===== error in result from derive_data")
            continue

        vega_lite["data"] = {"values": derived_table["rows"]}
        show_vega_lite_chart(vega_lite, goal["goal"] + '<br>' + goal["instruction"])


def read_csv(file_path, name=None, attached_metadata=""):
    df = pd.read_csv(file_path)
    tname = Path(file_path).stem if name is None else name
    return {
        "attached_metadata": attached_metadata,
        "name": tname,
        "rows": df.to_dict(orient="records")
    }


if __name__ == "__main__":
    main()
    
