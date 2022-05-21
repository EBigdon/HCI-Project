import pandas as pd
import pickle

from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

def generateModel(csv_data, model_file):
    df = pd.read_csv(csv_data) #readsData

    X = df.drop('class', axis=1) #splits data into X=Data and y=Label
    y = df['class']

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)
    #X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    X = StandardScaler().fit_transform(X)

    clf = SVC(C=1.0, kernel='rbf').fit(X_train,y_train)
    with open(model_file, 'wb') as f:
        pickle.dump(clf, f)

    pipelines = {
       'lr':make_pipeline(StandardScaler(), LogisticRegression()),
       'rc':make_pipeline(StandardScaler(), RidgeClassifier()),
       'rf':make_pipeline(StandardScaler(), RandomForestClassifier()),
       'gb':make_pipeline(StandardScaler(), GradientBoostingClassifier()),
    }

    fit_models = {}
    for algo, pipeline in pipelines.items():
       model = pipeline.fit(X_train, y_train)
       fit_models[algo] = model

    fit_models['rc'].predict(X_test)

    for algo, model in fit_models.items():
        yhat = model.predict(X_test)
        #print(algo, accuracy_score(y_test, yhat))

    fit_models['rf'].predict(X_test)

    with open(model_file, 'wb') as f:
        pickle.dump(fit_models['rf'], f)
