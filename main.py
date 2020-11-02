import joblib
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from joblib import dump, load
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from stopwatch import Stopwatch
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import DataDiscovery
import HelperMethods
import DatePreparation
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk import tokenize
from sklearn.linear_model import LogisticRegression
from langdetect import detect_langs

# data = DatePreparation.getLabeledData()
# HelperMethods.storeTable(data, "Reviews")

##

df = HelperMethods.query("Get_Reviews", 50000)
df = pd.DataFrame(df, columns=["Review", "Label"])

stopwatch = Stopwatch()
stopwatch.start()
print("Start lemmatizing")
WNlemmatizer = WordNetLemmatizer()

tokenized = df.apply(lambda row: tokenize.word_tokenize(row['Review']), axis=1)
lem_tokens = []
text = ""
for tokenize in tokenized:
    list = []
    for token in tokenize:
        list.append(WNlemmatizer.lemmatize(token))
    lem_tokens.append(list)

end_df = []
for review in lem_tokens:
    end_df.append(" ".join(review))
end_df = pd.DataFrame(end_df, columns=["Review"])
end_df["Label"] = df["Label"]

vectorizer = CountVectorizer(max_features=100, ngram_range=(1,1), stop_words=ENGLISH_STOP_WORDS)
vectorizer.fit(df["Review"])
sparse_matrix = vectorizer.transform(df["Review"])
sparse_matrix_df = pd.DataFrame(sparse_matrix.toarray(), columns=vectorizer.get_feature_names())

end_df = pd.merge(end_df, sparse_matrix_df, right_index=True, left_index=True)
end2lol = end_df
# end2lol["Language"] = end2lol["Review"].apply(lambda x: "en" if str(detect_langs(x)[0])[0:2] == "en" else "null")
end2lol = end2lol[(end2lol["Review"] != "No Negative")]
end2lol = end2lol[end2lol["Review"] != "No Positive"]
end2lol = end2lol[end2lol["Review"] != "null"]
end2lol = end2lol[end2lol["Review"] != "Nothing"]
end_df = end2lol
# str(detect_langs(text)[0])[0:2]
# print(str(detect_langs("Hello world how are you")[0])[0:2])
end_df = end_df.drop('Review', axis=1)

wordcloud = WordCloud(background_color="white", max_words=100000, contour_width=3, contour_color='firebrick', width=800, height=400).generate(str(df["Review"].values))
wordcloud.to_file("wordcloud.jpg")


y = end_df["Label"].values
X = end_df.drop("Label", axis=1).values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state= 325)

# Logictic Regression
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict((X_test))
y_pred_prob = log_reg.predict_proba(X_test)[:,1]


print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
joblib_file = "logreg_model.pkl"
joblib.dump(log_reg, joblib_file)
# Decision Trees
dec_tree = tree.DecisionTreeClassifier()
dec_tree.fit(X_train, y_train)
dec_tree_y_pred = dec_tree.predict((X_test))
dec_tree_prob = dec_tree.predict_proba(X_test)[:,1]
print(classification_report(y_test, dec_tree_y_pred))
print(confusion_matrix(y_test, dec_tree_y_pred))

joblib_file = "dectree_model.pkl"
joblib.dump(log_reg, joblib_file)
# Naive Bayes Multinomial
naive_bayes = MultinomialNB()
naive_bayes.fit(X_train, y_train)
naive_bayes_y_pred = naive_bayes.predict(X_test)
naive_bayes_prob = naive_bayes.predict_proba(X_test)[:,1]
print(classification_report(y_test, naive_bayes_y_pred))
print(confusion_matrix(y_test, naive_bayes_y_pred))
joblib_file = "naivebayes_model.pkl"
joblib.dump(log_reg, joblib_file)
