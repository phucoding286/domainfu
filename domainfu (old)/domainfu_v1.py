from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import platform
import os
from whois import whois


# chat nhận diện lệnh
class CommandUiChatQality:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def predict(self, inputs):
        random_forest = RandomForestClassifier()
        bow_transformer = CountVectorizer(analyzer="char")
        X_train = bow_transformer.fit_transform(self.x[0]).toarray()
        random_forest.fit(X_train, y=self.y)
        X_test = bow_transformer.transform(inputs)
        y_pred = random_forest.predict(X_test)
        return y_pred[0]

# dữ liệu train cho mô hình chat nhận diện lệnh
user_command = [["1", "tôi muốn chạy tool","chạy tool", "run tool đi", "kích hoạt tool",
                "bật đào tạo", "đào tạo bạn", "training", "2",
                "tải gói", "install package", "tải", "tải gói cho tool",
                "dự đoán tên miền", "dự đoán tên miền lẻ", "dự đoán miền", "đoán domain",
                "file predict", "dự đoán file", "đoán từ file", "đoán trong tệp", "dự đoán tệp"]]

predict_command = ["run tool", "run tool", "run tool", "run tool", "run tool",
             "training", "training", "training", "training",
             "install pack", "install pack", "install pack", "install pack",
              "domain predict", "domain predict", "domain predict", "domain predict",
              "file predict", "file predict", "file predict", "file predict", "file predict"]

def command_ui():
    path_log = "log.txt"
    path_save = "saved.txt"
    path_train = "train.txt"
    tlds = ["net", "com"]

    if not os.path.exists(path_log) \
            or not os.path.exists(path_save) \
            or not os.path.exists(path_train):
        print("chưa có các file cần thiết, tiến hành tạo ...")
        for path in [path_log, path_save, path_train]:
            with open(path, mode="a"):
                continue
    else:
        print("đã có đầy đủ file cần thiết")

    print("\n*Domain-FU công cụ AI phân tích tên miền thế hệ đầu")
    print("-For CloudSigma Service-")
    print("* lưu ý: train cho ireland\n- chạy tool\n- training cho nó\n- tải gói để chạy")
    print("- dự đoán tên miền\n- dự đoán hàng loạt từ tệp\n")

    inp = input("chọn 1 trong những lựa chọn trên : ")
    cm_pred = CommandUiChatQality(x=user_command, y=predict_command).predict([inp])
    print(f"đã hiểu, bạn muốn : {cm_pred}\n")

    if cm_pred in "run tool":
        while True:
            try:
                for _ in range(100):
                    run_tool = RunTool(path_log=path_log, path_save=path_save, path_train=path_train, tlds=tlds)
                    run_tool.run()
                    del(run_tool, _)
            except:
                continue

    elif cm_pred in "training":
        TrainingToolPredict().clasify_via_chatui()
    
    elif cm_pred in "install pack":
        InstallPackage().command_ui()
    
    elif cm_pred in "domain predict":
        PredictDomainByDomain(tlds=tlds, path_train=path_train).predict()

    elif cm_pred in "file predict":
        PredictFromFile().predict_file(path_save=path_save, path_train=path_train)


system_name = platform.system()

class TrainingToolPredict:
    def __init__(self, path_train="train.txt", tlds=["net", "com"]):
        self.path_train = path_train
        self.tlds = tlds

    def save_train(self, train_info, binary_clsf):
        with open(self.path_train, mode="a", encoding="utf-8") as file:
            file.write(f"{train_info} - {binary_clsf}\n")
    
    def clasify_via_chatui(self):
        while True:
            inp_domain = input("nhập vào đây tên miền mà bạn muốn training : ").lower().strip()
            if inp_domain.split(".")[1] not in self.tlds:
                print(f"xin hãy nhập tên miền hợp lệ đúng với các tlds sau {self.tlds}")
                continue
            inp_clsf = input("nhập vào đây 1 / 0 : ")
            if inp_clsf not in ["1", "0"]:
                os.system("cls") if system_name in "Windows" else os.system("clear") 
                print("vui lòng nhập số phân loại hợp lệ để training (1 hoặc 0)")
                continue
            
            train_info = GetDomainInfo().domain_information(inp_domain)

            try:
                self.save_train(train_info=train_info, binary_clsf=inp_clsf)
            except:
                input("tên file train không hợp lệ vui lòng xem lại ạ, enter để bỏ qua <_| : ")

            os.system("cls") if system_name in "Windows" else os.system("clear") 
            print("cảm ơn bạn đã cho tôi biết, tôi sẽ tốt hơn nhờ lần dạy này, tôi đã nhận được rồi nhé <3")

class StorageDomain:
    def __init__(self, path_save=None):
        self.path_save = path_save
    
    def save_domain(self, domain, clsf: int):
        if self.path_save is None:
            with open("saved.txt", mode="a", encoding="utf-8") as file:
                file.write(f"{domain} : {clsf}\n")
        else: 
            with open(self.path_save, mode="a", encoding="utf-8") as file:
                file.write(f"{domain} : {clsf}\n")

