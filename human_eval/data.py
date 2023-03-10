import json
import os


ROOT = os.path.dirname(os.path.abspath(__file__))
HUMAN_EVAL = os.path.join(ROOT, "..", "data", "human-eval.jsonl")


def read_problems(evalset_file=HUMAN_EVAL):
    return {task["task_id"]: task for task in stream_jsonl(evalset_file)}


def stream_jsonl(filename):
    """
    Parses each jsonl line and yields it as a dictionary
    """

    with open(filename, "r") as fp:
        for line in fp:
            if any(not x.isspace() for x in line):
                yield json.loads(line)


def write_jsonl(filename, data, append=False):
    """
    Writes an iterable of dictionaries to jsonl
    """

    if append:
        mode = 'ab'
    else:
        mode = 'wb'

    filename = os.path.expanduser(filename)
    with open(filename, mode) as fp:
        for x in data:
            fp.write((json.dumps(x) + "\n").encode('utf-8'))

if __name__ == "__main__":
    problems = read_problems()
    print(problems.keys())