import tkinter as tk
from viewable import Viewable
from codegame.misc.theme import get_entry_description_style
from codegame.misc.theme import get_info_entry_owner_repo_style
from cyberpunk_theme.widget.button import get_button_style_9, get_button_style_4


class Information(Viewable):
    def __init__(self, superview, data=None):
        super().__init__()
        self._superview = superview
        self._host = superview.host
        self._data = data
        self._master = superview.body
        self._views = superview.views
        self._data = data
        self._strvar_description = tk.StringVar()
        self._strvar_owner_repo = tk.StringVar()
        self._strvar_version = tk.StringVar()
        self._strvar_updated_since = tk.StringVar()
        self._image_cache = None
        self._setup()

    def _build(self):
        self._body = tk.Toplevel(name="info_toplevel")
        self._body.title("Codegame information")
        self._body.resizable(False, False)
        #self._body.overrideredirect(1)
        # install header
        self._install_header()
        # install central
        self._install_central()
        # install footer
        self._install_footer()

    def _on_map(self):
        super()._on_map()

    def _on_destroy(self):
        pass

    def _install_header(self):
        # install image
        canvas = tk.Canvas(self._body, width=400, height=100,
                           highlightthickness=0, borderwidth=0,
                           bg="#121519")
        canvas.pack(fill=tk.BOTH, pady=(0,5))
        data = self._host.get_background_image()
        image = tk.PhotoImage(data=data)
        self._image_cache = image
        canvas.create_image(0, 0, image=image, anchor="nw")
        # description
        description = tk.Entry(self._body,
                               textvariable=self._strvar_description,
                               state="readonly")
        description.pack(fill=tk.X, padx=2)
        get_entry_description_style().target(description)

    def _install_central(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.BOTH, expand=1, padx=(2, 10), pady=(10, 30))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, pad=5)
        frame.rowconfigure(1, pad=5)
        frame.rowconfigure(2, pad=5)
        frame.rowconfigure(3, pad=5)
        # install identification frame
        self._install_identification_frame(frame)
        # install version text
        self._install_version_text(frame)
        # install updating frame
        self._install_updating_frame(frame)

    def _install_identification_frame(self, frame):
        # entry
        entry = tk.Entry(frame, textvariable=self._strvar_owner_repo,
                         state="readonly")
        entry.grid(row=0, column=0, sticky="we")
        get_info_entry_owner_repo_style().target(entry)
        # button
        command = (lambda self=self:
                   self._host.open_website(self._data["repository"]))
        button = tk.Button(frame, text="Repository",
                           command=command)
        button.grid(row=0, column=1, sticky="we")

    def _install_version_text(self, frame):
        subframe = tk.Frame(frame)
        subframe.grid(row=1, column=0, sticky="we")
        label = tk.Label(subframe, text="Version:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(subframe, textvariable=self._strvar_version,
                         state="readonly")
        entry.pack(side=tk.LEFT, expand=1, fill=tk.X)
        #entry.grid(row=1, column=0, sticky="we")

    def _install_updating_frame(self, frame):
        # entry
        entry = tk.Entry(frame, textvariable=self._strvar_updated_since,
                         state="readonly")
        entry.grid(row=2, column=0, sticky="we")
        # button
        button = tk.Button(frame, text="Update",
                           command=self._on_click_update)
        button.grid(row=2, column=1, sticky="we")

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=3)
        # button uninstall
        button_uninstall = tk.Button(frame, text="Uninstall",
                                     command=self._on_click_uninstall)
        button_uninstall.pack(side=tk.LEFT)
        get_button_style_9().target(button_uninstall)
        # button run
        button_run = tk.Button(frame, text="Run",
                                 command=self._on_click_run)
        button_run.pack(side=tk.RIGHT, padx=(3, 0))
        get_button_style_4().target(button_run)
        # button close
        button_close = tk.Button(frame, text="Close",
                                 command=self.destroy)
        button_close.pack(side=tk.RIGHT, padx=(10, 0))

    def _setup(self):
        # populate
        self._strvar_description.set(self._data["description"])
        owner_repo = self._data["owner_repo"]
        cache = "/".join(owner_repo)
        self._strvar_owner_repo.set(cache)
        self._strvar_version.set(self._data["version"])
        updated_since = self._data["updated_since"]
        if updated_since >= 1000:
            cache = "Updated since 999+ days ago"
        elif updated_since > 1:
            cache = "Updated since {} days ago".format(updated_since)
        else:
            cache = "Updated recently"
        self._strvar_updated_since.set(cache)

    def _on_click_update(self):
        owner_repo = self._data["owner_repo"]
        owner, repo = owner_repo
        self.destroy()
        self._host.find_online(owner, repo)

    def _on_click_run(self):
        owner_repo = self._data["owner_repo"]
        self.destroy()
        self._host.run_codegame(owner_repo)

    def _on_click_uninstall(self):
        owner_repo = self._data["owner_repo"]
        owner, repo = owner_repo
        self.destroy()
        self._superview.show_toast("Uninstalling...", duration=None)
        self._host.uninstall(owner, repo)
