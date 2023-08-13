import pandas as pd #pip3 install pandas
from sklearn.feature_extraction.text import CountVectorizer #pip3 install scikit-learn
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

#Trains the systen to predict user intent based on some trained data

class IntentClassifier:

    def __init__(self):
        """
        Initialization function when an instance of the class
        is created
        """
        self.data = pd.read_csv('data.csv') #Reads the CSV file

        self.train()

    def train(self):
        X_train = self.data['text']
        y_train = self.data['intent']
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
sample_cls = IntentClassifier()

#print systeminfo
text = "Hey, what's good?"
print(sample_cls.predict(text))
