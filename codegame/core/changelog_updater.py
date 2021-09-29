import os
import os.path
import time
from datetime import datetime


def get_date():
    """ Returns the current date. Format: Month day, year.
    Example: January 15, 2020
    """
    MONTHS = ("January", "February", "March", "April", "May",
              "June", "July", "August", "September", "October",
              "November", "December")
    dt = datetime.fromtimestamp(time.time())
    text = "{month} {day}, {year}".format(month=MONTHS[dt.month - 1],
                                          day=dt.day, year=dt.year)
    return text


def update_changelog(root, version):
    # cut LATEST_RELEASE.md content and then log it in CHANGELOG.md
    latest_release_path = os.path.join(root, "LATEST_RELEASE.md")
    try:
        with open(latest_release_path, "r+") as file:
            data = file.readlines()
            file.seek(0)
            file.write("")
            file.truncate()
    except Exception as e:
        return False
    changelog_path = os.path.join(root, "CHANGELOG.md")
    cache = "## Version {} of {}\n"
    data.insert(0, cache.format(version, get_date()))
    data.append("\n\n\n")
    data = "".join(data)
    try:
        with open(changelog_path, "r+") as file:
            cache = file.readlines()
            cache.insert(0, data)
            file.seek(0)
            file.write("".join(cache))
            file.truncate()
    except Exception as e:
        return False
    return True
