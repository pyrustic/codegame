Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.cli.\_\_init\_\_
No description
<br>
[constants (2)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.cli.__init__/constants.md) &nbsp;.&nbsp; [functions (9)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.cli.__init__/functions.md)


## Constants
```python
HELP_TEXT = "
Visit https://github.com/pyrustic/codegame

Command line interface
======================
- init: initialize the project directory
- info [remote|github-repository]: check the local or remote information
- preview [level]: open the rendered litemark file of this level
- build: build a distribution package
- publish: publish the latest build

Examples:
# show the number of downloads and stargazers for the project in the CWD
info remote

# show the number of downloads and stargazers for pyrustic/cgame-demo
info pyrustic/cgame-demo
info https://github.com/pyrustic/cgame-gemo

# show local info (author, version, ...)
info

# preview level 3
preview 3

# preview level 1
preview
preview 1

"

MESSAGES = {'incorrect': "Incorrect command. Type 'help' !", 'unknown': "Unknown command. Type 'help' !", 'uninitialized': "Uninitialized codegame project. Type 'init' !"}

```

