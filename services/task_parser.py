import re


def parse_tasks(text):

    pattern = r'(\w+)[её]?\s+нужно\s+([^\.]+)'

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    tasks = []

    for name, task in matches:

        tasks.append({
            "name": name,
            "task": task.strip()
        })

    return tasks