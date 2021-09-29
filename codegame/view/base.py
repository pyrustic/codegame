import tkinter as tk
from viewable import Viewable
from megawidget.toast import Toast
from codegame.host import Host
from codegame.view.about import About
from codegame.view.home import Home
from codegame.view.information import Information
from codegame.view.installer import Installer
from codegame.game import Game


class Base(Viewable):
    def __init__(self, app):
        super().__init__()
        self._app = app
        self._host = None
        self._master = app.root
        self._views = []
        self._home = None
        self._toast = None
        self._game = None
        self._setup()

    @property
    def app(self):
        return self._app

    @property
    def root(self):
        return self._master

    @property
    def host(self):
        return self._host

    @property
    def views(self):
        return self._views

    @property
    def home(self):
        return self._home

    def open_about(self):
        about = About(self)
        about.build()

    def open_home(self, data=None):
        if not self._home:
            self._home = Home(self, data=data)
        if self._game:
            self._game.body.pack_forget()
        self._home.build_pack(expand=1, fill=tk.BOTH)

    def update_home(self, data):
        if not self._home:
            return
        self._home.populate(data)

    def open_codegame(self, path, level):
        if not self._game:
            self._game = Game(self._body, path, preview=False,
                              home_callback=self._on_open_home)
        if self._home:
            self._home.body.pack_forget()
        self._game.build_pack(fill=tk.BOTH, expand=1)
        self._game.open(level)

    def open_information(self, data=None):
        information = Information(self, data=data)
        information.build()

    def open_installer(self, data=None):
        installer = Installer(self, data=data)
        installer.build()

    def show_toast(self, message, duration=1234):
        self.close_toast()
        toast = Toast(self._app.root, message=message,
                      duration=duration)
        toast.update_idletasks()
        if duration is None:
            self._toast = toast

    def close_toast(self):
        if self._toast:
            self._toast.destroy()
            self._toast = None

    def exit(self):
        self._app.root.destroy()

    def _build(self):
        self._body = tk.Frame(self._master)

    def _on_map(self):
        if not self._host.initialized:
            self.open_about()
        else:
            self._on_open_home()

    def _on_destroy(self):
        pass

    def _setup(self):
        self._host = Host(self)

    def _on_open_home(self):
        data = self._host.get_codegames_list()
        self.open_home(data)