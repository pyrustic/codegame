Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.core.creator
No description
<br>
[constants (1)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.creator/constants.md) &nbsp;.&nbsp; [functions (11)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.creator/functions.md)


## Functions
```python
def ask_for_confirmation(message, default='y'):
    """
    Use this function to request a confirmation from the user.
    
    Parameters:
        - message: str, the message to display
        - default: str, either "y" or "n" to tell "Yes by default"
        or "No, by default".
    
    Returns: a boolean, True or False to reply to the request.
    
    Note: this function will append a " (y/N): " or " (Y/n): " to the message.
    """

```

```python
def build(root):
    """
    
    """

```

```python
def extract_github_profile(url):
    """
    
    """

```

```python
def get_kurl():
    """
    
    """

```

```python
def get_release_form(root):
    """
    
    """

```

```python
def init(root):
    """
    
    """

```

```python
def initialized(root):
    """
    
    """

```

```python
def publish(root):
    """
    Return {"meta_code":, "status_code", "status_text", "data"}
    meta code:
        0- success
        1- failed to create release (check 'status_code', 'status_text')
        2- failed to upload asset (check 'status_code', 'status_text')
        3- failed to create the release form
    """

```

