# coding: utf-8

import subprocess
import ConfigParser
from setupy import ask_yes_no, Component, sh, ask_or_download
import os


class JRE(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False
    

    def is_installed(self):
        return sh('java').returncode == 0

    
    def install_from_binary(self):
        "Install using the binary (it'll download you don't have the file)"
        filename = '/tmp/jre-6u20-linux-x64-rpm.bin'
        url = 'http://javadl.sun.com/webapps/download/AutoDL?BundleId=39488'
        if not ask_or_download(filename, url):
            return False
        sh('chmod +x %s' % filename)
        return sh_io(filename)


    def install_yum(self):
        'Install using YUM'
        return sh_io('yum install -y java-1.6.0-openjdk')


    def install_apt(self):
        'Install using aptitude'
        #TODO: needs non-free on Debian. should configure apt first
        return sh_io('aptitude -y install sun-java6-jre')


class MySQLServer(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False


    def is_installed(self):
        #CentOS: /etc/my.cnf, Debian: /etc/mysql/my.cnf
        exists = os.path.exists
        return exists('/etc/my.cnf') or exists('/etc/mysql/my.cnf')


    def install_yum(self):
        'Install using YUM'
        return sh_io('yum install -y mysql-server.x86_64')


    def install_apt(self):
        'Install using aptitude'
        return sh_io('aptitude -y install mysql-server')


class DummyOne(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_configured(self):
        return True


    def is_installed(self):
        return True


class DummyTwo(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_configured(self):
        return False


    def is_installed(self):
        return False


class DummyThree(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_configured(self):
        return False


    def is_installed(self):
        return False


    def install_dummy(self):
        return True


    def configure_dummy(self):
        return True

