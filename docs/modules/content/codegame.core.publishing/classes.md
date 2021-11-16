Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.core.publishing
No description
<br>
[functions (2)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.publishing/functions.md) &nbsp;.&nbsp; [classes (3)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.publishing/classes.md)


## Classes
```python
class Error(Exception):
    """
    Common base class for all non-exit exceptions.
    """

    # inherited from Exception
    def __init__(self, /, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """


    args = <attribute 'args' of 'BaseException' objects>
    
```

```python
class InvalidReleaseFormError(codegame.core.publishing.Error):
    """
    Common base class for all non-exit exceptions.
    """

    # inherited from Exception
    def __init__(self, /, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """


    args = <attribute 'args' of 'BaseException' objects>
    
```

```python
class ReleaseError(codegame.core.publishing.Error):
    """
    Common base class for all non-exit exceptions.
    """

    # inherited from Exception
    def __init__(self, /, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """


    args = <attribute 'args' of 'BaseException' objects>
    
```

