from core.config import Config
from gui.app import App


if __name__ == "__main__":

    config = Config()

    app = App(config)

    app.run()