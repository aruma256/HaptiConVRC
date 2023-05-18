from pathlib import Path


SOURCE = Path("licenses.txt")
TARGET = Path("hapticonvrc") / Path("app.py")


with open(SOURCE, "r", encoding="utf-8") as f:
    license_text = f.read()

with open(TARGET, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace(r"{PLACEHOLDER}", license_text)

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(code)
