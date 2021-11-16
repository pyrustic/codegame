Back to [Modules overview](https://github.com/pyrustic/codegame/blob/master/docs/modules/README.md)
  
# Module documentation
>## codegame.core.github\_client
No description
<br>
[functions (6)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.github_client/functions.md) &nbsp;.&nbsp; [classes (1)](https://github.com/pyrustic/codegame/blob/master/docs/modules/content/codegame.core.github_client/classes.md)


## Classes
```python
class Release(object):
    """
    
    """

    def __init__(self, kurl, owner, repo):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    def publish(self, name, tag_name, target_commitish, description, prerelease, draft, asset_path, asset_name, asset_label):
        """
        Return {"meta_code":, "status_code", "status_text", "data"}
        meta code:
            0- success
            1- failed to create release (check 'status_code', 'status_text')
            2- failed to upload asset (check 'status_code', 'status_text')
        """

    def _create_release(self, owner, repo, name, tag_name, target_commitish, description, prerelease, draft):
        """
        
        """

    def _upload_asset(self, upload_url, path, name, label):
        """
        
        """

```

