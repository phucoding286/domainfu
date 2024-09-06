import math

class LogisticRegression:
    def __init__(self, path_train: str):
        self.bow = []
        self.vocab = {}
        self.weights = []
        self.bias = 0.0
        self.path_train = path_train
        self.data, self.labels = self.__getData__()
    

    def __getData__(self):
        X_train, y_train = [], []
        with open(self.path_train, "r", encoding="utf-8") as file:
            data = file.read().splitlines()

            for info in data:
                X_train.append(info.split(" - ")[0])
                y_train.append(info.split(" - ")[1])

        return X_train, y_train


    def create_bow(self):
        self.bow = []
        self.vocab = {}
        for sentence in self.data:
            words = sentence.split()
            bow_sentence = {}
            for word in words:
                if word not in self.vocab:
                    self.vocab[word] = len(self.vocab)
                word_idx = self.vocab[word]
                if word_idx in bow_sentence:
                    bow_sentence[word_idx] += 1
                else:
                    bow_sentence[word_idx] = 1
            self.bow.append(bow_sentence)
    
    def train_logistic_regression(self):
        vocab_size = len(self.vocab)
        num_sentences = len(self.bow)
        self.weights = [0.0] * vocab_size
        self.bias = 0.0
        learning_rate = 0.01
        epochs = 100

        for epoch in range(epochs):
            for i in range(num_sentences):
                # Tính toán đầu ra dự đoán
                score = 0.0
                for word_idx, count in self.bow[i].items():
                    score += self.weights[word_idx] * count
                score += self.bias

                # Áp dụng hàm sigmoid
                predicted = 1.0 / (1.0 + math.exp(-score))

                # Tính gradient dựa trên cross-entropy loss
                error = predicted - self.labels[i]
                for word_idx, count in self.bow[i].items():
                    gradient = error * count
                    self.weights[word_idx] -= learning_rate * gradient
                self.bias -= learning_rate * error
    
    def predict(self, new_data):
        predictions = []
        for sentence in new_data:
            bow_sentence = {}
            words = sentence.split()
            for word in words:
                if word in self.vocab:
                    word_idx = self.vocab[word]
                    if word_idx in bow_sentence:
                        bow_sentence[word_idx] += 1
                    else:
                        bow_sentence[word_idx] = 1
            score = 0.0
            for word_idx, count in bow_sentence.items():
                score += self.weights[word_idx] * count
            score += self.bias
            predicted = 1.0 / (1.0 + math.exp(-score))
            if predicted >= 0.5:
                predictions.append(1)
            else:
                predictions.append(0)
        return predictions