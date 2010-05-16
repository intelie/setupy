# coding: utf-8

import subprocess
import ConfigParser
from setupy import execute_command_with_user_io, ask_yes_no, Component, \
                   operating_system


class JRE(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False
    

    def is_installed(self):
        #TODO: open a file just to get the info of a process?
        err = open('/tmp/err', 'w')

        #TODO: setupy needs something general to do this code:
        # Something like return sh('java') == 0
        try:
            java_process = subprocess.Popen(['java'], stderr=err, stdout=err)
        except OSError:
            self._is_installed = False
        else:
            self._is_installed = java_process.wait() == 0
        err.close()
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
            java_download = execute_command_with_user_io('wget %s -O %s' % (url, filename))
            if java_download != 0:
                print('Download failed!')
                return False

        execute_command_with_user_io('chmod +x %s' % filename)
        java_install = execute_command_with_user_io(filename)
        if java_install == 0:
            return True
        else:
            return False


    def install_yum(self):
        '''
        Install using YUM
        '''
        return_code = execute_command_with_user_io('yum install -y java-1.6.0-openjdk')
        if return_code == 0:
            return True
        else:
            return False


class MySQLServer(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_installed(self):
        try:
            f = open('/etc/my.cnf', 'r') #CentOS
        except IOError:
            installed_centos = False
        else:
            installed_centos = True

        try:
            f = open('/etc/mysql/my.cnf', 'r') #Debian
        except IOError:
            installed_debian = False
        else:
            installed_debian = True

        return installed_centos or installed_debian


    def install_yum(self):
        '''
        Install using YUM
        '''
        mysql_install = execute_command_with_user_io('yum install -y mysql-server.x86_64')
        if mysql_install == 0:
            return True
        else:
            return False


    def configure(self):
        distribution = operating_system[0]
        if distribution not in ['CentOS', 'RedHat', 'Debian', 'Ubuntu']:
            return False #Only support distributions above

        if distribution in ['CentOS', 'RedHat']:
            execute_command_with_user_io('chkconfig mysqld on')
            config_filename = '/etc/my.cnf'
            restart_command = 'service mysqld restart'
        else:
            #TODO: start on boot (Debian default?)
            config_filename = '/etc/mysql/my.cnf'
            restart_command = '/etc/init.d/mysql restart'
        
        #I should change some config here - but please, DON'T use ConfigParser

        #Run MySQL        
        execute_command_with_user_io(restart_command)


    def is_configured(self):
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

