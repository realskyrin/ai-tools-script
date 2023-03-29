#!/usr/bin/env python3
# This is an English word segmentation query assistant.

import json
import requests
import sys
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')


def trans(message):
    message = json.dumps(message)

    if len(sys.argv) > 1:
        prompt = "你是一个英语单词变种查询助手，每当用户发送一个单词给你，你都要将该词的所有变种以固定格式发送给用户"
    else:
        print("This is an English word segmentation query assistant.")
        print("Usage: qrf word")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "top_p": 1,
        "frequency_penalty": 1,
        "presence_penalty": 1,
        "stream": False,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "use"},
            {"role": "assistant",
             "content": "[\"uses\",\"used\",\"usage\",\"using\"]"},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(OPENAI_BASE_URL, headers=headers, data=json.dumps(data))

    answer = json.loads(response.content)["choices"][0]["message"]["content"].strip()
    print("\033[32m---🤖---------\033[0m")
    print(answer)
    print("\033[32m--------------\033[0m")


if __name__ == "__main__":
    trans(" ".join(sys.argv[1:]))