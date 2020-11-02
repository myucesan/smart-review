
import re
from textblob import TextBlob
import pandas as pd
from langdetect import detect_langs
from sqlalchemy import create_engine # pip install mysqlclient in order for sqlalchemy to use mysql drivers
from contextlib import closing


def sanitise(data):
    return re.sub(r"\['|'\]|\[\"|\"\]|\\r|\\n", "", str(data))

def reviewToDict(*args):
    completeDict = {}
    values = []
    for arg in args:
        isString = isinstance(arg, str)
        if isString == True:
            key = arg
            continue
        for item in arg:
            if(isString == False):
                item = sanitise(item.contents)
                if item == "[]":
                    item = "null"
                values.append(item)
        if len(values) != 0:
            dictize = {key : values}
            completeDict.update(dictize)
    return completeDict

def makeDict(*args):
    adict = {}
    for arg in args:
        adict.update(arg)
    return adict

# FIXME: Not always correct, double check.
# FIXME array wordt er niet goed ingezet
def detectLanguage(df):
    languages = []
    for text in df[df["description"] != "null"]["description"].values:
        languages.append(str(detect_langs(text)[0])[0:2])
    df["language"] = pd.DataFrame.from_dict(languages)

#FIXME array wordt er niet goed ingezet
def detectPolarity(df):
    sentiment = []
    for text in df[df["description"] != "null"]["description"].values:
        text = TextBlob(text).sentiment
        text = 1 if text[0] > 0 else 0
        sentiment.append(str(text))
    df["sentiment"] = pd.DataFrame.from_dict(sentiment)

#FIXME array wordt er niet goed ingezet
def detectScore(df):
    score_rate = []
    for score in df["score"].values:
        rate = 1 if ((int(score.replace(",", "")) / 10) >= 7) else 0
        score_rate.append(rate)
    print(score_rate)
    # df["score_rate"] = pd.DataFrame.from_dict(score_rate)
    lala = df["score_rate"] = pd.DataFrame.from_dict(score_rate)
    return lala


# SQL Connection
# engine = create_engine("mysql://deprak1q_deds:uibUzlt0]sqZ@depraktischewinkel.nl/deprak1q_deds_ass1")


def storeTable(df, tableName):
    engine = create_engine("mysql://deprak1q_deds2:RGDjD@%n[M&u@depraktischewinkel.nl/deprak1q_deds_ass1")
    connection = engine.connect()
    df.to_sql(tableName, engine, if_exists='fail')
    connection.close()

def query(procedureName, limito):
    engine = create_engine("mysql://deprak1q_deds2:RGDjD@%n[M&u@depraktischewinkel.nl/deprak1q_deds_ass1")
    connection = engine.connect()
    results = []
    connection = engine.raw_connection()
    try:
        print("trying")
        cursor = connection.cursor()
        limit = [limito]
        cursor.callproc(procedureName, (limit))
        results = list(cursor.fetchall())
        cursor.close()
        connection.commit()
    finally:
        connection.close()
    return results