class RunTool:
    def __init__(self, path_save=None, path_train="train.txt", path_log="log.txt", tlds=["net", "com"]):
        self.path_train = path_train
        self.path_log = path_log
        self.tlds = tlds
        self.path_save = path_save

    def run(self):
        good_domain, bad_domain = DomainFinding(path_log=self.path_log, tlds=self.tlds).get_domains()
        for domain in good_domain:
            while True:
                domain_info = GetDomainInfo(tlds=self.tlds).domain_information(domain=domain)
                if domain_info in "error":
                    continue
                else:
                    break
            domain_pred = PredictDomain(path_train=self.path_train).predict(domain=domain)
            if str(domain_pred) in "1":
                StorageDomain(path_save=self.path_save).save_domain(domain=domain, clsf=1)
            else:
                StorageDomain(path_save=self.path_save).save_domain(domain=domain, clsf=0)

class PredictFromFile:
    def predict_file(self, path_save, path_train):
        with open(path_save, mode="r", encoding="utf-8") as file:
            domains = file.read().splitlines()
        for i in range(len(domains)):
            domains[i] = domains[i].split(" : ")[0]
        
        domain_predict = PredictDomain(path_train=path_train)
        for domain in domains:
            try:
                y_pred = domain_predict.predict(domain=domain)
                print(f"{domain} kết quả: {y_pred}")
            except:
                print(f"tên miền {domain} đã có lỗi")
                continue
        input("đã xong, nhấn enter để quay lại console : ")

class PredictDomain:
    def __init__(self, path_train="train.txt"):
        self.path_train = path_train
    
    def read_train(self):
        X_train, y_train = [], []
        with open(self.path_train, "r", encoding="utf-8") as file:
            data = file.read().splitlines()
            for info in data:
                X_train.append(info.split(" - ")[0])
                y_train.append(info.split(" - ")[1])
        return [X_train], y_train
    
    def predict(self, domain):
        domain_info = GetDomainInfo().domain_information(domain=domain)
        X_train, y_train = self.read_train()
        bow_transformer = CountVectorizer(analyzer="char")
        X_train = bow_transformer.fit_transform(X_train[0]).toarray()
        desicion_tree = DecisionTreeClassifier()
        random_forest = RandomForestClassifier()
        bayes_model = GaussianNB()
        svm_model = SVC(probability=True)
        knn_model = KNeighborsClassifier(n_neighbors=3)
        voting_model = VotingClassifier(estimators=[("desicion tree", desicion_tree),
                                                    ("random forest", random_forest),
                                                    ("svm", svm_model),
                                                    ("knn", knn_model),
                                                    ("bayes", bayes_model)], voting="soft")
        voting_model.fit(X_train, y_train)
        X_test = bow_transformer.transform([domain_info]).toarray()
        predict = voting_model.predict(X_test)
        return predict[0]

class PredictDomainByDomain:
    def __init__(self, path_train, tlds):
        self.tlds = tlds
        self.path_train = path_train

    def predict(self):
        print("xin chào bạn bạn có thể dùng tôi để dự đoán từng domain lẻ tại đây ^.^")
        while True:
            inp = input("nhập domain mà bạn muốn dự đoán : ").lower().strip()
            try:
                if inp.split(".")[1] not in self.tlds:
                    os.system("cls") if system_name in "Windows" else os.system("clear") 
                    print("vui lòng nhập tên miền có trong giới hạn của tlds", 
                          f" đây là giới hạn mà mô hình đã được đào tạo : {self.tlds}")
                    continue
            except:
                os.system("cls") if system_name in "Windows" else os.system("clear") 
                print("vui lòng nhập tên miền hợp lệ đi ạ")
                continue
            predict_result = PredictDomain(path_train=self.path_train).predict(domain=inp)
            os.system("cls") if system_name in "Windows" else os.system("clear") 
            print(f"kết quả dự đoán : {predict_result}")

