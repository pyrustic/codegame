import sys
from tkf import App
from codegame.misc.theme import get_theme
from codegame.view.base import Base
from codegame import cli


def gui():
    # The App
    app = App()
    # Set the title
    app.title = "Codegame Platform"
    # Geometry
    app.geometry = "660x610+0+0"
    # Resizable
    app.resizable = (False, True)
    # Set the theme
    app.theme = get_theme()
    # Set the view
    app.view = lambda app: Base(app)
    # Center the window
    app.center()
    # Lift off !
    app.start()


def main():
    if len(sys.argv) > 1:
        cli.process(*sys.argv[1:])
    else:
        gui()


if __name__ == "__main__":
    main()
