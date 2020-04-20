import getopt, sys
import requests, zipfile
import json

json_registry_file = './import/registry/registry.json'
modules_target = './import/modules'

# GET NAME OF MODULE FROM PARAMS
short_options = "m:"
long_options = ["module="]

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
        print("Download and prepare module " + module_name)

if module_name == '':
    print('Module name is required. Please use -m or --module to specify module name')
    sys.exit(2)

# DOWNLOAD MODULE
rfile = open(json_registry_file, 'r')
json_registry_content = json.loads(rfile.read().encode().decode('utf-8-sig'))
modules_list = json_registry_content['downloads']
module = [x for x in modules_list if x['abr'] == module_name]

if not module:
    print('Specified module not found in registry')
    sys.exit(2)
elif len(module) > 1:
    print('Specified module not unique')
    sys.exit(2)
else:
    module = module[0]

# print(module)
source_host_list = json_registry_content['hosts']
source_host_list.sort(key=lambda el: el['weight'], reverse=True)
source_host = source_host_list[0]

module_url = [source_host['path'] % url.replace('{' + source_host['alias'] + '}', '') for url in module['url'] if
              url.find('{' + source_host['alias'] + '}') != -1][0]
# print(module_url)

response = requests.get(module_url, allow_redirects=True)

with open(modules_target + '/' + module_name + '.zip', 'wb') as zfile:
    zfile.write(response.content)

# LOAD MODULE TO PGSQL


# PARSE MODULE VERSE TO WORDS BY STRONG


