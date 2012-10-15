import os.path
from fabric.api import *

env.user = 'ec2-user'
env.roledefs = {
    'all':['fabric', 's1', 's2'],
    'web':['s1', 's2']
}

def install_apache_with_mod_wsgi():
    sudo("yum install -y httpd.x86_64 mod_wsgi.x86_64 git")

def install_flask():
    sudo("easy_install pip")
    sudo("pip install flask")
    with cd("/tmp"):
        run("rm -rf flask && git clone git://github.com/mitsuhiko/flask.git")
    db_init_script = os.path.join(os.path.dirname(__file__), "db_init.py")
    rpath_script = "/tmp/flask/examples/flaskr/db_init.py"
    put(db_init_script, rpath_script)
    run("python %s" % rpath_script)
    run("rm -f %s" % rpath_script)
    
    sudo("chown apache /tmp/flaskr.db")

def configure_wsgi():
    mod_wsgi_path = os.path.join(os.path.dirname(__file__), "mod_wsgi.conf")
    wsgi_path = os.path.join(os.path.dirname(__file__), "my.wsgi")
    put(mod_wsgi_path, "/etc/httpd/conf.d/mod_wsgi.conf", use_sudo=True)
    put(wsgi_path, "/tmp/flask/examples/flaskr/my.wsgi")

@task
def build_web():
    install_apache_with_mod_wsgi()
    install_flask()
    configure_wsgi()

@task 
def restart_web():
    sudo("service httpd restart")
