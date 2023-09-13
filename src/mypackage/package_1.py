import pandas as pd
import logging
import os

path_log = os.path.dirname("././src/log/")

def reading_json_file(x):
    df = pd.read_json(x)
    return df


def log(message):

    # Define the directory for the log file
    log_dir = '../log/'

    # Create the directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Define the path for the log file
    log_file = os.path.join(log_dir, 'log.txt')

    # Create a logger
    logger = logging.getLogger('my_logger')
    # Set the level of this logger. This means that only events of this level and above will be tracked.
    logger.setLevel(logging.DEBUG)

    # Create a file handler that logs debug and higher level log messages to a file.
    file_handler = logging.FileHandler(log_file)

    # Create a formatter that specifies the format of the log messages.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the file handler.
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger.
    logger.addHandler(file_handler)

    # Log some messages
    #logger.debug('This is a debug message')
    #logger.info('This is an info message')
    #logger.warning('This is a warning message')
    #logger.error('This is an error message')
    #logger.critical('This is a critical message')

    return logger.warning(message) 

if __name__ == '__main__':
    log('asdasd')