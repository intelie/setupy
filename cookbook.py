# coding: utf-8

import subprocess
import ConfigParser
from setupy import ask_yes_no, Component, operating_system, sh
import os


class JRE(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False
    

    def is_installed(self):
        self._is_installed = sh('java').returncode == 0
        return self._is_installed

    
    def install_from_binary(self):
        '''
        Install using the binary (it'll download if it isn't here)
        '''

        filename = raw_input("If you have the file jre-6u20-linux-x64-rpm.bin, please specify the complete path (if not just hit ENTER so it'll be downloaded):\n")
        if not filename:
            print('Downloading ...')
            filename = '/tmp/jre-6u20-linux-x64-rpm.bin'
            url = 'http://javadl.sun.com/webapps/download/AutoDL?BundleId=39488'
            java_download = sh_io('wget %s -O %s' % (url, filename))
            if java_download != 0:
                print('Download failed!')
                return False
        sh('chmod +x %s' % filename)
        return sh_io(filename) == 0


    def install_yum(self):
        '''
        Install using YUM
        '''
        return sh_io('yum install -y java-1.6.0-openjdk') == 0


class MySQLServer(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_installed(self):
        #CentOS: /etc/my.cnf
        #Debian: /etc/mysql/my.cnf
        exists = os.path.exists
        return exists('/etc/my.cnf') or exists('/etc/mysql/my.cnf')


    def install_yum(self):
        '''
        Install using YUM
        '''
        mysql_install = sh_io('yum install -y mysql-server.x86_64')
        if mysql_install == 0:
            return True
        else:
            return False


    def configure(self):
        distribution = operating_system[0]
        if distribution not in ['CentOS', 'RedHat', 'Debian', 'Ubuntu']:
            return False #Only support distributions above

        if distribution in ['CentOS', 'RedHat']:
            sh('chkconfig mysqld on')
            config_filename = '/etc/my.cnf'
            restart_command = 'service mysqld restart'
        else:
            #TODO: start on boot (Debian default?)
            config_filename = '/etc/mysql/my.cnf'
            restart_command = '/etc/init.d/mysql restart'

        #TODO: change some config here - but please, DON'T use ConfigParser

        #Restart MySQL (only needed if changed some configuration above)
        #sh_io(restart_command)


    def is_configured(self):
        #TODO: check if MySQL is configured properly
        return True


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

