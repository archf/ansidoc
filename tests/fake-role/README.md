# ansible-fake-role

A role to install and configure default packages.

## Ansible requirements

### Ansible version

Minimum required ansible version is 2.0.

### Ansible role dependencies

None.

## Installation

### Install with Ansible Galaxy

```shell
ansible-galaxy install nchuck.fake-role
```

Basic usage is:

```yaml
- hosts: all
  roles:
    - role: nchuck.fake-role
```

### Install with git

If you do not want a global installation, clone it into your `roles_path`.

```shell
git clone git@github['com']:nchuck/ansible-fake-role.git /path/to/roles_path
```

But I often add it as a submdule in a given `playbook_dir` repository.

```shell
git submodule add git@github['com']:nchuck/ansible-fake-role.git <playbook_dir>/roles/fake-role
```

As the role is not managed by Ansible Galaxy, you do not have to specify the
github user account.

Basic usage is:

```yaml
- hosts: all
  roles:
  - role: fake-role
```
## User guide

Content of this file will be literally inserted into the resulting README.
Below are some suggested subsections.

### Requirements

Explain your role requirements. e.g:

* The server needs WWW access
* The server needs to access internal repos
* ...

### Introduction

In case your role is complex you might want ot explain here the rational of
certain behaviors and/or concepts.

### Usage

Some role usage scenarios and examples.

# other miscencillious information you may want to share.
misc: |
  This role was carefully selected to be part an ultimate deck of roles to manage
  your infrastructure.

  All roles' documentation is wrapped in this [convenient guide](http://127.0.0.1:8000/).


## Role Variables

Variables are divided in three types.

The [default vars](#default-vars) section shows you which variables you may
override in your ansible inventory. As a matter of fact, all variables should
be defined there for explicitness, ease of documentation as well as overall
role manageability.

The [mandatory variables](#mandatory-variables) section contains variables that
for several reasons do not fit into the default variables. As name implies,
they must absolutely be defined in the inventory or else the role will
fail. It is a good thing to avoid reach for these as much as possible and/or
design the role with clear behavior when they're undefined.

The [context variables](#context-variables) are shown in section below hint you
on how runtime context may affects role execution.

### Default vars

Role default variables from `defaults/main.yml`.

```yaml
fake_role_pkg_state: latest

```

### Mandatory variables.

None.

### Context variables

Those variables from `vars/*.{yml,json}` are loaded dynamically during task
runtime using the `include_vars` module.

Variables loaded from `vars/Debian.yml`.

```yaml
fake_role_pkgs:
  - debian-pkg1
  - debian-pkg2
  - debian-pkg3

```
 
Variables loaded from `vars/RedHat.yml`.

```yaml
fake_role_pkgs:
  - rhel-pkg1
  - rhel-pkg2
  - rhel-pkg3

```
 
## Todo

You want to contribute and don't know where to start? Here's a few ideas base
on what we think it should be nice to implement next:

  * add this new awesome feature

Consider opening an issue to share your intent and avoid work duplication!
## License

MIT.

## Author Information

Chuck Norris.

