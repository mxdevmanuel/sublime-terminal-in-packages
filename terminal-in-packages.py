import sublime
import sublime_plugin
import threading
import os
import subprocess
import platform

PLATFORM = platform.system()


class CommandThread(threading.Thread):

    def __init__(self, terminal):
        self.terminal = terminal
        self.package_dir = sublime.packages_path()
        threading.Thread.__init__(self)

    def run(self):
        env = os.environ.copy()
        if PLATFORM == 'Windows':
            command = [
                'cmd.exe'
            ]
        if PLATFORM == 'Linux':
            command = [
                self.terminal
            ]
        if PLATFORM == 'Darwin':
            command = [
                'osascript',
                '-e', 'tell app "Terminal" to activate',
                '-e', 'tell application "System Events" to tell process \
                "Terminal" to keystroke "t" using command down',
                '-e', 'tell application "Terminal" to \
                do script "bash" in front window'
            ]
        subprocess.Popen(command, env=env, cwd=self.package_dir)


class TerminalInPackagesCommand(sublime_plugin.WindowCommand):

    def __init__(self, *args, **kwargs):
        self.settings = sublime.load_settings('terminalinpackages.sublime-settings')
        super(TerminalInPackagesCommand, self).__init__(*args, **kwargs)

    def run(self):
        terminal = self.settings.get('terminal-emulator')
        thread = CommandThread(terminal)
        thread.start()
