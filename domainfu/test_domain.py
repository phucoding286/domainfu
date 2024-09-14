from __predictDomainRandomForest import PredictDomain
from __getDomainInfomation import GetDomainInfo

predictor = PredictDomain(path_train="./domainfu/domain_train.txt")
informator = GetDomainInfo()

while True:
    inp = input("nhập tên miền của bạn: ")
    domain_info = informator.domain_information(inp)
    output = predictor.predict(domain_info)
    print(output)