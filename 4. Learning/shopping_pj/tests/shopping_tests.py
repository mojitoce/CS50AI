from nose.tools import *
from shopping import shopping
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

filename = 'shopping/shopping.csv'
TEST_SIZE = 0.3

evidence, labels = shopping.load_data(filename)

X_train, X_test, y_train, y_test = train_test_split(
    evidence, labels, test_size=TEST_SIZE
)

model = shopping.train_model(X_train, y_train)
predictions = model.predict(X_test)

print(predictions)
