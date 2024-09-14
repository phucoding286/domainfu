from domainfu_needed_modules.__getDomainInfomation import GetDomainInfo

class TrainingML:
    def __init__(self, path_train="./domainfu/domain_train.txt", tlds=["net", "com"]):
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
                print("vui lòng nhập số phân loại hợp lệ để training (1 hoặc 0)")
                continue
            
            train_info = GetDomainInfo().domain_information(inp_domain)

            try:
                self.save_train(train_info=train_info, binary_clsf=inp_clsf)
            except:
                input("tên file train không hợp lệ vui lòng xem lại ạ, enter để bỏ qua <_| : ")

            print("cảm ơn bạn đã cho tôi biết, tôi sẽ tốt hơn nhờ lần dạy này, tôi đã nhận được rồi nhé <3")