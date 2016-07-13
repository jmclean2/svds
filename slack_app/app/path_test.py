import os
import os.path

config_file_name = 'config_file.cfg'
PATH = '../config/config_file.cfg'

if ( os.path.isfile(PATH)):
 config_file_name = PATH
else:
 config_file_name = 'config_file.cfg'

print(config_file_name)