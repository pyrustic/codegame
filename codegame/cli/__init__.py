import os
import os.path
from codegame.core import creator
from codegame.cli import remote_info
from shared import Jason
from codegame.game import open_preview, UndefinedLevel


HELP_TEXT = \
"""
Visit https://github.com/pyrustic/codegame

Command line interface
======================
- init: initialize the project directory
- info [remote|github-repository]: check the local or remote information
- preview [level]: open the rendered litemark file of this level
- build: build a distribution package
- publish: publish the latest build

Examples:
# show the number of downloads and stargazers for the project in the CWD
info remote

# show the number of downloads and stargazers for pyrustic/cgame-demo
info pyrustic/cgame-demo
info https://github.com/pyrustic/cgame-gemo

# show local info (author, version, ...)
info

# preview level 3
preview 3

# preview level 1
preview
preview 1

"""


def process(*args):
    """commands are: init, preview, build,
    publish, hub, help"""
    handlers = {"init": init, "preview": preview,
                "build": build, "publish": publish,
                "info": info, "help": print_help}
    command = args[0]
    try:
        handlers[command](*args[1:])
    except KeyError as e:
        print(MESSAGES["unknown"])


def init(*args):
    if args:
        print(MESSAGES["incorrect"])
        return
    root = os.getcwd()
    if creator.initialized(root):
        print("Already initialized !")
        return
    creator.init(root)
    # fill codegame.json
    _fill_codegame_config(root)
    # exit
    print("Successfully initialized !")


def info(*args):
    root = os.getcwd()
    if args:
        _show_remote_info(root, args[0])
        return
    if not creator.initialized(root):
        print(MESSAGES["uninitialized"])
        return
    jason = Jason("codegame.json", location=root)
    items = ("name", "version", "author", "email", "github", "description")
    for item in items:
        print("{}: {}".format(item, jason.data.get(item)))


def preview(*args):
    level = 1
    if args:
        try:
            level = int(args[0])
        except ValueError as e:
            print("The level should be an integer !")
            return
    root = os.getcwd()
    try:
        open_preview(root, level)
    except UndefinedLevel as e:
        print("Failed to load the level {}.".format(level))
        print("Undefined level !")
    except Exception as e:
        print("Failed to load the level {}.".format(level))


def build(*args):
    if args:
        print(MESSAGES["incorrect"])
        return
    root = os.getcwd()
    if not creator.initialized(root):
        print(MESSAGES["uninitialized"])
        return
    # latest build
    jason = Jason("build_report.json", location=root)
    if jason.data:
        cache = jason.data[0]
        if cache["release_timestamp"] is None:
            print("The latest build hasn't yet been released.")
            message = "Do you still want to make a new build ?"
            answer = creator.ask_for_confirmation(message, default="n")
            if not answer:
                return
    name = creator.build(root)
    print("Output: {}".format(name))
    print("Successfully built !")


def publish(*args):
    if args:
        print(MESSAGES["incorrect"])
        return
    root = os.getcwd()
    if not creator.initialized(root):
        print(MESSAGES["uninitialized"])
        return
    # latest build
    jason = Jason("build_report.json", location=root)
    if not jason.data or jason.data[0]["release_timestamp"] is not None:
        print("You need to build this codegame first !")
        return
    archive_name = jason.data[0]["dist"]
    archive = os.path.join(root, "dist", archive_name)
    if not os.path.isfile(archive):
        print("Missing codegame distribution package !")
        print("Please make a new build.")
        return
    # publishing
    data = creator.publish(root)
    meta_code = data["meta_code"]
    status_text = data["status_text"]
    status_code = data["status_code"]
    if meta_code == 0:
        print("Successfully published '{}' !".format(archive_name))
    else:
        print(status_code, status_text)
        if meta_code == 1:
            print("Failed to create release.")
        elif meta_code == 2:
            print("Failed to upload asset.")
        elif meta_code == 3:
            print("Failed to create the release form.")
        else:
            print("Unknown meta_code.")


def print_help(*args):
    print(HELP_TEXT)


MESSAGES = {"incorrect": "Incorrect command. Type 'help' !",
            "unknown": "Unknown command. Type 'help' !",
            "uninitialized": "Uninitialized codegame project. Type 'init' !"}


def _show_remote_info(root, url):
    if url == "remote":
        jason = Jason("codegame.json", location=root, readonly=True)
        if not jason.data:
            print("Missing 'codegame.json' config file !")
            return
        url = jason.data["github"]
    owner_repo = creator.extract_github_profile(url)
    if len(owner_repo) != 2:
        print("Incorrect GitHub Repository URL")
        return
    owner, repo = owner_repo
    print("https://github.com/{}/{}\n".format(owner, repo))
    kurl = creator.get_kurl()
    if not remote_info.show_repo_description(kurl, owner, repo):
        return
    if not remote_info.show_latest_release(kurl, owner, repo):
        return
    if not remote_info.show_latest_releases_downloads(kurl, owner, repo):
        return


def _fill_codegame_config(root):
    jason = Jason("codegame.json", location=root)
    items = ("author", "email", "description", "github")
    introduced = False
    for item in items:
        if not jason.data.get(item):
            if not introduced:
                print("Let's fill the config file 'codegame.json'")
                introduced = True
            cache = input("{}: ".format(item))
            jason.data[item] = cache
    if introduced:
        jason.save()
