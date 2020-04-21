import getopt, sys, os
import requests, zipfile
import json

# GET NAME OF MODULE FROM PARAMS
short_options = "r"
long_options = ["reload"]

zip_file_target = './import/registry/registry.zip'
zip_registry_extract_target = './import/registry'
json_registry_file = './import/registry/registry.json'

cache_registry_file_exist = os.path.isfile(json_registry_file)
reload = not cache_registry_file_exist
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print(str(err))
    sys.exit(2)


for current_argument, current_value in arguments:
    if current_argument in ("-r", "--reload"):
        reload = True
        print("Reload registry from source")


if reload:

    if cache_registry_file_exist:
        rfile = open(json_registry_file, 'r')
        json_registry_content = json.loads(rfile.read().encode().decode('utf-8-sig'))
        url = json_registry_content['registries']
        url.sort(key=lambda el: el['priority'])
        url = [x['url'] for x in url if 'test' not in x or not x['test']]
    else:
        url = 'http://myb1ble.1nterb1bl1a.org/reg1stry.z1p'
        url = [url.replace('1', 'i')]


    #GET REGISTRY FROM
    i = 0
    response = requests.get(url[i])
    print('try url '+url[i])
    while not response.ok:
        i += 1
        print('try url '+ url[i])
        response = requests.get(url[i])

    if not response.ok:
        print('Unable to load registry. Please contact administrator')
        sys.exit(2)

    #UNZIP REGISTRY
    with open(zip_file_target,'wb') as zfile:
        zfile.write(response.content)

    with zipfile.ZipFile(zip_file_target, 'r') as zip_reg:
        zip_reg.extractall(zip_registry_extract_target)

    #BEAUTIFY JSON STRUCTURE OF REGISTRY
    rfile = open(json_registry_file,'r')
    json_registry_content = json.loads(rfile.read().encode().decode('utf-8-sig'))
    rfile.close()
    rfile = open(json_registry_file,'w')

    rfile.write(json.dumps(json_registry_content,sort_keys=True, indent=4))
else:
    print('Registry already exist in cache. To reload please specify -r or --reload in options')






