Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.game.testing
No description
<br>
[functions (6)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.game.testing/functions.md) &nbsp;.&nbsp; [classes (3)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.game.testing/classes.md)


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
class InvalidTest(codegame.game.testing.Error):
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
class Section(object):
    """
    
    """


    INPUT = "[INPUT]"
    
    META = "[META]"
    
    OUTPUT = "[OUTPUT]"
    
```

