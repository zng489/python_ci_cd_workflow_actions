import pandas as pd

def reading_json_file(x):
    df = pd.read_json(x)
    return df