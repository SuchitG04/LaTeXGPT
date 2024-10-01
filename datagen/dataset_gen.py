import os, asyncio, json, random, logging

from prompts import description_sys_prompt, nl_sys_prompt
from together import AsyncTogether, Together
from datasets import load_dataset
from dotenv import load_dotenv
from itertools import islice
from typing import TextIO, Any
from openai import OpenAI
from time import sleep

load_dotenv()

logger = logging.getLogger("datagen")
logger.setLevel(logging.INFO)
logging.basicConfig(filename="datagen.log", encoding="utf-8", level=logging.INFO)

async_client = AsyncTogether(
    api_key=os.getenv("TOGETHER_API_KEY")
)


async def generate_instruction(latex_eqns: list[str], sys_prompt: str):
    tasks = [
        async_client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": eqn},
            ]
        )
        for eqn in latex_eqns
    ]
    responses = await asyncio.gather(*tasks)
    return responses


def save_data(qn_batch: list[Any], ans_batch: list[str], ans_type: str, data_file: TextIO):
    """Save the dataset in the instruction answer pair format."""
    logger.info(f" [DATA_PERSIST] Persisting data of type {ans_type}")
    
    for qn, ans in zip(qn_batch, ans_batch):
        dict_obj = {"qn": qn.choices[0].message.content, "ans": ans, "type": ans_type}
        json.dump(dict_obj, data_file, ensure_ascii=False)
        data_file.write('\n')
        
    logger.info(f" [DATA_PERSIST] Successfully persisted data of type {ans_type}")


def create_instruction_data(eqn_file: str, data_file: str, batch_sz: int = 8, n_retry: int = 5):
    """Create instruction dataset given a LaTeX equations filepath and a output path."""
    eqn_file = open(eqn_file, 'r')
    data_file = open(data_file, 'a')
    
    i = 0
    while True:
        
        batch = list(islice(eqn_file, batch_sz))
        if not batch:
            logger.info(f" [DATA_GEN] DONE.")
            break

        for _ in range(n_retry):
            try:
                logger.info(f" [DATA_GEN] Starting generation for batch {i+1} type 'desc'")
                desc = asyncio.run(generate_instruction(batch, description_sys_prompt))
                save_data(desc, batch, "desc", data_file)
                logger.info(f" [DATA_GEN] Finished generation for batch {i+1} type 'desc'")
            except:
                logger.info(f" [DATA_GEN] Generation FAILED for batch {i+1} type 'desc'. Retrying ...")
                sleep(2)
                continue
            else:
                break

        for _ in range(n_retry):
            try:
                logger.info(f" [DATA_GEN] Starting generation for batch {i+1} type 'nl'")
                nl = asyncio.run(generate_instruction(batch, nl_sys_prompt))
                save_data(nl, batch, "nl", data_file)
                logger.info(f" [DATA_GEN] Finished generation for batch {i+1} type 'nl'")
            except:
                logger.info(f" [DATA_GEN] Generation FAILED for batch {i+1} type 'nl'. Retrying ...")
                sleep(2)
                continue
            else:
                break

        i += 1

    eqn_file.close()
    data_file.close()

create_instruction_data("sample.txt", "data_batched.jsonl")