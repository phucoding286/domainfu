try:
    from domainfu_predict_modules_ml.__predictDomainRandomForest import PredictDomainRDFR
    from domainfu_predict_modules_ml.__predictDomainMachineLearning import PredictDomain
    from domainfu_predict_modules_ml.__predictDomainLogistic import LogisticRegression
except: pass
from domainfu_needed_modules.__getDomainInfomation import GetDomainInfo
import time
import os


class PredAgain(GetDomainInfo):
    
    def __init__(self, path_train="./needed_data/domain_train.txt", saved_file="./needed_data/domain_saved.txt", algorithm_pred="rdfr"):
        self.saved_file = saved_file
        (self.list_domain_true, self.list_domain_false) = ([], [])
        self.path_train = path_train

        if algorithm_pred == "rdfr": self.predict_model = [PredictDomainRDFR(self.path_train), print("bạn đã chọn thuật toán random forests\n".upper()), time.sleep(1)][0]
        elif algorithm_pred == "logi": self.predict_model = [LogisticRegression(self.path_train), print("bạn đã chọn thuật toán Logistic Regression\n".upper()), time.sleep(1)][0]
        elif algorithm_pred == "ml": self.predict_model = [PredictDomain(self.path_train), print("bạn đã chọn thuật toán ML kết hợp\n".upper()), time.sleep(1)][0]
        else: self.predict_model = PredictDomainRDFR(self.path_train)
        
        self.__checkExistPath__()
        self.get_predict()
        self.print_domains()


    def __checkExistPath__(self):
        for path in [self.saved_file, self.path_train]:
            if os.path.exists(path):
                print("tên tệp quan trọng tồn tại")
            else:
                input("một số tệp quan trọng không tồn tại, vui lòng liên hệ người tạo ra scripts này để tìm hiểu: (enter để đóng)")
                exit()
        print()

    
    def get_predict(self):
        with open(self.saved_file, "r", encoding="utf8") as file: domain_saved = file.read().splitlines()
        for domain_predicted in domain_saved:
            (self.list_domain_true.append(domain_predicted.split(":")[0]) if int(domain_predicted.split(":")[1]) == 1\
            else self.list_domain_false.append(domain_predicted.split(":")[0]))
        return 0
    

    def print_domains(self):
        while True:
            print("các tên miền hợp lệ")
            for v_dm in self.list_domain_true: print("\t", v_dm)
            print("các tên miền không hợp lệ")
            for v_dm in self.list_domain_false: print("\t", v_dm)

            chk_d = input("muốn dự đoán lại? (Y/n)")
            if chk_d.lower() == "y": continue
            else: break
        return 0