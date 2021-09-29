import os
import os.path
import tkinter as tk
import litemark
from tkinter.scrolledtext import ScrolledText
from codegame.game.editor import Editor
from viewable import Viewable
from codegame.misc.theme import get_entry_title_style,\
    get_button_lite_style, get_entry_level_style,\
    get_button_solve_me_style, get_button_next_level_style
from codegame.game.indexview import IndexView
from codegame.game import testing
from shared import Jason
from codegame.game.indexview import IndexView
from codegame.misc.theme import get_theme
from tkutil import center_window


class Game(Viewable):
    def __init__(self, master, target, preview=True, home_callback=None):
        super().__init__()
        self._master = master
        self._target = target
        self._level = None
        self._preview = preview
        self._home_callback = home_callback
        self._title_strvar = tk.StringVar()
        self._level_strvar = tk.StringVar()
        self._scrolledtext = None
        self._levels = []
        self._level = None
        self._tests = []
        self._viewer = None
        self._filename = None
        self._codegame_jason = None
        self._solved = False
        self._setup()

    def open(self, level):
        try:
            self._title, file = self._levels[level-1]
        except IndexError:
            raise UndefinedLevel
        self._level = level
        self._filename = os.path.join(self._target, "source", file)
        self._update_header()
        with open(self._filename, "r") as file:
            data = file.read()
        tokens = litemark.scan(data)
        tests = self._extract_tests(tokens)
        self._tests = self._formalize_tests(tests)
        self._viewer = litemark.Viewer(self._scrolledtext, root=self._target,
                                 style=litemark.get_default_style())
        self._viewer.render(tokens, ignore="codegame-test")
        self._add_button_solve_me()
        self._viewer.readonly = True
        self._solved = False

    def _setup(self):
        levels = self._extract_levels()
        progression = self._get_codegame_jason().data.get("progression")
        if self._preview:
            progression = len(levels)
        self._levels = levels
        self._progression = progression

    def _build(self):
        self._body = tk.Frame(self._master, bg="white")
        self._install_header()
        self._install_reader()

    def _on_map(self):
        pass

    def _on_destroy(self):
        pass

    def _install_header(self):
        frame = tk.Frame(self._body, bg="#F8F6FF")
        frame.pack(fill=tk.X, ipady=3)
        # level entry
        self._entry_level = tk.Entry(frame, state="readonly",
                               textvariable=self._level_strvar)
        self._entry_level.pack(side=tk.LEFT, ipady=1)
        get_entry_level_style().target(self._entry_level)
        # level title entry
        entry_title = tk.Entry(frame, state="readonly",
                               textvariable=self._title_strvar)
        entry_title.pack(side=tk.LEFT, fill=tk.X, ipady=1, expand=1)
        get_entry_title_style().target(entry_title)
        # button index
        about_button = tk.Button(frame, text="Index",
                                 bg="#EBE9F2", highlightbackground="#8698C0",
                                 foreground="#8698C0",
                                 command=self._on_click_index)
        about_button.pack(side=tk.LEFT, padx=1)
        get_button_lite_style().target(about_button)
        if self._home_callback:
            # button Home
            home_button = tk.Button(frame, text="Home",
                                     command=self._home_callback)
            home_button.pack(side=tk.RIGHT, padx=1)
            get_button_lite_style().target(home_button)

    def _install_reader(self):
        self._scrolledtext = ScrolledText(self._body, bg="white",
                                          padx=5,
                                          wrap="word",
                                          spacing2=3, spacing3=3,
                                          selectbackground="#F0F0F0",
                                          selectforeground="#606060")
        self._scrolledtext.pack(fill=tk.BOTH, expand=1, padx=(0, 0))
        self._scrolledtext.vbar.config(activebackground="#DADADA",
                                       background="#F0F0F0",
                                       highlightbackground="white",
                                       highlightcolor="white",
                                       troughcolor="white")

    def _on_click_index(self):
        if not self._preview and not self._progression:
            return
        if self._preview:
            data = [x[0] for x in self._levels]
        else:
            maxlimit = 1 if self._progression is None else self._progression
            data = [self._levels[x][0] for x in range(maxlimit)]
        on_open = lambda level, self=self: self.open(level)
        index_view = IndexView(self._body, data, len(self._levels), on_open)
        index_view.build()

    def _extract_levels(self):
        source = os.path.join(self._target, "source")
        files = []
        cache = os.listdir(source)
        cache.sort()
        for item in cache:
            if item == "index.json":
                continue
            files.append(item)
        jason = Jason("index.json", location=source, readonly=True)
        levels = []
        for i, file in enumerate(files):
            try:
                title = jason.data[i]
            except Exception as e:
                title = file
            cache = (title, file)
            levels.append(cache)
        return levels

    def _extract_tests(self, tokens):
        cache = []
        for token in tokens:
            if token.name == litemark.Element.CODEBLOCK:
                if token.data[0] == "codegame-test":
                    cache.append(token.data[1])
        return cache

    def _update_header(self):
        if self._level == len(self._levels):
            cache = "Finale :"
        else:
            cache = "Level {}:".format(self._level)
        self._level_strvar.set(cache)
        self._title_strvar.set(self._title)
        self._entry_level.config(width=len(cache))

    def _formalize_tests(self, tests):
        cache = []
        for test in tests:
            cache.append(testing.parse_test(test))
        return cache

    def _add_button_solve_me(self):
        if not self._tests:
            return
        self._viewer.readonly = False
        command = lambda self=self: self._on_click_button_solve_me()
        button_solve_me = tk.Button(self._viewer.widget, text="SOLVE ME !",
                                    command=command)
        get_button_solve_me_style().target(button_solve_me)
        self._viewer.widget.insert(tk.END, "\n")
        self._viewer.widget.window_create(tk.END, window=button_solve_me)
        self._viewer.widget.insert(tk.END, " ")

    def _add_button_next_level(self):
        if self._level == len(self._levels):
            return
        if self._solved:
            return
        self._solved = True
        self._viewer.readonly = False
        command = lambda self=self: self._on_click_button_next_level()
        button_next_level = tk.Button(self._viewer.widget, text="NEXT LEVEL",
                                      command=command)
        get_button_next_level_style().target(button_next_level)
        self._viewer.widget.window_create(tk.END, window=button_next_level)

    def _on_click_button_solve_me(self):
        editor = Editor(self._master, self._tests,
                        on_success=self._on_success)
        editor.build()

    def _on_click_button_next_level(self):
        self.open(self._level+1)

    def _get_codegame_jason(self):
        if not self._codegame_jason:
            self._codegame_jason = Jason("codegame.json", location=self._target)
        return self._codegame_jason

    def _on_success(self):
        self._add_button_next_level()
        if self._preview:
            return
        jason = self._get_codegame_jason()
        if self._progression is None:
            jason.data["progression"] = 1
            self._progression = self._level
            jason.save()
            return
        if self._progression < self._level:
            jason.data["progression"] = self._level
            jason.save()
            self._progression = self._level


class Error(Exception):
    pass


class UndefinedLevel(Error):
    pass


def open_preview(root, level):
    gui = tk.Tk()
    codegame_name = os.path.basename(root)
    title = "{} {} (Preview) | Codegame Platform".format(codegame_name, level)
    gui.title(title)
    gui.geometry("660x610+0+0")
    center_window(gui)
    get_theme().target(gui)
    game = Game(gui, root)
    game.build_pack(fill=tk.BOTH, expand=1)
    game.open(level)
    gui.mainloop()
