Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.core.github\_client
No description
<br>
[functions (6)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.github_client/functions.md) &nbsp;.&nbsp; [classes (1)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.github_client/classes.md)


## Functions
```python
def get_hub_url(res):
    """
    
    """

```

```python
def latest_release(kurl, owner, repo):
    """
    Returns: (status_code, status_text, data}
    data = {"tag_name": str, "published_at": date,
            "downloads_count": int}
    """

```

```python
def latest_releases_downloads(kurl, owner, repo, maxi=10):
    """
    Returns: (status_code, status_text, data}
    data = int, downloads count
    """

```

```python
def repo_description(kurl, owner, repo):
    """
    Returns: (status_code, status_text, data)
    data = {"created_at": date, "description": str,
            "stargazers_count": int, "subscribers_count": int}
    """

```

