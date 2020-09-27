from bs4 import BeautifulSoup
import pandas as pd
import requests

# Part 1: Data Discovery | Scrape 100 reviews per hotel booking site. Do 3 hotel booking site's. Booking, Trivago, 
bookingPage = requests.get("https://www.booking.com/reviewlist.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaKkBiAEBmAExuAEHyAEP2AEB6AEB-AECiAIBqAIDuAKw0o_7BcACAdICJDRiNmJkZDBmLTNjZmYtNDlkZC05MzRhLTM5MWE2M2ZjYTY2MtgCBeACAQ&sid=e76d27d037651f4921a5a8a6c425330f&cc1=tr&dist=1&pagename=silence-istanbul&srpvid=65e5a1203c000028&type=total&offset=10&rows=10")
# Hotel_Address,Additional_Number_of_Scoring,Review_Date,Average_Score,Hotel_Name,Reviewer_Nationality,Negative_Review,Review_Total_Negative_Word_Counts,Total_Number_of_Reviews,Positive_Review,Review_Total_Positive_Word_Counts,Total_Number_of_Reviews_Reviewer_Has_Given,Reviewer_Score,Tags,days_since_review,lat,lng
# load kaggle dataset
kaggle = pd.read_csv("reviews.csv") 
print(bookingPage)
if bookingPage.status_code == 200:
    print("The page has been requested succesfully.")
    soup = BeautifulSoup(bookingPage.content, "html.parser")
    print(soup.prettify())
    review = soup.find_all(class_="bui-avatar-block__title")
    print(review)

    
