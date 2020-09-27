import HelperMethods
from bs4 import BeautifulSoup
import pandas as pd
import requests
from collections import defaultdict


# Part 1: Data Discovery | Scrape 100 reviews per hotel booking site. Do 3 hotel booking site's. Hotels , ..., ...
# TODO: For sentiment analysis we kight have trouble with multiple languages, check later.

page = 1
hotelsComReview = requests.get('https://nl.hotels.com/ho434942-tr-p' + str(page))
# Hotel_Address,Additional_Number_of_Scoring,Review_Date,Average_Score,Hotel_Name,Reviewer_Nationality,Negative_Review,Review_Total_Negative_Word_Counts,Total_Number_of_Reviews,Positive_Review,Review_Total_Positive_Word_Counts,Total_Number_of_Reviews_Reviewer_Has_Given,Reviewer_Score,Tags,days_since_review,lat,lng
# load kaggle dataset12
# kaggle = pd.read_csv("reviews.csv") # comment for faster processing
# print(type(kaggle))

if hotelsComReview.status_code == 200:
    print("The page has been requested succesfully.")
    soup = BeautifulSoup(hotelsComReview.content, "html.parser")
    reviewers = soup.find_all(attrs={"class": "reviewer"})
    review_desc = soup.find_all(attrs={"class": "description"})
    review_score = soup.find_all(attrs={"class": "rating-score"})

    thedictionary = HelperMethods.makeDict(HelperMethods.reviewToDict("name", reviewers), HelperMethods.reviewToDict("name", reviewers), HelperMethods.reviewToDict("description", review_desc), HelperMethods.reviewToDict("score", review_score))
    
    # thedictionary = pd.DataFrame.from_dict(thedictionary)
    print(thedictionary)


