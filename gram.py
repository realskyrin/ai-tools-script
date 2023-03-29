#!/usr/bin/env python3
# This is an English word search assistant.

import json
from json import JSONDecodeError
import requests
import sys
import re
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')


def query(message):
    message = json.dumps(message)
    if len(sys.argv) > 1:
        # prompt = "你是一个像Grammarly一样的英语语法检查助手，你会修正和润色用户发来的英文语句和标点符号，并按固定格式返回给用户。" \
        #          "如果你删除了某个单词，用<del>标签包裹它。如果你增加了某个单词，用<add>标签标记它" \
        #          "如果用户发送的语句没有问题，则回复 This sentence looks perfect."
        prompt = "You are an English grammar checking assistant like Grammarly." \
                 " You will correct and polish the English sentences sent by users, " \
                 "and return them to the users in a fixed format." \
                 "If you delete a word, wrap it with the <del> tag. If you add a word, wrap it with the <add> tag." \
                 "If the sentence sent by the user is correct and no need to polish, just translate it into Chinese."

        request_content = "I seen he at the library on yesterday."

        response_text = "修正: I <del>seen</del><add>saw</add> <del>he</del><add>him</add> " \
                               "at the library <del>on</del> yesterday." \
                               "\n翻译: 我昨天在图书馆看到了他"

        request_content_2 = "i saw him at the library yesturday."
        response_text_2 = "修正: <del>i</del><add>I</add> saw him at the library " \
                                 "<del>yesturday</del><add>yesterday</add>." \
                                 "\n翻译: 我昨天在图书馆看到了他"
    else:
        print("我是英语语法检查助手")
        print("Usage: gram \"sentence\"")
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
            {"role": "user", "content": request_content},
            {"role": "assistant", "content": response_text},
            {"role": "user", "content": request_content_2},
            {"role": "assistant", "content": response_text_2},
            {"role": "user", "content": "Is there someone who can help me solve this issue? Thanks."},
            {"role": "assistant", "content": "{\"翻译\":\"有人能帮我解决这个问题吗？谢谢。\"}"},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(OPENAI_BASE_URL, headers=headers, data=json.dumps(data))
    answer = ""
    try:
        answer = json.loads(response.content)["choices"][0]["message"]["content"].strip()
    except JSONDecodeError as e:
        print(f"response==={response}\nerror==={e.msg}")
    except ValueError as e:
        print(f"response==={response}\nerror==={e}")
    except Exception as e:
        print(f"response==={response}\nerror==={e}")

    print("\033[32m---🤖---------\033[0m")
    print(color_text(answer))
    print("\033[32m--------------\033[0m")


def color_text(text):
    # 匹配 <del> 标签中的文本，让其变成红色
    text = re.sub(r'<del>(.*?)</del>', r'\033[31m\1\033[0m', text, flags=re.DOTALL)
    # 匹配 <add> 标签中的文本，让其变成绿色
    text = re.sub(r'<add>(.*?)</add>', r'\033[32m\1\033[0m', text, flags=re.DOTALL)
    return text


if __name__ == "__main__":
    query(" ".join(sys.argv[1:]))
