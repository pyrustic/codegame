import tkinter as tk
from viewable import Viewable


class Player(Viewable):
    def __init__(self, superview, host=None):
        super().__init__()
        self._superview = superview
        self._host = host if host else superview.host
        self._master = superview.body
        self._views = superview.views

    @property
    def superview(self):
        return self._superview

    @property
    def host(self):
        return self._host

    @property
    def views(self):
        return self._views

    def _build(self):
        self._body = tk.Frame(self._master)

    def _on_map(self):
        pass

    def _on_destroy(self):
        pass
