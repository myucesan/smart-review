import pandas as pd
import requests
import HelperMethods
from bs4 import BeautifulSoup

# Part 1: Data Discovery | Scrape 100 reviews per hotel booking site. Do 3 hotel booking site's. Hotels , ..., ...
# TODO: Scrape more than 100 reviews.
# TODO: Multiple booking site's instead of one
# TODO: More than 100  reviews.
# TODO: Have appropriate insight in content.
# TODO: Minimum of 3, best 30 hand-written reviews
# TODO: Refactor data discovery so it can be done upon request.
# TODO: polarity (neg, neut, pos) | TextBlob, Naive Bayes
# TODO: emotion

#FIXME: null values get a language tag aswell
# r2 = reviews.loc[(reviews["language"] == "en") & (reviews["description"] != "null"), ["description", "language", "score"]]
# HelperMethods.detectPolarity(r2)  # adds a column with polarity
# r2 = pd.concat(r2, HelperMethods.detectScore(r2)) # adds a column with score label
def discoverData(hotelsComUrl):
    # Hotel_Address,Additional_Number_of_Scoring,Review_Date,Average_Score,Hotel_Name,Reviewer_Nationality,Negative_Review,Review_Total_Negative_Word_Counts,Total_Number_of_Reviews,Positive_Review,Review_Total_Positive_Word_Counts,Total_Number_of_Reviews_Reviewer_Has_Given,Reviewer_Score,Tags,days_since_review,lat,lng
    # load kaggle dataset12
    # kaggle = pd.read_csv("reviews.csv") # comment for faster processing
    # print(type(kaggle))
    # turkishhotels: https://nl.hotels.com/ho434942-tr-p3
    page = 1
    thedictionary = pd.DataFrame.from_dict(dict())
    mergeDF = []

    isRunning = True
    while isRunning:
        hotelsComReview = requests.get(hotelsComUrl + str(page))
        if hotelsComReview.status_code == 200:
            print("The page has been requested succesfully.")
            soup = BeautifulSoup(hotelsComReview.content, "html.parser")
            reviewers = soup.find_all(attrs={"class": "reviewer"})
            if len(reviewers) != 0:
                review_desc = soup.find_all(attrs={"class": "description"})
                review_score = soup.select(".review-card .rating-score")
                thedict = HelperMethods.makeDict(HelperMethods.reviewToDict("name", reviewers), HelperMethods.reviewToDict("description", review_desc), HelperMethods.reviewToDict("score", review_score))
                df = pd.DataFrame.from_dict(thedict)
                mergeDF.append(df)
            else:
                isRunning = False
                print("No more pages.")
                thedictionary = pd.concat(mergeDF)
        page = page + 1
    
    return thedictionary