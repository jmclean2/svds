import os
import os.path

config_file_name = 'config_file.cfg'
PATH = '.svds/config/config_file.cfg'
if ( os.path.isfile(PATH) ):
 print("true")
else:
 print("false")