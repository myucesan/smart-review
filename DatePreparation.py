
import pandas as pd
import DataDiscovery
def getLabeledData():
    #################### Fixing Kaggle Dataset here #############################
    print("Ontaining and preparing data")
    kaggle = pd.read_csv("reviews.csv")
    kaggleNegative = kaggle["Negative_Review"].to_frame().rename(columns={"Negative_Review": "Review"})
    kaggleNegative["Label"] = 0
    kagglePositive = kaggle["Positive_Review"].to_frame().rename(columns={"Positive_Review": "Review"})
    kagglePositive["Label"] = 1
    # reviews = DataDiscovery.discoverData('https://nl.hotels.com/ho475591-tr-p')
    reviews = DataDiscovery.discoverData('https://nl.hotels.com/ho495663-tr-p')
    reviews["Label"] = reviews["score"].apply(lambda x: 1 if float(x.replace(",", ".")) >= 6 else 0)
    reviews = reviews.drop(["name", "score"], axis=1)
    reviews = reviews.rename(columns={"description": "Review"})

    endResult = pd.concat([reviews, kaggleNegative, kagglePositive])


    return endResult