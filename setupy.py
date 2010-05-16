# coding: utf-8

import os
import subprocess
import inspect
import struct
import shlex

print2 = os.sys.stdout.write

class Storage(object):
    pass

def sh_io(command):
    return subprocess.call(shlex.split(command))


def sh(command):
    process = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    process.wait()
    process.out = process.stdout.read()
    process.err = process.stderr.read()
    return process


def get_operating_system():
    bits = struct.calcsize('P') * 8
    name = os.name.capitalize()
    if name != 'Posix':
        return name, bits, None
    else:
        result = open('/tmp/linux_distribution', 'rw')
        try:
            a = subprocess.Popen(['lsb_release', '-a'], stderr=result, stdout=result)
        except OSError:
            return name, bits, None
        else:
            distribution = name
            version = None
            contents = result.read().split('\n')
            result.close()
            for line in contents:
                if line.startswith('Distributor ID:'):
                    distribution = line.split('Distributor ID:')[1].strip()
                elif line.startswith('Release:'):
                    version = line.split('Release:')[1].strip()
            return distribution, bits, version

operating_system = get_operating_system()


def ask_with_limited_answers(question, answers):
    answers = [answer.lower() for answer in answers]
    answer = None
    while answer not in answers:
        answer = raw_input(question).lower()
    return answer


def ask_yes_no(question):
    answer = ask_with_limited_answers(question + ' [y/n] ', ['yes', 'no', 'y', 'n'])
    if answer[0] == 'y':
        return True
    return False


class Component(object):

    def __init__(self):
        self._is_installed = None
        self._is_configured = None
        self.needs_configuration = None
        self.name = self.__class__.__name__


    def is_installed(self):
        return self._is_installed


    def install(self):
        install_methods = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if attr_name.startswith('install_') and inspect.ismethod(attr):
                install_methods.append({'method': attr, 'name': attr_name,
                                        'doc': attr.__doc__})
        if len(install_methods) == 0:
            print2('This software does not provide any installation method.')
            return
        elif len(install_methods) == 1:
            answer = '1'
        else:
            menu = '\n'.join(['(%d) %s' % (x + 1, install_method['doc'].strip()) \
                              for x, install_method in enumerate(install_methods)])
            ask = 'Current install methods for install %s are:\n%s\nType what you want: '
            options = [str(x) for x in range(1, len(install_methods) + 1)]
            answer = ask_with_limited_answers(ask % (self.name, menu), options)
        install_method = install_methods[int(answer) - 1]['method']
        if install_method():
            self._is_installed = True
        return self._is_installed


    def is_configured(self):
        return self._is_configured


    def configure(self):
        #TODO: configure() should act as install()
        self._is_configured = True
        return self._is_configured

    
    def try_install(self):
        print2('Verifying if %s is installed ... ' % self.name)
        if self.is_installed():
            print('INSTALLED')
            return None
        else:
            print('NOT INSTALLED')
            print2('Installing %s ... ' % self.name)
            if self.install():
                print('OK')
                return True
            else:
                print('FAILED')
                return False


    def try_configure(self):
        print2('Verifying if %s is configured ... ' % self.name)
        if self.is_configured():
            print('CONFIGURED')
            return None
        else:
            if not self.needs_configuration:
                print("NOT CONFIGURED (DON'T NEED)")
                return True
            else:
                print('NOT CONFIGURED')
                print2('Configuring %s ... ' % self.name)
                if self.configure():
                    print('OK')
                    return True
                else:
                    print('FAILED')
                    return False

def install_interactive(software_list):
    print('Installing/configuring: %s' % ', '.join([x.__name__ for x in software_list]))
    ask_continue = 'Do you want to continue with the installtion/configuration of other recipes?'
    for Software in software_list:
        obj = Software()
        if obj.try_install() is False or obj.try_configure() is False:
            if not ask_yes_no(ask_continue):
                break





def list_installed(software_list):
    yes = u'\u2713' #unicode rules
    no = u'\u2717'
    for Software in software_list:
        obj = Software()
        installed = color(' %s NOT INSTALLED ' % no, background='red')
        if obj.is_installed():
            installed = color(' %s   INSTALLED   ' % yes, background='green')

        configured = 'NOT CONFIGURED'
        needs_configuration = " (DON'T NEED)"
        if obj.needs_configuration:
            needs_configuration = ''
            configured = color(' %s %s ' % (no, configured), background='red')
        else:
            configured = color(' %s %s ' % (yes, configured), background='green')
        if obj.is_configured():
            configured = color(' %s   CONFIGURED   ' % yes, background='green')
        print('%20s %20s %20s%s' % (obj.name, installed, configured,
                                    needs_configuration))



def list_recipes(recipes):
    software_list = []
    for attr_name in dir(recipes):
        attr = getattr(recipes, attr_name)
        if inspect.isclass(attr):
            parents = [x.__name__ for x in attr.__bases__]
            if 'Component' in parents:
                software_list.append(attr)
    return software_list


COLOR_NAMES = ('red', 'green', 'blue', 'magenda', 'cyan', 'gray')
COLORS = dict(zip(COLOR_NAMES, range(31, 38)))
BACKGROUND_COLORS = dict(zip(COLOR_NAMES, range(41, 48)))

def color(text, color=None, background=None):
    if color:
        text = '\033[%dm%s\033[0m' % (COLORS[color], text)
    if background:
        text = '\033[%dm%s\033[0m' % (BACKGROUND_COLORS[background], text)
    return text

