import getopt,sys
import requests, zipfile
import json

json_registry_file = './import/registry/registry.json'
modules_target = './import/modules'


#GET NAME OF MODULE FROM PARAMS
short_options = "m:"
long_options = ["module="]

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)


module_name = ''
for current_argument, current_value in arguments:
    if current_argument in ("-m", "--module"):
        module_name = current_value
        print ("Download and prepare module" + module_name)

if module_name=='':
    print('Module name is required. Please use -m or --module to specify module name')
    sys.exit(2)





#DOWNLOAD MODULE
rfile = open(json_registry_file,'r')
json_registry_content = json.loads(rfile.read().encode().decode('utf-8-sig'))
modules_list = json_registry_content['downloads']
source_list =  json_registry_content['registries']




#LOAD MODULE TO PGSQL





#PARSE MODULE VERSE TO WORDS BY STRONG








#GET REGISTRY FROM
#response = requests.get(url,allow_redirects=True)

#UNZIP REGISTRY AND BEAUTIFY JSON STRUCTURE OF REGISTRY
#with open(zip_file_target,'wb') as zfile:
#    zfile.write(response.content)

#with zipfile.ZipFile(zip_file_target, 'r') as zip_reg:
#    zip_reg.extractall(zip_registry_extract_target)

#rfile = open(json_registry_file,'r')
#json_registry_content = json.loads(rfile.read().encode().decode('utf-8-sig'))
#rfile.close()
#rfile = open(json_registry_file,'w')

#rfile.write(json.dumps(json_registry_content,sort_keys=True, indent=4))






