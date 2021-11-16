import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import ScrollBox
from cyberpunk_theme.widget.button import get_button_blue_style, get_button_blue_filled_style


class IndexView(Viewable):

    def __init__(self, master, data, finale, on_open):
        super().__init__()
        self._master = master
        self._data = data
        self._finale = finale
        self._on_open = on_open
        self._strvar_description = tk.StringVar(value="Currently running")
        self._strvar_owner_repo = tk.StringVar(value="pyrustic/demo")
        self._strvar_tag_name = tk.StringVar(value="v10.0.2")
        self._strvar_published_on = tk.StringVar(value="January 21, 2021 at 12:20 UTC")
        self._strvar_created_on = tk.StringVar(value="March 14, 2021 at 09:10 UTC")
        self._strvar_stargazers_count = tk.StringVar(value="34")
        self._strvar_downloads_count = tk.StringVar(value="345")
        self._strvar_package_size = tk.StringVar(value="24 KB")
        self._image_cache = None
        self._scrollbox = None

    def _build(self):
        self._body = tk.Toplevel()
        self._body.geometry("500x350")
        self._body.title("Codegame Index")
        self._body.resizable(False, False)
        #self._body.overrideredirect(1)
        self._scrollbox = ScrollBox(self._body)
        self._scrollbox.pack(expand=1, fill=tk.BOTH)
        # install central
        self._install_central()
        # install footer
        self._install_footer()

    def _on_map(self):
        super()._on_map()

    def _on_destroy(self):
        pass

    def _install_central(self):
        # install identification frame
        for i, title in enumerate(self._data):
            level = i+1
            self._install_row_frame(level, title)

    def _install_row_frame(self, level, title):
        # frame
        frame = tk.Frame(self._scrollbox.box)
        frame.pack(fill=tk.X, padx=(3, 5), pady=5)
        # entry level-title
        if level == self._finale:
            cache = "Finale - {}".format(title)
        else:
            cache = "Level {} - {}".format(level, title)
        strvar = tk.StringVar(value=cache)
        entry = tk.Entry(frame, textvariable=strvar,
                         readonlybackground="#121519",
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        #get_info_entry_owner_repo_style().target(entry)
        # button
        command = (lambda level=level, self=self: self._on_click_open(level))
        button = tk.Button(frame, text="Open",
                           command=command)
        button.pack(side=tk.LEFT, padx=(5, 0))
        get_button_blue_style().target(button)

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=(15, 3))
        # button close
        button = tk.Button(frame, text="Close",
                           command=self.destroy)
        button.pack(side=tk.RIGHT)

    def _on_click_open(self, level):
        self._on_open(level)
        self.destroy()