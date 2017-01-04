# pai-lang

[![Build Status](https://travis-ci.org/ahawker/pai-lang.svg?branch=master)](https://travis-ci.org/ahawker/pai-lang)
[![Coverage Status](https://coveralls.io/repos/github/ahawker/pai-lang/badge.svg?branch=master)](https://coveralls.io/github/ahawker/pai-lang?branch=master)
[![Code Climate](https://codeclimate.com/github/ahawker/pai-lang/badges/gpa.svg)](https://codeclimate.com/github/ahawker/pai-lang)
[![Issue Count](https://codeclimate.com/github/ahawker/pai-lang/badges/issue_count.svg)](https://codeclimate.com/github/ahawker/pai-lang)

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

### Deployment

Package deployments to index servers are automatically performed by [Travis CI](https://travis-ci.org/).

[PyPI](https://pypi.python.org/pypi/pai-lang) - Hosts **Official** Builds

[TestPyPI](https://testpypi.python.org/pypi/pai-lang) - Hosts **Development** Builds

Tagged versions of the `master` branch will be deployed to the official PyPI index server while non-tagged versions will be deployed
to the test PyPI index server.

To kick off a new, official deployment, just run one of the following:

**Patch** Version Release: Use this when you make backwards-compatible bug fixes.
```bash
    $ make push-patch
```

**Minor** Version Release: Use this when you add functionality in a backwards-compatible manner.
```bash
    $ make push-minor
```

**Major** Version Release: Use this when you make incompatible API changes.
```bash
    $ make push-major
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