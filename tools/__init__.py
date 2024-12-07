import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import re
import time
import logging

load_dotenv(Path(__file__).parent.parent / ".env")


def get_input(day: int) -> str:
    path = Path(__file__).parent.parent / str(day).zfill(2) / "input.txt"
    if not path.exists():
        data = requests.get(
            f"https://adventofcode.com/2024/day/{day}/input",
            cookies={"session": os.getenv("AOC_SESSION")},
        ).text
        path.write_text(data, encoding="utf-8")
    return path.read_text("utf-8")


PARSER_MAP = {
    r"(\d+)": int,
    r"(\d+\.\d+)": float,
}


def parse_data(data: list[str], *pattern: list[str]) -> list:
    parser = [
        PARSER_MAP[p] if p in PARSER_MAP else str for p in pattern if p.startswith("(")
    ]
    matcher = re.compile(r"".join(pattern))
    res = [[] for _ in range(len(parser))]
    for line in data:
        m = matcher.match(line)
        for i, p in enumerate(parser):
            res[i].append(p(m.group(i + 1)))
    return res


def parse_input(day: int, *pattern: list[str]) -> list:
    return parse_data(get_input(day).splitlines(), *pattern)


def parse_test(day: int, *pattern: list[str]) -> list:
    path = Path(__file__).parent.parent / str(day).zfill(2) / "test.txt"
    assert path.exists()
    return parse_data(path.read_text("utf-8").splitlines(), *pattern)


def profile(func):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    def wrap(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        logging.info(time.time() - started_at)
        return result

    return wrap
