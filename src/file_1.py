import os
from os import environ
import logging
import dotenv
from dotenv import load_dotenv
from mypackage.package_1 import reading_json_file
from mypackage.package_1 import log

load_dotenv()

def printing():
    logging.warning('Watch out!')
    return reading_json_file('./data/data.json')

if __name__ == '__main__':
    print(printing())
    log('sdsdsd')
    api_key = os.getenv('API_KEY')
    print(api_key)
    print(os.environ['local_development'])






