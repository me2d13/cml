from os.path import dirname, basename, isfile, join
from importlib import import_module
import glob
import re

module_files = glob.glob(join(dirname(__file__), "*.py"))
modules = [ basename(f)[:-3] for f in module_files if isfile(f) and not f.endswith('__init__.py')]
#print('Detected commands', modules)
commands = {}
numeric_pattern = re.compile('[0-9]+')
for file in modules:
    if file != 'abstract_command':
        command_file = import_module('.{}'.format(file), 'commands')
        if numeric_pattern.match(file):
            print('Importing numeric command', file)
            commands[file] = command_file.CmlCommand(file)
        else:
            print('Trying to import commands from file', file)
            try:
                file_commands = command_file.create_commands()
                if file_commands:
                    commands.update(file_commands)
            except:
                print("File {} has no create_commands() function. Ignored".format(file))