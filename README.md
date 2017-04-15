# DO Help.

  - Manages the installation of GitLab from scratch on a single (or multiple) DO instances (maybe other hosting providers too), with a single command
  - Syncs local GDK/GitLab instance or remote branch to DO, and automatically restarts and runs migrations on the instance.
  - Some other magic
  - Does everything from the local machine

## Requirements
### Remote
 - rsync (should be there by default)
 - user with sudo (better without password) SSH access

### Local
 - rsync (should be there by default)
 - fabric (brew install fabric)

## Setup

Change `fabfile.py` header configuration to suit your needs. Particularly:

 - `env.user`: Remote SSH login
 - `env.hosts`: Remote SSH host(s)

Alternatively, you can use it by passing `-H login@host`.

## Examples

Runs the initial setup on a DO instance and installs GitLab CE version 9.0.0:

```sh
$ fab setup
$ fab install 9.0.0
```

Syncs local GitLab CE code with remote DO instance, runs migrations and restarts Unicorn workers

```sh
$ fab sync
```

## List of commands:

| Command | Description |
| ------ | ------ |
| fab setup | GitLab repo setup (install required dependencies) |
| fab install:version,edition,package | Installs specified GitLab version X.X.X. Defaults to X.X.X,ce,0|
| uninstall | Uninstall GitLab |
| sync:extra_dirs,edition | Syncs default dirs (app,lib,db) + extra_dirs (if specified) from local instance to remote and restarts and runs migrations on GitLab |
| sync_branch:branch_name,extra_dirs,edition | Syncs default dirs (app,lib,db) + extra_dirs (if specified) from remote branch to remote and restarts and runs migrations on GitLab |
| run_migrations | Runs migrations on DO instance |
| restart | Restarts unicorn on DO instance |
| restart_all | Restarts all GitLab services on DO instance |
| reconfigure | Reconfigures GitLab on DO instance |
| logs | Tails GitLab logs on DO instance |

License
----

MIT

