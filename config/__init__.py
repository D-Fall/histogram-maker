from pathlib import Path

DATA = "./data.json"
STYLESHEET = Path.cwd().joinpath("./styles.css")
DATA_TEMPLATE = {
    "file": "",
    "column": "",
    "amount": "",
    "bins": "",
    "imgname": "histogram",
}
