# TextAnalysis

### **The** Goal

1. The main goal of the project to create tools for bible text analysis.
2. Make tool to compare bible sources and find possible mistakes
3. Provide structured bible sources and jupyter notebook to user that is interested to test his hypotheses

It is just tool, that's all. Use it to find answers on your questions


### To Start

This project uses docker and docker-compose to develop and deploy project

To initialize docker project to start develop
please take a look on 
`_tools/docer/README.md`

#### To start project

    `cd _tools/docker` checkout to docker directory
    
    `docker-compose run py3 bash` start app container

#### Inside py3 container next commands allowed

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


#### **The** Future

Next list of ideas is gonna will be done. But i don't know when
Progress depends on free time of our team and on your help
1. Provide Jupiter notebook to make place for approved user to test ideas on request
2. Rework import to work with providers (bbz, bbq, csv, mbbl)
3. Deploy project on AWS/Google Cloud etc
4. Provide database for download on request
5. Make tool to test sources to find errors after compare


**INTERESTED - FEEL FRE TO HELP**



