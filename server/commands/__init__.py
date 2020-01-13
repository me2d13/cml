from os.path import dirname, basename, isfile, join
from importlib import import_module
import glob

module_files = glob.glob(join(dirname(__file__), "*.py"))
modules = [ basename(f)[:-3] for f in module_files if isfile(f) and not f.endswith('__init__.py')]
#print('Detected commands', modules)
commands = {}
for file in modules:
    if file != 'abstract_command':
        command_file = import_module('.{}'.format(file), 'commands')
        commands[file] = command_file.CmlCommand(file)