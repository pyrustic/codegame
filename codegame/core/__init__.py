import os
import os.path
import uuid
import shutil
import subprocess
import sys
import time
from pathlib import PurePath
from zipfile import ZipFile
from codegame.misc import funcs
from tempfile import TemporaryDirectory
from codegame.misc import constant
from kurl import Kurl
from shared import Jason


def get_jason():
    """
    Returns the data jason object if it exists,
    else returns None
    The json file linked to this jason is located in 'codegames' directory
    """
    cache = os.path.join(constant.PYRUSTIC_DATA, "codegame")
    if not os.path.exists(os.path.join(cache, "meta.json")):
        return None
    jason = Jason("meta.json", location=cache)
    if not jason.data:
        return None
    path = jason.data.get("codegames")
    if not path:
        return None
    cache = os.path.join(path, "codegames.json")
    if not os.path.exists(cache):
        return None
    return Jason("codegames.json", default={}, location=path)


def should_init_codegame():
    if get_jason():
        return False
    return True


def init_codegame(path):
    """
    Initialize Codegame.

    Param:
        - path: absolute path in which the folder "codegames"
        will be created

    Return:
        A dict: {"error_code": int, "error": object, "root_dir": str}
        - The "error_code" is one of:
            0 = all right
            1 = failed to create "codegames" folder
        - "root_dir" is the absolute path to the folder "codegames".
        Example: init_codegame("/path/to/use") will return this "root_dir":
            "/path/to/use/codegames"
    """
    error_code = 0
    error = None
    root_dir = None
    data = {"error_code": error_code,
            "error": error,
            "root_dir": root_dir}
    # create codegames
    error, root_dir = _create_codegames_folder(path)
    if error is not None:
        data["error_code"] = 1
        data["error"] = error
        return data
    # register Codegame in PyrusticData
    _register_codegame_in_pyrustic_data(root_dir)
    data["root_dir"] = root_dir
    return data


def rate(kurl):
    """
    Get Rate Limit
    Return: status_code, status_text, data
    data = {"limit": int, "remaining": int}
    """
    target = "https://api.github.com"
    url = "{}/rate_limit".format(target)
    response = kurl.request(url)
    json = response.json
    status_code, status_text = response.status
    data = {}
    if status_code == 304:
        data = response.cached_response.json
    if (status_code in (200, 304)) and json:
        data["limit"] = json["resources"]["core"]["limit"]
        data["remaining"] = json["resources"]["core"]["remaining"]
    return status_code, status_text, data


def fetch(owner, repo, kurl):
    """ Fetch resource
    Param:
        - owner: str
        - repo: str
        - kurl: Kurl object

    Return:
        status_code, status_text, json_data
        Json_data: {"description": str, "stargazers": int,
                    "tag": str, "published_at": str,
                    "downloads": int, "size": int,
                    "repository": str, "owner_repo": str,
                    "assets": list}
    """
    # fetch repo description
    data = dict()
    data["owner_repo"] = "{}/{}".format(owner, repo)
    data["repository"] = "https://github.com/{}/{}".format(owner, repo)
    status_code, status_text, json = fetch_description(owner, repo, kurl)
    if status_code in (200, 304):
        data["description"] = json["description"]
        data["stargazers"] = json["stargazers_count"]
        status_code, status_text, json = fetch_latest_release(owner, repo, kurl)
        if status_code in (200, 304):
            data["tag"] = json["tag_name"]
            data["published_at"] = funcs.badass_iso_8601_date_parser(json["published_at"])
            data["assets"] = []
            for asset in json["assets"]:
                _, ext = os.path.splitext(asset["name"])
                if ext != ".zip":
                    continue
                cache = {"name": asset["name"],
                         "size": asset["size"],
                         "url": asset["browser_download_url"],
                         "download_count": asset["download_count"],
                         "content_type": asset["content_type"]}
                data["assets"].append(cache)
    return status_code, status_text, data


def useful_info(data):
    """ Return useful info in a dict. Return None if the dict data is empty """
    if not data:
        return None
    info = {"tag_name": data["tag_name"],
            "published_at": funcs.badass_iso_8601_date_parser(data["published_at"]),
            "assets": []}
    for asset in data["assets"]:
        cache = {"name": asset["name"],
                 "size": asset["size"],
                 "url": asset["browser_download_url"],
                 "created_at": funcs.badass_iso_8601_date_parser(asset["created_at"]),
                 "updated_at": funcs.badass_iso_8601_date_parser(asset["updated_at"]),
                 "uploader_login": asset["uploader"]["login"],
                 "download_count": asset["download_count"],
                 "content_type": asset["content_type"]}
        info["assets"].append(cache)
    return info


def download(name, url, kurl):
    """
    Download the resource (url) with kurl object
    Return a boolean is_success, error, and tempdata
    Tempdata: (tempdir, filename)
    """
    is_success = True
    error = None
    response = kurl.request(url)
    data = response.body
    if response.code == 304:
        if response.cached_response:
            data = response.cached_response.body
    if data is None:
        return None, "The server returned an empty body", None
    tempdir = None
    filename = None
    try:
        tempdir = TemporaryDirectory()
        filename = os.path.join(tempdir.name, name)
        with open(filename, "wb") as file:
            file.write(data)
    except Exception as e:
        error = e
        is_success = False
    tempdata = {"tempdir": tempdir, "filename": filename}
    return is_success, error, tempdata


