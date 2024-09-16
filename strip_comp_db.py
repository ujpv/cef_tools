import json
import argparse

white_list = [
    "../../base/",
    "../../cc/",
    "../../cef/",
    "../../content/",
    "../../ipc/",
    "../../media/",
    "../../mojo/",
    "../../skia/",
    "../../ui/",
    "../../url/",
    "../../v8/"
]


def check(item):
    for path in white_list:
        command = item.get("command", "")
        if command.startswith("python") or command.startswith("/bin/ln") or command.startswith("/bin/rm"):
            return False

        if path in item.get("file", ""):
            return True

    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Compilation database path")
    parser.add_argument("-o", "--output", help="Output compilation database path")
    args = parser.parse_args()

    print("Reading compilation database...", end="")
    with open(args.input, encoding="utf-8", errors='ignore') as f:
        items = json.load(f)
    print(f"Done({len(items)} records)")

    print("Filtering...", end="")
    items = list(filter(check, items))
    print(f"Done({len(items)} records left)")

    output = args.output or args.input
    print(f"Saving {output}...", end="")
    with open(output, "w") as f:
        json.dump(items, f, indent=2)
    print("Done")


if __name__ == '__main__':
    main()
