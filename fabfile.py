from fabric.api import *
from fabric.contrib.project import *

env.user = 'james'
env.hosts = ['jlo']

local_gitlab = {}
local_gitlab['ce'] = '~/Development/gitlab-development-kit/gitlab'
local_gitlab['ee'] = '~/Development/gitlab-development-kit-ee/gitlab'
local_tmp_gitlab = '/tmp/gitlab-doh'
remote_gitlab = '/opt/gitlab/embedded/service/gitlab-rails'

sync_dirs = ['app', 'lib', 'db']

@task
def setup():
    sudo('apt-get install -y curl openssh-server ca-certificates postfix')
    with cd('/tmp'):
        run("curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash")
    
@task
def install(version, edition='ce', package='0'):
    sudo('apt-get -y update')
    sudo("sudo apt-get install gitlab-%s=%s-%s.%s" % (edition, version, edition,package))
    sudo('gitlab-ctl reconfigure')
    
@task
def uninstall(edition='ce'):
    sudo('apt-get remove -y --purge gitlab-' + edition)

@task
def sync(extra_dirs = [], edition='ce'):
    sync_dirs.extend(extra_dirs)
    
    for sync_dir in sync_dirs:
        local_gitlab_dir = "%s/%s/" % (local_gitlab[edition], sync_dir)
        remote_gitlab_dir = "%s/%s/" % (remote_gitlab, sync_dir)
        rsync_project(remote_gitlab_dir, local_gitlab_dir, extra_opts="-e ssh --rsync-path=\"sudo rsync\"")

    sudo("chown -R git:root /opt/gitlab/embedded/service/gitlab-rails/")
    run_migrations()
    restart()

@task
def sync_branch(branch_name, extra_dirs = [], edition='ce'):
    sync_dirs.extend(extra_dirs)
    local_tmp_gitlab_edition = "%s/%s" % (local_tmp_gitlab, edition)
    with lcd(local_tmp_gitlab_edition):
        if not exists(local_tmp_gitlab_edition):
            run("git clone git@gitlab.com:gitlab-org/gitlab-%s.git .", edition)
        run("git fetch %s", branch_name)
        run("git checkout %s", branch_name)
        run("git pull %s", branch_name)       

    # TODO inherit this using new fab syntax.
    for sync_dir in sync_dirs:
        local_gitlab_dir = "%s/%s/" % (local_tmp_gitlab_edition, sync_dir)
        remote_gitlab_dir = "%s/%s/" % (remote_gitlab, sync_dir)
        rsync_project(remote_gitlab_dir, local_gitlab_dir, extra_opts="-e ssh --rsync-path=\"sudo rsync\"")

    sudo("chown -R git:root /opt/gitlab/embedded/service/gitlab-rails/")
    restart()
    run_migrations()

@task
def run_migrations():
    sudo('gitlab-rake db:migrate')

@task
def restart():
    sudo('gitlab-ctl restart unicorn')

@task
def restart_all():
    sudo('gitlab-ctl restart')

@task
def reconfigure():
    sudo('gitlab-ctl reconfigure')

@task
def logs():
    env.remote_interrupt = True
    with settings(warn_only=True):
        sudo("gitlab-ctl tail")
