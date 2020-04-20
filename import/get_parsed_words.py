import getopt, sys, os
import requests, zipfile
import json


# GET NAME OF MODULE FROM PARAMS
short_options = "m:"
long_options = ["module="]

reload = False
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print(str(err))
    sys.exit(2)

module_name = ''
for current_argument, current_value in arguments:
    if current_argument in ("-m", "--module"):
        module_name = current_value
        print("Parse verses in module " + module_name)

if module_name == '':
    print('Module name is required. Please use -m or --module to specify module name')
    sys.exit(2)

# SPECIFY DB NAME FOR PARSE MODULE
module_name_replace_symbols_configs = './import/configs/module_name_replace_symbols.json'
replace = json.loads(open(module_name_replace_symbols_configs,'r').read().encode().decode('utf-8-sig'))

db_name = module_name
for s in replace:
    db_name = db_name.replace(s,replace[s])
db_name = db_name.lower()


# PARSE MODULE VERSE TO WORDS BY STRONG


