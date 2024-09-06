import requests
from bs4 import BeautifulSoup

class GetDomainEmailFake:
    
    def __init__(self, path_log="log_domain.txt", path_save="domain_saved.txt", path_train="domain_train.txt", tdls = ["net", "com"], day_limit=7):
        self.path_log = path_log
        self.tdls = tdls
        self.day_limit = day_limit
        self.path_train = path_train
        self.path_save = path_save


    def get_domain(self):
        while True:
            try:
                email_request = requests.get(url="https://emailfake.com/fake_email_generator")
                break
            except:
                continue

        soup = BeautifulSoup(email_request.text, "html.parser")
        domain_html = str(soup.find_all("input"))
        domain = domain_html.split('value="')[-1].split('"/>]')[0]

        return domain
    


    def check_log(self, domain: str):
        with open(self.path_log, "r", encoding="utf-8") as f:
            domains = f.read()

        if domain in domains.splitlines():
            print(f"tên miền {domain} có trong log!")
            return 0
        else:
            print(f"tên miền mới {domain}")
            return 1

    

    def check_tlds(self, domain: str):
        if domain.split(".")[1].strip() not in self.tdls:
            print(f"đuôi tên miền {domain} không thuộc vùng tên miền đã train: {self.tdls} nên sẽ được bỏ qua")
            return 0
        
        else:
            print(f"đuôi tên miền {domain} nằm trong vùng hợp lệ: {self.tdls}")
            return 1
        

    def check_up_time(self, domain: str):
        url = 'https://emailfake.com/check_adres_validation3.php'
        data = {
            'usr': 'charleswhatmore',
            'dmn': domain
        }

        while True:
            try:
                response = requests.post(url, data=data)
                break
            except:
                continue

        result = response.json()
        day = result["uptime"]

        if int(day) > self.day_limit:
            print(f"số ngày đăng tên miền {domain} quá lớn so với mức quy định {self.day_limit} nên bỏ qua!")
            return 0
        else:
            print(f"tên miền {domain} có số ngày đã đúng mức quy định {self.day_limit}!!")
            return 1
        
    
    def criteria(self):
        domain = self.get_domain()

        if self.check_log(domain) == 0:
            return 0
        
        elif self.check_tlds(domain) == 0:
            return 0
        
        elif self.check_up_time(domain) == 0:
            return 0
        
        else:
            return domain