import getopt, sys, os
import requests, zipfile
import json
from pathlib import Path

json_registry_file = './import/registry/registry.json'
modules_target = './import/modules'
pg_loader_configs = './import/tmp/pg_mod.load'
module_name_replace_symbols_configs = './import/configs/module_name_replace_symbols.json'
db_configs = './import/configs/db_config.json'
db_configs = json.loads(open(db_configs,'r').read().encode().decode('utf-8-sig'))

# GET NAME OF MODULE FROM PARAMS
short_options = "m:r"
long_options = ["module=","reload"]

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
        print("Download and prepare module " + module_name)
    elif current_argument in ("-r", "--reload"):
        reload = True
        print("Reload from url soruce " + module_name)

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
source_host_list.sort(key=lambda el: el['weight'])
source_host = source_host_list[0]

module_url = [source_host['path'] % url.replace('{' + source_host['alias'] + '}', '') for url in module['url'] if
              url.find('{' + source_host['alias'] + '}') != -1][0]
print(module_url)

zip_file_target = modules_target + '/' + module_name + '.zip'
if reload:
    response = requests.get(module_url, allow_redirects=True)

    with open(zip_file_target, 'wb') as zfile:
        zfile.write(response.content)

    print(zip_file_target)
else:
    print('Skip download, use cached module')

with zipfile.ZipFile(zip_file_target, 'r') as zip_reg:
    zip_reg.extractall(modules_target)

pg_conn_string = 'psql -h rev_pgsql -p 5432 -U rev_user -w'

replace = json.loads(open(module_name_replace_symbols_configs,'r').read().encode().decode('utf-8-sig'))

db_name = module_name
for s in replace:
    db_name = db_name.replace(s,replace[s])
db_name = db_name.lower()

print('Create and fill db {} from module {}'.format(db_name,module_name))

# LOAD MODULE TO PGSQL
os.system('echo "SELECT \'CREATE DATABASE {}\' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = \'{}\')\gexec" | {}'.format(db_name,db_name,pg_conn_string))

Path("import/tmp").mkdir(parents=True, exist_ok=True)
rfile = open(pg_loader_configs,'w')
rfile.write("""load database
     from sqlite:///var/app/import/modules/.SQLite3
     into postgresql://{}:{}@{}:{}/{}

 with include drop, create tables, drop indexes, create indexes, reset sequences

  set work_mem to '16MB', maintenance_work_mem to '512 MB';""".format(db_configs['user'],db_configs['pass'],db_configs['host'],db_configs['port'],db_name))
rfile.close()
os.system('pgloader import/tmp/pg_mod.load')


