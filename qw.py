#!/usr/bin/env python3
# This is an English word search assistant.

import json
import requests
import sys
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')


def query(message):
    message = json.dumps(message)

    if len(sys.argv) > 1:
        prompt = "你是一个英语单词查询助手，每当用户发送一个英语单词给你，你都要以固定格式响应用户，" \
                 "如果用户发给你的不是一个单词，回复 'invalid token'"

        response_few_shot_text = "run [/rʌn/]" \
                                 "\n\nn. 奔跑;竞赛;连续的演出\nHe went for a run after work. (他下班后去跑步了)" \
                                 "\n\nv. 奔跑;运行\nI like to run in the park every morning. (我喜欢每天早上在公园里跑步)" \
                                 "\n\nadj. 连续的;流畅的\nThis printer is really fast and runs smoothly. (这台打印机速度非常快，而且运行流畅)"
    else:
        print("This is an English word search assistant")
        print("Usage: qr word")
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
            {"role": "user", "content": "run"},
            {"role": "assistant", "content": response_few_shot_text},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(OPENAI_BASE_URL, headers=headers, data=json.dumps(data))

    answer = json.loads(response.content)["choices"][0]["message"]["content"].strip()
    print("\033[32m---🤖---------\033[0m")
    print(answer)
    print("\033[32m--------------\033[0m")


if __name__ == "__main__":
    query(" ".join(sys.argv[1:]))
