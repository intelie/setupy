# coding: utf-8

from setupy import Component, sh, sh_io, ask_or_download
import os


class JRE(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False
    

    def is_installed(self):
        try:
            return sh('java').returncode == 0
        except OSError:
            return False

    
    def install_binary_rpm_64(self):
        "Install using the binary RPM (it'll download you don't have the file)"
        url = 'http://javadl.sun.com/webapps/download/AutoDL?BundleId=39488'
        filename = '/tmp/jre-6u20-linux-x64-rpm.bin'
        filename_on_system = ask_or_download(url, filename)
        if not filename_on_system:
            return False
        sh_io('chmod +x %s' % filename_on_system)
        return sh_io(filename_on_system)

    def install_binary_32(self):
        'Install with the binary 32bit (without RPM)'
        url = 'http://javadl.sun.com/webapps/download/AutoDL?BundleId=39485'
        filename = '/tmp/jre-6u20-linux-i586.bin'
        filename_on_system = ask_or_download(url, filename)
        if not filename_on_system:
            return False
        print2('Installing JRE ... ')
        sh_io('chmod +x %s' % filename_on_system)
        java_install = sh(filename_on_system, finalize=False)
        ask_agree = 'Do you agree to the above license terms? [yes or no]\n'
        while java_install.stdout.readline() != ask_agree:
            pass #Read the Java License carefully: line by line
        java_install.stdin.write('yes\n') #As I've read I can accept
        out, err = java_install.communicate()
        java_install.wait()
        #TODO: now it is unpacked on ./jre1.6.0_20/. What should I do?
        # Move to /opt and create symlinks on /usr/bin?
        if java_install.returncode == 0:
            print('OK')
            return True
        else:
            print('FAILED')
            return False


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

