import getopt, sys, os
import requests, zipfile
import json, re
from peewee import *


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
print('DB used '+db_name)

db_configs = './import/configs/db_config.json'
db_configs = json.loads(open(db_configs,'r').read().encode().decode('utf-8-sig'))


# DB STRUCTURE
psql_db = PostgresqlDatabase(db_name, user=db_configs['user'],host=db_configs['host'],port=db_configs['port'],password=db_configs['pass'])

class BaseModel(Model):
    class Meta:
        database = psql_db

class Verse(BaseModel):
    book_number=DecimalField()
    chapter=DecimalField()
    verse=DecimalField()
    text=TextField(null=True)

    class Meta:
        primary_key = False
        db_table='verses'

class Word(BaseModel):
    book_number=IntegerField()
    chapter=IntegerField()
    verse=IntegerField()
    word_number=IntegerField()
    words=FixedCharField(null=True, max_length=256)
    strong=IntegerField(null=True)

    class Meta:
        primary_key = False
        db_table='words'


# CREATE TABLE WORDS IF NOT EXIST
try:
    psql_db.connect()
    Word.drop_table()
    Word.create_table()
except InternalError as px:
    print(str(px))
print('Words table dropped and created')

# sys.exit(0)


# PARSE MODULE VERSE TO WORDS BY STRONG
limit= 200
verses_count = Verse.select().count()
print('Total count of verses: {}'.format(verses_count))


parsed = 0
while parsed<verses_count:
    verses = Verse.select().limit(limit).offset(parsed).execute()
    data = []
    for verse in verses:
        parsed+=1
        # remove bad tags
        text = re.sub(r'(<[ikhfnm]>.*?</[ikhfnm]>)?(<pb/>)?(<br/>)?(</?[teJ]>)?','',verse.text, flags=re.IGNORECASE)
        # cleanup text from bad tags
        elements =[re.split(r'<s>',x.strip(),flags=re.IGNORECASE) for x in re.split(r'</s>',text, flags=re.IGNORECASE) if x.strip()]

        if parsed % 100 == 0:
            print('{} verses parsed from {}'.format(parsed,verses_count))
        number = 0
        for el in elements:
            data.append({
                "book_number":verse.book_number,
                "chapter":verse.chapter,
                "verse":verse.verse,
                "word_number":number,
                "words":el[0].strip(),
                "strong":int(el[1].strip()) if len(el)>1 else None,
            })
            # row = Word(
            #     book_number=verse.book_number,
            #     chapter=verse.chapter,
            #     verse=verse.verse,
            #     word_number=number,
            #     words=el[0].strip(),
            #     strong= int(el[1].strip()) if len(el)>1 else None
            # )
            # row.save()
            number+=1
    Word.insert_many(data).execute()

print('Verses parse finished.')

