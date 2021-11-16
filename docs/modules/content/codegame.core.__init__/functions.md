Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.core.\_\_init\_\_
No description
<br>
[functions (20)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.__init__/functions.md)


## Functions
```python
def app_metadata(owner, repo):
    """
    returns a dict with these keys:
    - "version", "description", "img", "timestamp"
    """

```

```python
def download(name, url, kurl):
    """
    Download the resource (url) with kurl object
    Return a boolean is_success, error, and tempdata
    Tempdata: (tempdir, filename)
    """

```

```python
def fetch(owner, repo, kurl):
    """
    Fetch resource
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

```

```python
def fetch_description(owner, repo, kurl):
    """
    
    """

```

```python
def fetch_latest_release(owner, repo, kurl):
    """
    
    """

```

```python
def get_jason():
    """
    Returns the data jason object if it exists,
    else returns None
    The json file linked to this jason is located in 'codegames' directory
    """

```

```python
def get_kurl():
    """
    Generate a Kurl object
    """

```

```python
def get_path(owner, repo, jason=None):
    """
    Use this to get the path to the app owner/repo
    Return a path string or None
    """

```

```python
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

```

```python
def install(owner, repo, tempdata):
    """
    Install the cached codegame book
    Return bool is_success, error
    """

```

```python
def normpath(target, path):
    """
    
    """

```

```python
def parse_owner_repo(val):
    """
    
    """

```

```python
def rate(kurl):
    """
    Get Rate Limit
    Return: status_code, status_text, data
    data = {"limit": int, "remaining": int}
    """

```

```python
def should_init_codegame():
    """
    
    """

```

```python
def uninstall(owner, repo):
    """
    Uninstall an app by providing its owner and repo.
    Return bool is_success, error
    """

```

```python
def useful_info(data):
    """
    Return useful info in a dict. Return None if the dict data is empty 
    """

```

