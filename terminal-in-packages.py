import sublime
import sublime_plugin
import threading
import os
import subprocess
import platform

PLATFORM = platform.system()
TERMINAL = ''
log = print


class CommandThread(threading.Thread):

    def __init__(self, command):
        self.command = command
        threading.Thread.__init__(self)

    def run(self):
        command = "{}".format(self.command)
        env = os.environ.copy()
        if PLATFORM == 'Windows':
            command = [
                'cmd.exe',
                '/k', "{} && timeout /T 10 && exit".format(command)
            ]
        if PLATFORM == 'Linux':
            command = [
                TERMINAL,
                '-e', 'bash -c \"{0}; read line\"'.format(command)
            ]
        if PLATFORM == 'Darwin':
            command = [
                'osascript',
                '-e', 'tell app "Terminal" to activate',
                '-e', 'tell application "System Events" to tell process \
                "Terminal" to keystroke "t" using command down',
                '-e', 'tell application "Terminal" to \
                do script "{0}" in front window'.format(command)
            ]

        log('Command is : {0}'.format(str(command)))
        subprocess.Popen(command, env=env)


class TerminalInPackagesCommand(sublime_plugin.WindowCommand):

    def __init__(self, *args, **kwargs):
        self.settings = sublime.load_settings('terminalinpackages.sublime-settings')
        global TERMINAL
        TERMINAL = self.settings.get('terminal-emulator')
        super(TerminalInPackagesCommand, self).__init__(*args, **kwargs)

    def run(self):
        pdir = sublime.packages_path()
        change_dir_command = 'cd {0}'.format(pdir)
        if PLATFORM == 'Windows':
            command = 'cmd /k {}'.format(change_dir_command)
        if PLATFORM == 'Linux' or PLATFORM == 'Darwin':
            command = "bash --rcfile <(echo '. ~/.bashrc && {}')".format(change_dir_command)
        print(command)
        thread = CommandThread(command)
        thread.start()
