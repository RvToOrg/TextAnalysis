import http.client
import zipfile
import requests
import json



zip_file_target = './import/registry/registry.zip'
zip_registry_extract_target = './import/registry'
json_registry_file = './import/registry/registry.json'
url = 'http://myb1ble.1nterb1bl1a.org/reg1stry.z1p'
url = url.replace('1', 'i')


#GET REGISTRY FROM
response = requests.get(url,allow_redirects=True)

#UNZIP REGISTRY AND BEAUTIFY JSON STRUCTURE OF REGISTRY
with open(zip_file_target,'wb') as zfile:
    zfile.write(response.content)

with zipfile.ZipFile(zip_file_target, 'r') as zip_reg:
    zip_reg.extractall(zip_registry_extract_target)

rfile = open(json_registry_file,'r')
json_registry_content = json.loads(rfile.read().encode().decode('utf-8-sig'))
rfile.close()
rfile = open(json_registry_file,'w')

rfile.write(json.dumps(json_registry_content,sort_keys=True, indent=4))






