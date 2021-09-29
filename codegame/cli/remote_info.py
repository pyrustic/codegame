from codegame.core import github_client


def show_repo_description(kurl, owner, repo):
    cache = github_client.repo_description(kurl, owner, repo)
    status_code, status_text, data = cache
    if status_code not in (200, 304):
        print("Failed to get the repo description")
        if status_code:
            print("{} {}".format(status_code, status_text))
        else:
            print(status_text)
        return False
    _show_section("Repository description")
    description = data["description"]
    description = "- No description -" if not description else description
    print(description)
    print("Created on {}".format(data["created_at"]))
    stargazers = data["stargazers_count"]
    subscribers = data["subscribers_count"]
    print("{} Stargazer{} and {} Subscriber{}".format(stargazers,
                                                      _plural(stargazers),
                                                      subscribers,
                                                      _plural(subscribers)))
    print("")
    return True


def show_latest_release(kurl, owner, repo):
    cache = github_client.latest_release(kurl, owner, repo)
    status_code, status_text, data = cache
    if status_code not in (200, 304):
        print("Failed to get the latest release info")
        if status_code:
            print("{} {}".format(status_code, status_text))
        else:
            print(status_text)
        return False
    _show_section("Latest release")
    print("Tag name: {}".format(data["tag_name"]))
    print("Published on {}".format(data["published_at"]))
    downloads = data["downloads_count"]
    print("{} Download{}".format(downloads,
                                 _plural(downloads)))
    print("")
    return True


def show_latest_releases_downloads(kurl, owner, repo):
    cache = github_client.latest_releases_downloads(kurl, owner, repo)
    status_code, status_text, data = cache
    if status_code not in (200, 304):
        print("Failed to get the latest ten (pre)releases info")
        if status_code:
            print("{} {}".format(status_code, status_text))
        else:
            print(status_text)
        return False
    _show_section("Latest ten (pre)releases")
    downloads = data
    print("{} Download{}".format(downloads,
                                 _plural(downloads)))
    print("")
    return True


def _show_section(title):
    count = len(title)
    print(title)
    print("".join(["=" for _ in range(count)]))


def _plural(item):
    item = int(item)
    return "s" if item > 1 else ""