class InstallPackage:
    def install_package(self, path_pip: str):
        install_command = f"{path_pip} install -r requirements.txt"
        out_cmd = os.system(str(install_command))
        if out_cmd == 1:
            print(f"đã có lỗi khi tải gói thư viện mã lỗi như sau: {out_cmd}")
            return False
        return True
    
    def driver_install(self, command: str):
        command = command.lower().strip()
        if command in ["chrome", "chrome driver"]:
            try:
                chrome_driver_install = ChromeDriverManager().install()
                print("bạn đã hoàn thành tải chrome driver mà không gặp vấn đề gì!")
                print(f"đường dẫn của driver: {chrome_driver_install}")
            except Exception as error:
                print(f"driver tải không thành công mã lỗi như sau: {error}")
                return False

        elif command in ["firefox", "firefox driver"]:
            try:
                firefox_driver_install = GeckoDriverManager().install()
                print("bạn đã hoàn thành tải firefox driver mà không gặp vấn đề gì!")
                print(f"đường dẫn của driver: {firefox_driver_install}")
            except Exception as error:
                print(f"driver tải không thành công mã lỗi như sau: {error}")
                return False

        elif command in ["edge", "edge driver"]:
            try:
                edge_driver_install = EdgeChromiumDriverManager().install()
                print("bạn đã hoàn thành tải edge driver mà không gặp vấn đề gì!")
                print(f"đường dẫn của driver: {edge_driver_install}")
            except Exception as error:
                print(f"driver tải không thành công mã lỗi như sau: {error}")
                return False
        else:
            print("bạn vui lòng nhập đúng lệnh!")
            return False
        return True
    
    def command_ui(self):
        chk_align = False
        while True:
            if not chk_align:
                print('*gợi ý: bạn nên dùng lệnh "where pip" để tìm kiếm đường dẫn pip')
                pip_input = input("vui lòng nhập lệnh pip hoặc đường dẫn pip của bạn để cài gói thư viện cho tool: ")
                pip_input = pip_input.strip()
                install_pack_output = self.install_package(pip_input)
                if not install_pack_output:
                    continue

            chk_align = True
            
            print('*gợi ý: bạn có thể nhập lệnh "edge" hoặc "edge driver" nếu trên máy của bạn có trình duyệt edge')
            print('hoặc bạn có thể dùng lệnh "chrome" hoặc "chrome driver" nếu trên máy của bạn chỉ có chrome')
            print("và tương tự với firefox")
            command_input = input("nhập tên driver của bạn để chúng tôi có thể tải cho bạn: ")
            command_input = command_input.lower().strip()
            driver_install_output = self.driver_install(command_input)
            if not driver_install_output:
                continue

            break

class GetDomainInfo:
    def __init__(self, tlds=["net", "com"]):
        self.tlds = tlds

    def domain_information(self, domain):
        try:
            domain_infomations = whois(domain)
        except:
            return "error"
        
        keys = ["domain_name", "registrar", "whois_server", "referral_url", "updated_date", "creation_date",
                "expiration_date", "name_servers", "status", "emails", "dnssec", "name", "org", "address",
                "city", "state", "registrant_postal_code", "country"]
        update_domain_infomation = ""
        for key in keys:
            update_domain_infomation += str(f"{domain_infomations[key]}, ")
        for tld in self.tlds:
            if domain.split(".")[1] in tld:
                update_domain_infomation = update_domain_infomation+tld
                break
        return update_domain_infomation

class DomainFinding:
    def __init__(self, path_log="log.txt", tlds=["net", "com"]):
        assert isinstance(tlds, list), "chúng tôi cần 1 danh sách chứa các .net hoặc .com để phân loại"
        self.path_log = path_log
        self.tlds = tlds

    def setup_browser(self):
        option = Options()
        option.add_argument("--log-level=3")
        option.add_argument("--headless=new")
        browser = webdriver.Chrome(options=option)
        os.system("cls") if system_name in "Windows" else os.system("clear")
        return browser
    
    def finding_domain(self):
        browser = self.setup_browser()
        domains, uptimes = [], []
        for i in range(20):
            try:
                browser.get("https://emailfake.com/fake_email_generator")
                email = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email_ch_text"]'))).text
                domain = email.split("@")[1]

                uptime_text = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkdomainset"]'))).text
                uptime = uptime_text.split()[4]

                domains.append(domain)
                uptimes.append(uptime)

                print(f"{i+1} - {domain} - {uptime} days")

            except Exception as e:
                print(f"mã lỗi: {e}")
                browser.quit()
                return domains, uptimes
            
        browser.quit()
        return domains, uptimes
    
    def check_log(self, domain):
        with open(self.path_log, mode="r", encoding='utf-8', errors="ignore") as file:
            data_logs = file.read().splitlines()
        if domain not in data_logs:
            return True
        else:
            return False
        
    def check_tld(self, domain):
        if domain.split(".")[1] in self.tlds:
            return True
        else:
            return False
    
    def check_uptime(self, uptime):
        if int(uptime) <= 7:
            return True
        else:
            return False
        
    def save_log(self, domain):
        with open(self.path_log, mode="a", encoding='utf-8', errors="ignore") as file:
            file.write(domain+"\n")
    
    def get_domains(self):
        domains, uptimes = self.finding_domain()
        good_domain_filtered, bad_domain_filtered = [], []
        for i in range(len(domains)):
            check_log = self.check_log(domain=domains[i])
            check_tld = self.check_tld(domain=domains[i])
            check_uptime = self.check_uptime(uptime=uptimes[i])
            if check_log == True and check_tld == True and check_uptime == True:
                self.save_log(domain=domains[i])
                good_domain_filtered.append(domains[i])
            else:
                bad_domain_filtered.append(domains[i])
        return good_domain_filtered, bad_domain_filtered
    
if __name__ == "__main__":
    while True:
        command_ui()