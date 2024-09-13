from __domainFindingRandomForest import PredictDomain
from __getDomainOnEmailFake import GetDomainEmailFake
from __getDomainInfomation import GetDomainInfo
import threading
import os

class DomainFind:
    
    def __init__(self, path_log="./domainfu/log_domain.txt", path_save="./domainfu/domain_saved.txt",
            path_train="./domainfu/domain_train.txt", tdls = ["net", "com"], day_limit=7):
        
        self.path_log = path_log
        self.tdls = tdls
        self.day_limit = day_limit
        self.path_train = path_train
        self.path_save = path_save

        self.predict_model = PredictDomain(self.path_train)
        self.get_domain_on_emailfake = GetDomainEmailFake(path_log, path_save, path_train, tdls, day_limit)
        self.get_domain_info = GetDomainInfo(tdls)
        
        self.__infoCreators__()
        self.__checkExistPath__()

    
    def __infoCreators__(self):
        print("scripts created by Phu Tech")
        print("facebook: https://www.facebook.com/profile.php?id=61562099241369")
        print("youtube: https://www.youtube.com/@phucoding286")
        print("github: https://github.com/phucoding286")
        print()


    def __checkExistPath__(self):
        for path in [self.path_save, self.path_log, self.path_train]:
            if os.path.exists(path):
                print("tên tệp quan trọng tồn tại")
            else:
                input("một số tệp quan trọng không tồn tại, vui lòng liên hệ người tạo ra scripts này để tìm hiểu: (enter để đóng)")
                exit()
        print()


    def predict_domain(self, domain: str):
        domain_info = self.get_domain_info.domain_information(domain)
        try:
            predict = self.predict_model.predict(domain_info)
        except Exception as error:
            print(f"có 1 chút lỗi ở phần dự đoán nên chạy lại mã lỗi là: {error}")
            return 0
        
        if str(predict) in '1':
            with open(self.path_save, "a", encoding='utf8') as f:
                f.write(f"{domain} : 1\n")

            with open(self.path_log, "a", encoding="utf8") as f:
                f.write(f"{domain}\n")

            print(f"domain {domain} có vẻ ngon nên đã lưu lại.")
            print(f"và đã lưu domain {domain} vào log")

        else:
            with open(self.path_log, "a", encoding="utf8") as f:
                f.write(f"{domain}\n")
            
            with open(self.path_save, "a", encoding='utf8') as f:
                f.write(f"{domain} : 0\n")

            print(f"đã lưu domain {domain} vào log")
    


    def criteria(self):
        criter = self.get_domain_on_emailfake.criteria()
        if criter != 0:
            self.predict_domain(criter)
    


    def run_script(self, thr=50):
        threads = []
        for _ in range(thr):
            thread = threading.Thread(target=self.criteria)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

    
    def run_all_script(self):
        print("*BETA version")
        print("*Công cụ AI phân tích tên miền Domain-FU thế hệ thứ 2 với các cập nhật về tốc độ tìm kiếm và dự đoán tên miền ^_+")
        print("-For CloudSigma Service-")
        c = False
        while True:
            if c is False:
                try:
                    inp_t = int(input("nhập số luồng của bạn: ").strip())
                    c = True
                except:
                    print("vui lòng nhập số nguyên (số luồng)")
                    continue
            self.run_script(inp_t)
