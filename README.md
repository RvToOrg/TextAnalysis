# TextAnalysis

To initialize docker project to start develop
please take a look on 
`_tools/docer/README.md`

§. To start project:

    `cd _tools/docker` checkout to docker directory
    
    `docker-compose run py3 bash` start app container

INSIDE PY3 CONTAINER NEXT COMMANDS ALLOWED  
1. This tool allows to fetch module registry

    To load registry run `python3 import/get_registry.py`
    
    To update cached registry run `python3 import/get_registry.py -r`

2. Fetch any module described in registry to pgsql database

    To load module run `python3 import/get_module.py -m MODULE_NAME`
    
    To update cached module run `python3 import/get_module.py -m MODULE_NAME -r`

3. Parse bible verses to words

    To parse module verses to word use `python3 import/get_parsed_words.py -m MODULE_NAME`


**To connect to database that contains loaded module and parsed words
use connection described in `_tools/docker/README`**

