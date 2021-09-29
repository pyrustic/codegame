import os
import os.path
import pkgutil
import getpass
import time
from kurl import Kurl
from codegame.core import publishing
from codegame.core.changelog_updater import update_changelog
from zipfile import ZipFile
from shared import Jason


DEFAULT_CONFIG = {"name": None, "author": None,
                  "email": None, "description": None,
                  "github": None, "version": 1}


def initialized(root):
    elements = ["assets", "dist", "source",
                "README.md", "LATEST_RELEASE.md",
                "CHANGELOG.md", ".gitignore", "codegame.json"]
    for item in elements:
        path = os.path.join(root, item)
        if not os.path.exists(path):
            return False
    return True


def init(root):
    # create folder 'assets'
    path = os.path.join(root, "assets")
    if not os.path.isdir(path):
        os.mkdir(path)
    # create folder 'source'
    path = os.path.join(root, "source")
    if not os.path.isdir(path):
        os.mkdir(path)
    # create folder 'dist'
    path = os.path.join(root, "dist")
    if not os.path.isdir(path):
        os.mkdir(path)
    # create file 'README.md'
    path = os.path.join(root, "README.md")
    if not os.path.isfile(path):
        data = pkgutil.get_data("codegame.core",
                                "template/README.md")
        with open(path, "w") as file:
            file.write(data.decode("utf-8"))
    # create .gitignore
    path = os.path.join(root, ".gitignore")
    if not os.path.isfile(path):
        data = pkgutil.get_data("codegame.core",
                                "template/.gitignore")
        with open(path, "w") as file:
            file.write(data.decode("utf-8"))
    # create LATEST_RELEASE.md
    path = os.path.join(root, "LATEST_RELEASE.md")
    if not os.path.isfile(path):
        with open(path, "w") as file:
            pass
    # create CHANGELOG.md
    path = os.path.join(root, "CHANGELOG.md")
    if not os.path.isfile(path):
        with open(path, "w") as file:
            pass
    # create codegame.json
    jason = Jason("codegame.json", default=DEFAULT_CONFIG, location=root)
    if jason.new:
        jason.data["name"] = os.path.basename(root)
        jason.save()


def build(root):
    jason = Jason("codegame.json", location=root)
    current_version = jason.data.get("version", 1)
    files_to_zip = _get_files_to_zip(root)
    # correct github entry
    cache = extract_github_profile(jason.data.get("github"))
    if not cache:
        print("Please set the GitHub Repository URL in 'codegame.json' !")
        return
    github_name = cache[0]
    # codegame name
    codegame_name = jason.data.get("name")
    # new version
    new_version = current_version + 1
    # zipfile name
    name = "{name}_{version}_{github_name}.codegame.zip"
    name = name.format(name=codegame_name, version=current_version,
                       github_name=github_name)
    # zip
    _zip(root, name, files_to_zip, os.path.join(root, "dist"))
    # update config
    jason.data["version"] = new_version
    jason.save()
    # update build_report
    jason = Jason("build_report.json", location=root,
                  default=[])
    data = {"build_timestamp": int(time.time()), "dist": name,
            "version": current_version, "release_timestamp": None}
    jason.data.insert(0, data)
    jason.save()
    return name


def publish(root):
    """
    Return {"meta_code":, "status_code", "status_text", "data"}
    meta code:
        0- success
        1- failed to create release (check 'status_code', 'status_text')
        2- failed to upload asset (check 'status_code', 'status_text')
        3- failed to create the release form
    """
    kurl = get_kurl()
    form = get_release_form(root)
    if not form:
        return {"meta_code": 3, "status_code": None, "status_text": None}
    try:
        kurl.token = getpass.getpass("Your GitHub Token: ")
    except EOFError as e:
        return
    data = publishing.publish(form, kurl)
    if data["meta_code"] == 0:
        # update build_report.json
        jason = Jason("build_report.json", location=root)
        jason.data[0]["release_timestamp"] = int(time.time())
        jason.save()
        update_changelog(root, jason.data[0]["version"])
    return data


def ask_for_confirmation(message, default="y"):
    """
    Use this function to request a confirmation from the user.

    Parameters:
        - message: str, the message to display
        - default: str, either "y" or "n" to tell "Yes by default"
        or "No, by default".

    Returns: a boolean, True or False to reply to the request.

    Note: this function will append a " (y/N): " or " (Y/n): " to the message.
    """
    cache = "Y/n" if default == "y" else "y/N"
    user_input = None
    try:
        user_input = input("{} ({}): ".format(message, cache))
    except EOFError as e:
        pass
    if not user_input:
        user_input = default
    if user_input.lower() == "y":
        return True
    return False


def get_kurl():
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "codegame"}
    kurl = Kurl(headers=headers)
    return kurl


def get_release_form(root):
    form = {}
    owner_repo = _check_github_owner_repo(root)
    if not owner_repo:
        return
    jason = Jason("codegame.json", location=root)
    codegame_name = jason.data.get("name")
    jason = Jason("build_report.json", location=root)
    version = jason.data[0].get("version")
    asset_name = jason.data[0].get("dist")
    asset_path = os.path.join(root, "dist", asset_name)
    release_note_path = os.path.join(root, "LATEST_RELEASE.md")
    with open(release_note_path, "r") as file:
        release_note = file.read()
    if not release_note:
        release_note = "This is a `codegame` built with the [Codegame Platform](https://github.com/pyrustic/codegame)."
    form["owner"] = owner_repo[0]
    form["repository"] = owner_repo[1]
    form["release_name"] = "{} v{}".format(codegame_name, version)
    form["tag_name"] = "v{}".format(version)
    form["target_commitish"] = "master"
    form["description"] = release_note
    form["is_prerelease"] = False
    form["is_draft"] = False
    form["asset_name"] = asset_name
    form["asset_path"] = asset_path
    form["asset_label"] = "Download the codegame archive"
    return form


def _check_github_owner_repo(root):
    jason = Jason("codegame.json", location=root)
    github_profile = jason.data["github"]
    cache = extract_github_profile(github_profile)
    if not cache:
        print("Please set the GitHub Repository URL in 'codegame.json' !")
        return
    return cache


def _zip(root, name, files, destination):
    zip_filename = os.path.join(destination, name)
    with ZipFile(zip_filename, "w") as archive:
        for item in files:
            archive.write(item,
                          os.path.relpath(item, root))


def extract_github_profile(url):
    if not url:
        return None
    cache = url.replace("https://github.com/", "")
    cache = cache.split("/")
    return cache


def _get_files_to_zip(root):
    files_to_zip = []
    # add codegame.json
    path = os.path.join(root, "codegame.json")
    files_to_zip.append(path)
    # add README
    path = os.path.join(root, "README.md")
    files_to_zip.append(path)
    # add img.png
    path = os.path.join(root, "img.png")
    if os.path.isfile(path):
        files_to_zip.append(path)
    # add 'source' folder
    source_dir = os.path.join(root, "source")
    for item in os.listdir(source_dir):
        path = os.path.join(source_dir, item)
        if os.path.isfile(path):
            files_to_zip.append(path)
    # add 'assets' folder
    assets_dir = os.path.join(root, "assets")
    for directory, folders, files in os.walk(assets_dir):
        for item in files:
            path = os.path.join(directory, item)
            files_to_zip.append(path)
    return files_to_zip
