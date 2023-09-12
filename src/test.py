# factorial.py 

'''
import time   

final_list = []    

def factorial(n):   
    time.sleep(.1)   
    factorial = 1   
    for i in range (1,n+1):   
        factorial = factorial * i   
    return factorial     

def sum_factorial():  
    for i in range(50):   
        final_list.append(factorial(i))    
    result=sum(final_list)    
    print("Final SUM = {}".format(result)) 
    return result

if __name__ == "__main__": 

    sum_factorial()  
    print("Testing")
'''

import os
from os import environ
import dotenv
from dotenv import load_dotenv
load_dotenv()



# Access environment variables
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


import logging

#import mypackage.package_1
#mypackage.package_1.reading_json_file('data.json')

from mypackage.package_1 import reading_json_file

def printing():
    logging.warning('Watch out!')
    return reading_json_file('././data/data.json')

if __name__ == '__main__':
    printing()

api_key = os.getenv('API_KEY')


print(api_key)
print(os.environ['local_development'])