import json
import pandas

def run(xlsx: str) -> str:
    """ convert xlsx to json """
    df = pandas.read_excel(xlsx, engine="openpyxl")
    df = df.rename(columns = lambda a: a.replace(" ", "_"))

    return df.to_json(orient = "records")
