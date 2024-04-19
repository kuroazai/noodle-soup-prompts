import random
import json
import os
import requests
from typing import Union


def download_pantry(url: str, output: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Failed to download {url}')
    print(f'Downloading {url} to {output}')
    with open(output, 'wb') as f:
        f.write(response.content)
        f.close()


def nsp_parse(prompt: Union[list, dict, str], nspterminology: dict = None) -> dict:
    new_prompts = []
    new_dict = {}

    if not nspterminology:
        with open('./nsp_pantry.json', 'r', encoding='cp932', errors='ignore') as f:
            nspterminology = json.loads(f.read())

    if isinstance(prompt, dict):
        for pstep, pvalue in prompt.items():
            if isinstance(pvalue, list):
                for prompt in pvalue:
                    new_prompt = prompt
                    for term in nspterminology:
                        tkey = f'_{term}_'
                        tcount = prompt.count(tkey)
                        for i in range(tcount):
                            new_prompt = new_prompt.replace(tkey, random.choice(nspterminology[term]), 1)
                    new_prompts.append(new_prompt)
                new_dict[pstep] = new_prompts
                new_prompts = []
        return new_dict
    elif isinstance(prompt, list):
        for pstr in prompt:
            new_prompt = pstr
            for term in nspterminology:
                tkey = f'_{term}_'
                tcount = new_prompt.count(tkey)
                for i in range(tcount):
                    new_prompt = new_prompt.replace(tkey, random.choice(nspterminology[term]), 1)
            new_prompts.append(new_prompt)
        return new_prompts
    elif isinstance(prompt, str):
        new_prompt = prompt
        for term in nspterminology:
            tkey = f'_{term}_'
            tcount = new_prompt.count(tkey)
            for i in range(tcount):
                new_prompt = new_prompt.replace(tkey, random.choice(nspterminology[term]), 1)
        return new_prompt


if not os.path.exists('./nsp_pantry.json'):
    download_pantry('https://raw.githubusercontent.com/WASasquatch/noodle-soup-prompts/main/nsp_pantry.json',
                    './nsp_pantry.json')
