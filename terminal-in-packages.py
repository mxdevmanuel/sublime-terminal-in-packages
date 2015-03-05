import sublime
import sublime_plugin
import threading
import os
import subprocess
import platform

PLATFORM = platform.system()


class CommandThread(threading.Thread):

    def __init__(self, command, terminal):
        self.command = command
        self.terminal = terminal
        self.package_dir = sublime.packages_path()
        threading.Thread.__init__(self)

    def run(self):
        env = os.environ.copy()
        if PLATFORM == 'Windows':
            command = [
                'cmd.exe',
                '/k', "{} && timeout /T 10 && exit".format(self.command)
            ]
        if PLATFORM == 'Linux':
            command = [
                self.terminal,
                '-e', 'bash -c \"{0}; read line\"'.format(self.command)
            ]
        if PLATFORM == 'Darwin':
            command = [
                'osascript',
                '-e', 'tell app "Terminal" to activate',
                '-e', 'tell application "System Events" to tell process \
                "Terminal" to keystroke "t" using command down',
                '-e', 'tell application "Terminal" to \
                do script "{0}" in front window'.format(self.command)
            ]
        subprocess.Popen(command, env=env, cwd=self.package_dir)


class TerminalInPackagesCommand(sublime_plugin.WindowCommand):

    def __init__(self, *args, **kwargs):
        self.settings = sublime.load_settings('terminalinpackages.sublime-settings')
        super(TerminalInPackagesCommand, self).__init__(*args, **kwargs)

    def run(self):
        if PLATFORM == 'Windows':
            command = 'cmd'
        if PLATFORM == 'Linux' or PLATFORM == 'Darwin':
            command = "bash"
        terminal = self.settings.get('terminal-emulator')
        thread = CommandThread(command, terminal)
        thread.start()
