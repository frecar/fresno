from fabric.api import *

# the user to use for the remote commands
env.user = 'user'
# the servers where the commands are executed
env.hosts = ['fresno.frecar.no']


def deploy():

    with cd('/opt/fresno/'):
        run('git pull origin master')

    run("sudo supervisorctl restart fresno")
