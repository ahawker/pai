# pai-lang

Language for describing resources/relations as shell-safe strings.

### Status

`pai-lang` is in alpha stage and not yet used by any production workloads.

### Installation

Install `pai-lang` using [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install pai_lang
```

Install `pai-lang` from source:
```bash
    $ git clone git@github.com:ahawker/pai_lang.git
    $ cd pai_lang
    $ python setup.py install
```

### Usage

`pai-lang` does not enforce any constraints on the `node`, `relation`, and `property` values.

For this example, lets imagine we're trying to describe a service that deals with:

* Users
* Workspaces
* Workspace Settings

Describe a single resource by its relation to a property value. In layman's terms:
"Resolve to a user with the email address foo@bar.com".

```python
    import pai_lang

    >>> pai_lang.parse('user:email:foo@bar.com')
    [<Node(node=user, edge=email, property=foo@bar.com>]
```

Describe two linked resources by a specific relation. In layman's terms:
"Resolve to a workspace (linked by workspace-id) to a user with the email address foo@bar.com"

```python
    import pai_lang

    >>> pai_lang.parse('workspace:workspace-id:user:email:foo@bar.com')
    [<Node(node=user, edge=email, property=foo@bar.com>,
     <Node(node=workspace, edge=workspace-id, property=None>]
```

Describe two linked resources by any relation. In layman's terms:
"Resolve a workspace (linked by any discoverable relation) to a user with the email address foo@bar.com".

```python
    import pai_lang

    >>> pai_lang.parse('workspace:any:user:email:foo@bar.com')
    [<Node(node=user, edge=email, property=foo@bar.com>,
     <Node(node=workspace, edge=any, property=None>]
```

Describe N (where N=3 in this example) resources by any relation. In layman's terms:
"Resolve the settings data (linked by any discoverable relation) to a workspace (linked by any discoverable relation) to a user with the email address foo@bar.com"

```python
    import pai_lang

    >>> pai_lang.parse('settings:any:workspace:any:user:email:foo@bar.com')
    [<Node(node=user, edge=email, property=foo@bar.com>,
     <Node(node=workspace, edge=any, property=None>,
     <Node(node=settings, edge=any, property=None>]
```


### License

[Apache 2.0](LICENSE)