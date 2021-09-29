from codegame.core import github_client


def publish(form, kurl):
    # publish
    try:
        data = _publish(form, kurl)
    except Exception as e:
        raise ReleaseError
    return data


def _publish(form, kurl):
    owner = form.get("owner")
    repository = form.get("repository")
    release_name = form.get("release_name")
    tag_name = form.get("tag_name")
    target_commitish = form.get("target_commitish")
    description = form.get("description")
    prerelease = form.get("is_prerelease")
    draft = form.get("is_draft")
    asset_name = form.get("asset_name")
    asset_path = form.get("asset_path")
    asset_label = form.get("asset_label")
    if (not release_name or not tag_name
            or not asset_path or not owner or not repository):
        raise InvalidReleaseFormError
    github_release = github_client.Release(kurl, owner, repository)
    data = github_release.publish(release_name, tag_name,
                                  target_commitish, description,
                                  prerelease, draft,
                                  asset_path, asset_name, asset_label)
    return data


class Error(Exception):
    pass


class ReleaseError(Error):
    pass


class InvalidReleaseFormError(Error):
    pass
