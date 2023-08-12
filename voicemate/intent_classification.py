import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

class IntentClassifier:

    def __init__(self):
        self.data = pd.read_csv('data.csv') #Read the CSV file

        self.train()

    def train(self):
        X_train, y_train = self.data['text'], self.data['intent']
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts) #Calculates tf-idf for the text
        self.clf = MultinomialNB().fit(X_train_tfidf, y_train)

        #print(X_train_tfidf)
        #print(X_train_counts.toarray())
        
    def predict(self, text):
        return self.clf.predict(self.count_vect.transform([text]))[0]
    
#test
intent_classifier = IntentClassifier()