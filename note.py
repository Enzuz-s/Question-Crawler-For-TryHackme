import re
import sys
from datetime import datetime

import requests

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
name = "Enhzuz"
code = ""


def get_room_code(s):
    if len(s) == 1:
        print("USAGE: ./note.py [url] [room code]")
    else:
        if s[1].startswith("https://tryhackme.com/room/"):
            room_code = s[1].split('/')[-1]
        else:
            room_code = s[1]
        write_notes(room_code)


def get_room_tasks(task_code):
    task_data = requests.get(f"https://tryhackme.com/api/tasks/{task_code}").json()['data']
    return task_data


def parse_task_data(data):
    output = []
    for task in data:
        output.append(f"# Task {task['taskNo']} - {task['taskTitle']}\n")
        for x in task["questions"]:
            output.append(f"> {x['question']}\n")
            output.append("```\n\n```\n")
    return output


def date_generator():
    x = datetime.now()
    return x.strftime("%B %d, %Y")


def get_room_name(rooms_code):
    return requests.get(f"https://tryhackme.com/api/room/details?codes={rooms_code}").json()[rooms_code]["title"]


def write_notes(room):
    with open('README.md', 'w') as f:
        f.write(f"# {get_room_name(room)}\n\n")
        f.write(f"{name} | {date_generator()}\n\n")
        questions = tag_re.sub("", "\n".join(parse_task_data(get_room_tasks(room))))
        f.write(f"{questions}")
    print("Wrote notes file!")


get_room_code(sys.argv)