def install(owner, repo, tempdata):
    """
    Install the cached codegame book
    Return bool is_success, error
    """
    is_success, error = _install(owner, repo, tempdata)
    if not is_success:
        return False, error
    jason = get_jason()
    owner_repo_str = "{}/{}".format(owner, repo)
    timestamp_install = int(time.time())
    jason.data[owner_repo_str] = timestamp_install
    jason.save()
    return True, None


def app_metadata(owner, repo):
    """ returns a dict with these keys:
        - "version", "description", "img", "timestamp"

    """
    owner_repo_str = "{}/{}".format(owner, repo)
    timestamp = get_jason().data.get(owner_repo_str)
    path = get_path(owner, repo)
    jason = Jason("codegame.json", location=path, readonly=True)
    version = ""
    description = ""
    repository = "https://github.com/{}".format(owner_repo_str)
    current_time = int(time.time())
    cache = current_time - timestamp
    updated_since = int(cache / (60 * 60 * 24))
    if jason.data:
        version = jason.data.get("version")
        description = jason.data.get("description")
    data = {"owner_repo": (owner, repo),
            "version": version,
            "description": description,
            "timestamp": timestamp,
            "repository": repository,
            "updated_since": updated_since}
    return data


def uninstall(owner, repo):
    """
    Uninstall an app by providing its owner and repo.
    Return bool is_success, error
    """
    is_success = None
    error = None
    codegames_path = get_jason().location
    owner_folder = os.path.join(codegames_path, owner)
    repo_folder = os.path.join(owner_folder, repo)
    # if the repo folder doesn't exist, return
    if not os.path.exists(repo_folder):
        return False, None
    cache = os.path.join(constant.PYRUSTIC_DATA, "trash")
    if not os.path.exists(cache):
        try:
            os.makedirs(cache)
        except Exception as e:
            return False, e
    while True:
        random_data = str(uuid.uuid4().hex)
        cache = os.path.join(cache, random_data)
        if not os.path.exists(cache):
            break
    is_success, error = _moveto(repo_folder, cache)
    if is_success:
        jason = get_jason()
        owner_repo_str = "{}/{}".format(owner, repo)
        if owner_repo_str in jason.data:
            del jason.data[owner_repo_str]
            jason.save()
    return is_success, error


def get_path(owner, repo, jason=None):
    """
    Use this to get the path to the app owner/repo
    Return a path string or None
    """
    if not jason:
        jason = get_jason()
    if not jason:
        return None
    path = os.path.join(jason.location, owner, repo)
    if os.path.exists(path):
        return path
    return None


def parse_owner_repo(val):
    data_splitted = val.split("/")
    if len(data_splitted) != 2:
        return None, None
    if data_splitted[0] == "":
        data_splitted[0] = data_splitted[1]
    elif data_splitted[1] == "":
        data_splitted[1] = data_splitted[0]
    owner, repo = data_splitted
    return owner, repo


def get_kurl():
    """
    Generate a Kurl object
    """
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "Pyrustic"}
    return Kurl(headers=headers)


def fetch_latest_release(owner, repo, kurl):
    target = "https://api.github.com"
    url = "{}/repos/{}/{}/releases/latest".format(target, owner, repo)
    response = kurl.request(url)
    json = response.json
    status_code, status_text = response.status
    if status_code == 304:
        json = response.cached_response.json
    return status_code, status_text, json


def fetch_description(owner, repo, kurl):
    target = "https://api.github.com"
    url = "{}/repos/{}/{}".format(target, owner, repo)
    response = kurl.request(url)
    json = response.json
    status_code, status_text = response.status
    if status_code == 304:
        json = response.cached_response.json
    return status_code, status_text, json


def normpath(target, path):
    purepath = PurePath(path)
    cache = os.path.join(target, *purepath.parts)
    return os.path.normpath(cache)


def _create_codegames_folder(parent_path):
    """
    parent_path is the absolute path in which the folder "codegames"
    will be created.
    return (error, root_dir)
    """
    codegames_path = os.path.join(parent_path, "codegames")
    if not os.path.exists(codegames_path):
        try:
            os.mkdir(codegames_path)
        except Exception as e:
            return e, codegames_path
    # initialize codegames Jason
    Jason("codegames.json", default={}, location=codegames_path)
    return None, codegames_path


def _register_codegame_in_pyrustic_data(codegames):
    location = os.path.join(constant.PYRUSTIC_DATA, "codegame")
    jason = Jason("meta.json", location=location)
    jason.data = {"codegames": codegames}
    jason.save()


def _install(owner, repo, tempdata):
    """
    Install the cached wheel file
    Return bool is_success, error
    """
    codegames = get_jason().location
    tempdir = tempdata["tempdir"]
    filename = tempdata["filename"]
    src = filename
    dest = os.path.join(codegames,
                        owner, repo)
    if not os.path.exists(dest):
        os.makedirs(dest)
    try:
        with ZipFile(src, "r") as zfile:
            zfile.extractall(dest)
    except Exception as e:
        return False, e
    finally:
        tempdir.cleanup()
    if not os.listdir(dest):
        return False, "Unknown error"
    return True, None


def _moveto(src, dest):
    """
    If the DEST exists:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        - /home/ocean (DEST)
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/lake
        - /home/ocean/lake/fish.txt
    Else IF the DEST doesn't exist:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/fish.txt


    Move a file or directory (src) to a destination folder (dest)
    """
    if not os.path.exists(src):
        return False, None
    try:
        shutil.move(src, dest)
    except Exception as e:
        return False, e
    return True, None
