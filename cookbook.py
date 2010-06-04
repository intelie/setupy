# coding: utf-8

from setupy import Component, sh, sh_io, ask_or_download, print2, \
                   get_operating_system
import os


class JRE(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False
    

    def is_installed(self):
        try:
            assert sh('java').returncode == 0
        except OSError:
            assert False

    
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


    def add_nonfree_repository(self):
        sources_list = open('/etc/apt/sources.list', 'r')
        for line in sources_list:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('deb-src') \
               or line.startswith('deb http://volatile'):
                continue
            splitted = line.split()
            dist = splitted[2].split('/')[0]
            url = splitted[1]
            if 'non-free' in ' '.join(splitted[3:]):
                sources_list.close()
                break
        else:
            sources_list.close()
            sources_list = open('/etc/apt/sources.list', 'a')
            print2('Adding non-free to sources.list ... ')
            sources_list.write('\ndeb %s %s non-free\n' % (url, dist))
            sources_list.close()
            print('OK')
            print2('Update APT base ... ')
            if sh('aptitude update'):
                print('OK')
                return True
            else:
                return False


    def install_apt(self):
        'Install using aptitude'
        distribution = get_operating_system()[0]
        if distribution == 'Debian':
            self.add_nonfree_repository()

        #TODO: trust untrusted packages: read aptitude output and say yes
        return sh_io('aptitude -y install sun-java6-jre')


    def install_yum(self):
        'Install using YUM'
        return sh_io('yum install -y java-1.6.0-openjdk')


class MySQLServer(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = False
        self.distribution = get_operating_system()[0]

        if self.distribution in ['CentOS', 'RedHat']:
            self.config_filename = '/etc/my.cnf'
            self.restart_command = 'service mysqld restart'
        elif self.distribution in ['Debian', 'Ubuntu']:
            self.config_filename = '/etc/mysql/my.cnf'
            self.restart_command = '/etc/init.d/mysql restart'
        else:
            self.configure = lambda: False

    def is_installed(self):
        #CentOS: /etc/my.cnf, Debian: /etc/mysql/my.cnf
        exists = os.path.exists
        assert exists('/etc/my.cnf') or exists('/etc/mysql/my.cnf')


    def install_yum(self):
        'Install using YUM'
        return sh_io('yum install -y mysql-server.x86_64')


    def install_apt(self):
        'Install using aptitude'
        #We need to answer debconf for root password
        return sh_io('aptitude -y install mysql-server')


class DummyOne(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_configured(self):
        assert 1 == 0


    def is_installed(self):
        assert 42 == 42


class DummyTwo(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_configured(self):
        assert 42 == 42


    def is_installed(self):
        assert 0 == 1


class DummyThree(Component):
    def __init__(self):
        Component.__init__(self)
        self.needs_configuration = True


    def is_configured(self):
        assert 42 == 42


    def is_installed(self):
        assert 0 == 1


    def install_dummy(self):
        return True


    def configure_dummy(self):
        return True

