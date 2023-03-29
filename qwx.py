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
        # prompt = "你是一个英语单词、短语查询助手，每当用户向你咨询某个单词、短语或者语法相关问题时，尽量简明扼要的回答。" \
        #          "如果用户问的问题和单词、短语咨询没有关系，例如让你写诗、写代码、写笑话、翻译句子或文章等，就拒绝回答"
        prompt = "You are an English word and phrase query assistant. When a user consults you about a certain word, " \
                 "phrase or grammar-related question, try to answer in a concise and clear manner." \
                 "If the question asked by the user has nothing to do with word or phrase consultation, " \
                 "such as asking you to write a poem, code, joke, translate sentences or articles, etc., " \
                 "refuse to answer."
    else:
        print("This is an English word segmentation query assistant.")
        print("Usage: qrx \"question about English\"")
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
            {"role": "user", "content": "kick-off meeting 是什么意思，为啥这里要用 kick-off"},
            {"role": "assistant",
             "content": "\"kick-off\"一般指的是一个项目、计划或活动的启动会议。它是一个团队集合起来，"
                        "讨论项目的目标、范围、进度、资源预算、责任分配等问题的会议。在这个会议中，团队成"
                        "员可以了解项目的整体情况，明确各自的工作内容，确立工作计划，为项目的实施打好基础。"
                        "因此，\"kick-off meeting\"是一个很重要的组织管理活动"},
            {"role": "user", "content": "Help me write a sorting algorithm in Kotlin"},
            {"role": "assistant", "content": "对不起，作为英语单词和短语查询助手，我不能为您编写代码"},
            {"role": "user", "content": message},
        ]
    }

    response = requests.post(OPENAI_BASE_URL, headers=headers, data=json.dumps(data))

    answer = json.loads(response.content)["choices"][0]["message"]["content"].strip()
    print("\033[32m---🤖---------\033[0m")
    print(answer)
    print("\033[32m--------------\033[0m")


if __name__ == "__main__":
    trans(" ".join(sys.argv[1:]))
