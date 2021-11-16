import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import ScrollBox
from megawidget.toast import Toast
from codegame.misc.theme import get_highlight_style, get_unhighlight_style
from suggestion import Suggestion, Engine
from codegame.misc.theme import get_text_search_style
from codegame.misc import constant


MAX_TILES_BY_ROW = 3


class Home(Viewable):
    def __init__(self, superview, host=None, data=None):
        super().__init__()
        self._superview = superview
        self._host = host if host else superview.host
        self._data = data
        self._master = superview.body
        self._views = superview.views
        self._frame_matrix = None
        self._frame_row_cache = None  # will hold: [tk_frame, int_children_count]
        self._image_cache = {}
        self._sorted_by_owner = False
        self._search_strvar = tk.StringVar()

    @property
    def superview(self):
        return self._superview

    @property
    def host(self):
        return self._host

    @property
    def views(self):
        return self._views

    def populate(self, data):
        self._clear_frame_matrix()
        if not data:
            #Toast(self._body, message="No data available")
            return
        self._frame_row_cache = None
        self._image_cache = {}
        self._loop(data, 0)

    def _build(self):
        self._body = tk.Frame(self._master)
        self._install_header()
        self._install_pane()

    def _on_map(self):
        self._link_suggestion()
        self._entry_search.bind("<Return>",
                                lambda e, self=self: self._on_search(), "+")
        if self._data:
            self.populate(self._data)

    def _on_destroy(self):
        pass

    def _install_header(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, pady=(2, 10), padx=2)
        # Search:
        strvar = tk.StringVar(value="Search:")
        entry = tk.Entry(frame, width=7, textvariable=strvar, borderwidth=1,
                         state="readonly", cursor="hand1")
        entry.pack(side=tk.LEFT, ipady=1)
        entry.bind("<Button-1>", lambda e, self=self: self._on_search())
        get_text_search_style().target(entry)
        # search entry
        self._entry_search = tk.Entry(frame,
                                      textvariable=self._search_strvar)
        self._entry_search.pack(side=tk.LEFT, fill=tk.X, ipady=1,
                                expand=1, anchor="center")
        self._entry_search.focus_set()
        # button About
        about_button = tk.Button(frame, text="About",
                                 command=self._on_click_about)
        about_button.pack(side=tk.RIGHT, padx=(2, 0))

    def _install_pane(self):
        self._scrollbox = ScrollBox(self._body)
        self._scrollbox.pack(expand=1, fill=tk.BOTH)
        self._frame_matrix = tk.Frame(self._scrollbox.box)
        self._frame_matrix.pack(fill=tk.BOTH, expand=1)

    def _loop(self, data, index):
        if index == len(data):
            return
        owner, repo = data[index]
        self._populate(owner, repo)
        index += 1
        command = (lambda self=self, data=data, index=index:
                    self._loop(data, index))
        self._body.after(0, command)

    def _populate(self, owner, repo):
        if self._frame_row_cache is None:
            self._add_frame_row()
        elif self._frame_row_cache[1] == MAX_TILES_BY_ROW:
            self._add_frame_row()
        frame_row = self._frame_row_cache[0]
        children_count = self._frame_row_cache[1]
        self._add_tile(frame_row, owner, repo)
        self._frame_row_cache[1] = children_count + 1

    def _clear_frame_matrix(self):
        if self._frame_matrix:
            self._frame_matrix.destroy()
        self._frame_matrix = tk.Frame(self._scrollbox.box)
        self._frame_matrix.pack(fill=tk.BOTH, expand=1)

    def _add_frame_row(self):
        frame = tk.Frame(self._frame_matrix)
        frame.pack(fill=tk.X, padx=6)
        self._frame_row_cache = [frame, 0]

    def _add_tile(self, frame_row, owner, repo):
        tile = tk.Frame(frame_row)
        tile.pack(side=tk.LEFT, padx=3, pady=(0, 6))
        #tile.config(highlightthickness=2)
        #tile.config(highlightbackground="white")
        get_unhighlight_style().target(tile)
        # owner name
        entry_owner = tk.Entry(tile,borderwidth=0,width=0,
                               name="entry_owner_name",
                               cursor="hand1")
        entry_owner.pack(anchor="center", fill=tk.X,
                         padx=2, pady=(2, 1))
        entry_owner.insert(0, owner)
        entry_owner.config(state="readonly", cursor="hand1")
        # canvas
        canvas = tk.Canvas(tile, width=200, height=80,
                           highlightthickness=0, borderwidth=0,
                           cursor="hand1")
        canvas.pack(padx=2, pady=1, fill=tk.BOTH, expand=1)
        self._set_image(canvas, owner, repo)
        # repo name
        entry_repo = tk.Entry(tile, borderwidth=0, width=0,
                              name="entry_repo_name",
                              cursor="hand1")
        entry_repo.pack(anchor="w", fill=tk.X,
                        padx=2, pady=(0, 2), ipady=2)
        entry_repo.insert(0, repo)
        entry_repo.config(state="readonly")
        # binding
        self._bind_handler_owner(owner, tile, entry_owner)
        self._bind_handler_canvas(owner, repo, tile, canvas)
        self._bind_handler_repo(owner, repo, tile, entry_repo)

    def _set_image(self, canvas, owner, repo):
        self.body.update_idletasks()
        owner_repo = owner, repo
        data = self._host.get_codegame_image(owner_repo)
        if not data:
            return
        image = tk.PhotoImage(data=data)
        #image.zoom(25)
        #image = image.subsample(3, 3)
        self._image_cache["{}/{}".format(owner, repo)] = image
        canvas.create_image(0, 0, image=image, anchor="nw")

    def _bind_handler_owner(self, owner, tile, entry_owner):
        # on click
        command = (lambda event, self=self, owner=owner:
                   self._on_click_owner(owner))
        entry_owner.bind("<Button-1>", command, "+")
        # on enter
        command = (lambda event, tile=tile:
                   get_unhighlight_style().target(tile))
        entry_owner.bind("<Enter>", command, "+")
        # on leave
        entry_owner.bind("<Leave>", command, "+")

    def _bind_handler_canvas(self, owner, repo, tile, canvas):
        # handle Click on Canvas
        command = (lambda event, self=self, owner=owner,
                          repo=repo:
                   self._on_click_canvas(owner, repo))
        canvas.bind("<Button-1>", command)
        # handle on enter Canvas
        command = (lambda event, tile=tile:
                   get_highlight_style().target(tile))
        canvas.bind("<Enter>", command, "+")
        # handle on leave Canvas
        command = (lambda event, tile=tile:
                   get_unhighlight_style().target(tile))
        canvas.bind("<Leave>", command, "+")

    def _bind_handler_repo(self, owner, repo, tile, entry_repo):
        command_entry = (lambda event, self=self, owner=owner, repo=repo:
                         self._on_click_repo(owner, repo))
        # on click
        entry_repo.bind("<Button-1>", command_entry)
        # on enter
        command = (lambda event, tile=tile:
                   get_unhighlight_style().target(tile))
        entry_repo.bind("<Enter>", command, "+")
        # on leave
        entry_repo.bind("<Leave>", command, "+")

    def _on_click_owner(self, owner):
        self._sorted_by_owner = not self._sorted_by_owner
        data = self._host.get_codegames_list(self._sorted_by_owner)
        self.populate(data)

    def _on_click_canvas(self, owner, repo):
        self._host.run_codegame((owner, repo))

    def _on_click_repo(self, owner, repo):
        owner_repo = (owner, repo)
        data = self._host.get_info(owner_repo)
        self._superview.open_information(data)

    def _on_click_about(self):
        self._superview.open_about()
        self._search_strvar.set("")

    def _link_suggestion(self):
        owners_repos = self._host.get_codegames_list()
        suggestion = Suggestion(self._entry_search)
        self._suggestion_engine = SuggestionEngine(suggestion,
                                                   owners_repos=owners_repos)
        suggestion.engine = self._suggestion_engine

    def _on_search(self):
        search = self._search_strvar.get()
        search = search.strip()
        github_prefix = "https://github.com/"
        if search.startswith(github_prefix):
            search = search.replace(github_prefix, "")
            search = search.strip("/")
        owner_repo = search.split("/")
        if len(owner_repo) != 2:
            return
        self._search_strvar.set("")
        self._host.find(owner_repo)


class SuggestionEngine(Engine):
    def __init__(self, suggestion, owners_repos=None):
        self._suggestion = suggestion
        self._owners_repos = None
        self._owners = None
        self._prepare_dataset(owners_repos=owners_repos)
        self._setup()

    @property
    def owners_repos(self):
        return self._owners_repos

    @owners_repos.setter
    def owners_repos(self, val):
        self._prepare_dataset(owners_repos=val)

    def process(self, info, callback):
        if info.special_word:
            return
        word = info.word
        cache = []
        for owner, repo in self._owners_repos:
            if word in owner or word in repo:
                cache.append("{}/{}".format(owner, repo))
        callback(cache)

    def _setup(self):
        self._owners_repos = (self._owners_repos if self._owners_repos
                              else ())
        self._owners = (self._owners if self._owners
                        else ())

    def _basic_search(self, word, dataset):
        cache = []
        for item in dataset:
            if word in item:
                cache.append(item)
        return cache

    def _prepare_dataset(self, owners_repos=None):
        if owners_repos is not None:
            self._owners_repos = owners_repos
            self._owners = [owner for owner, repo in owners_repos]


class Dataset:
    def __init__(self):
        self.owners_repos = None
        self.commands = None
