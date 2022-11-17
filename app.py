import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from config import STYLESHEET
from ui.gui import App


def main() -> None:
    stylesheet: str = Path(STYLESHEET).read_text()

    app = QApplication(sys.argv)
    win = App()

    win.setStyleSheet(stylesheet)
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
