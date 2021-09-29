import pkgutil
import os
import os.path
import webbrowser
from shared import Jason
from codegame.misc import constant
from codegame import core


class Host:
    def __init__(self, base):
        self._base = base
        self._root = base.root
        self._views = base.views
        self._images = {}
        self._app = base.app
        self._initialized = None
        self._quota = None
        self._kurl = core.get_kurl()
        self._count_processes = 0
        self._processes = list()

    @property
    def initialized(self):
        return not core.should_init_codegame()

    def initialize(self, path):
        cache = core.init_codegame(path)
        if cache["error_code"] == 1:
            self._base.show_toast("Failed to initialize Codegame App")
            self._base.exit()
            return
        data = self.get_codegames_list()
        self._base.open_home(data)

    def run_codegame(self, owner_repo):
        owner, repo = owner_repo
        path = core.get_path(owner, repo)
        jason = Jason("codegame.json", location=path)
        progression = jason.data.get("progression")
        level = 1
        if progression:
            level = progression + 1
        self._base.open_codegame(path, level)

    def find(self, owner_repo):
        owner, repo = owner_repo
        path = core.get_path(owner, repo)
        if path:
            data = self.get_info(owner_repo)
            self._base.open_information(data)
        else:
            self.find_online(*owner_repo)

    def find_online(self, owner, repo):
        self._base.show_toast("Fetching...", duration=None)
        # update quota
        updated, status_text = self._update_quota()
        if not updated:
            self._base.show_toast("Check your connection")
            return
        # check rate
        if self._quota - 2 == 0:
            message = "You are reaching the quota limit !\nPlease try in a few minutes"
            self._base.show_toast(message)
            return
        # open download pane
        cache = core.fetch(owner, repo, self._kurl)
        code, error, data = cache
        self._base.close_toast()
        if code in (200, 304):
            self._quota -= 2
            self._base.open_installer(data)
        else:
            self._base.show_toast(error)

    def get_info(self, owner_repo):
        return core.app_metadata(*owner_repo)

    def install(self, owner, repo, name, url):
        message = "Installation..."
        self._base.show_toast(message, duration=None)
        if core.get_path(owner, repo):
            is_success, error = core.uninstall(owner, repo)
            if not is_success:
                self._base.show_toast("Failed to uninstall previous version !")
                return
        # download
        is_success, error, tempfile = core.download(name, url, self._kurl)
        if not is_success:
            self._base.show_toast("Failed to download the asset !")
            return
        # install
        is_success, error = core.install(owner, repo, tempfile)
        if not is_success:
            self._base.show_toast("Failed to install the asset !")
            return
        # update the list of apps
        message = "Successfully installed '{}/{}' !".format(owner, repo)
        self._base.show_toast(message)
        self._base.update_home(self.get_codegames_list())

    def uninstall(self, owner, repo):
        is_success, error = core.uninstall(owner, repo)
        message = "Successfully uninstalled !"
        if not is_success:
            message = "Failed to uninstall"
        self._base.show_toast(message)
        self._base.update_home(self.get_codegames_list())

    def open_website(self, url):
        command = lambda: webbrowser.open(url, new=2)
        self._root.after(1, command)

    def get_codegames_list(self, sort_by_owner=False):
        jason = core.get_jason()
        data = []
        for owner_repo_str in jason.data.keys():
            owner, repo = core.parse_owner_repo(owner_repo_str)
            data.append((owner, repo))
        return data

    def get_codegame_index(self, owner_repo):
        # level, title, completed
        return [(("level 1", "title"), True), ]

    def get_codegame_to_solve(self, owner_repo):
        return None

    def get_codegame_litemark(self, owner_repo, level):
        pass

    def get_background_image(self):
        try:
            data = self._images["background"]
        except KeyError as e:
            data = pkgutil.get_data("codegame",
                                    "asset/background.png")
            self._images["background"] = data
        return data

    def get_default_image(self):
        try:
            data = self._images["default"]
        except KeyError as e:
            data = pkgutil.get_data("codegame",
                                    "asset/default_img.png")
            self._images["default"] = data
        return data

    def get_codegame_image(self, owner_repo):
        path = core.get_path(*owner_repo)
        img_path = os.path.join(path, "img.png")
        if not os.path.isfile(img_path):
            return self.get_default_image()
        with open(img_path, "rb") as file:
            data = file.read()
        owner_repo_str = "{}/{}".format(*owner_repo)
        self._images[owner_repo_str] = data
        return data

    def get_codegames_directory(self):
        if not self.initialized:
            return os.path.expanduser("~")
        location = os.path.join(constant.PYRUSTIC_DATA, "codegame")
        jason = Jason("meta.json", location=location, readonly=True)
        return os.path.dirname(jason.data.get("codegames"))


    def _update_quota(self):
        if self._quota:
            return True, None
        status_code, status_text, data = core.rate(self._kurl)
        updated = False
        if status_code in (200, 304):
            self._quota = data["remaining"]
            updated = True
        return updated, status_text
