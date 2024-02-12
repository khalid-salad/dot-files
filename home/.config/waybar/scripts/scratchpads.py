#!/usr/bin/env python3
import json
import subprocess
import sys


def findScratchpads(sway_tree: str) -> int:
    # sway_tree = subprocess.run(
    # ["swaymsg", "-t", "get_tree"], stdout=subprocess.PIPE
    # ).stdout

    data = json.loads(sway_tree)

    scratchpad_count = len(data["nodes"][0]["nodes"][0]["floating_nodes"])

    return scratchpad_count


def main():
    print(findScratchpads(sys.stdin.read()))

if __name__ == "__main__":
    main()
