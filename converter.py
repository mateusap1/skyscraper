import json
import os


def json_to_txt(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as file:
        final_string = ""

        final_string += data["titulo"] + "\n\n"

        for estrofe in data["estrofes"]:
            for line in estrofe:
                final_string += line + "\n"

            final_string += "\n"

        file.write(final_string)
        print(f"Data has been written to {path}")


def main():
    files = os.listdir("assets/")
    for file in os.listdir("assets/"):
        file_path = os.path.join("assets/", file)
        if os.path.isfile(file_path):
            if file_path == "assets/hinos.csv":
                continue

            with open(file_path, "r") as json_file:
                json_to_txt(
                    json.loads(json_file.read()),
                    os.path.join("assets/txt", file[:-5] + ".txt"),
                )


if __name__ == "__main__":
    main()
