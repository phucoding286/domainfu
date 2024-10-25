from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier


class PredictDomainRDFR:

    def __init__(self, path_train="train_v2.txt", num_models=4):
        self.path_train = path_train
        self.num_models = num_models
    

    # chuẩn bị data
    def read_train(self):
        X_train, y_train = [], []
        with open(self.path_train, "r", encoding="utf-8") as file:
            data = file.read().splitlines()

            for info in data:
                X_train.append(" - ".join(info.split(" - ")[:-1]))
                y_train.append(info.split(" - ")[-1])

        return [X_train], y_train
    
    
    # mô hình dự đoán
    def predict(self, domain_info):
        X_train, y_train = self.read_train()

        # mô hình mã hóa túi từ
        bow_transformer = CountVectorizer(analyzer="char")
        X_train = bow_transformer.fit_transform(X_train[0]).toarray()
        
        random_forest = RandomForestClassifier()

        # mô hình hội quyết định
        voting_model = VotingClassifier(estimators=[(f"random forest {str(i)}", random_forest) for i in range(self.num_models)], voting="hard")
        
        # training mô hình hội quyết định
        voting_model.fit(X_train, y_train)

        # dự đoán với x đầu vào
        X_test = bow_transformer.transform([domain_info]).toarray()
        predict = voting_model.predict(X_test)

        return predict[0]