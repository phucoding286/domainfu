from __trainingMLPredictDomain import TrainingML
from __domainFinding import DomainFind
from __predictDomainMachineLearning import PredictDomain
from __getDomainOnEmailFake import GetDomainEmailFake
from __getDomainInfomation import GetDomainInfo


class TrainingAIScript(TrainingML):
    def __init__(self, path_train="./domainfu/domain_train.txt", tlds=["net", "com"]):

        super().__init__(self, path_train=path_train, tlds=tlds)


class FindingDomains(DomainFind):
    def __init__(self, path_log="./domainfu/log_domain.txt", path_save="./domainfu/domain_saved.txt",
            path_train="./domainfu/domain_train.txt", tdls = ["net", "com"], day_limit=7):
        
        super().__init__(path_log=path_log, path_save=path_save, path_train=path_train, tdls=tdls,
            day_limit=day_limit)


class DomainPrediction(PredictDomain):
    def __init__(self, path_train="train_v2.txt"):
        super().__init__(path_train=path_train)



class GetDomain(GetDomainEmailFake):
    def __init__(self, path_log="log_domain.txt", path_save="domain_saved.txt", path_train="domain_train.txt",
        tdls = ["net", "com"], day_limit=7):

        super().__init__(path_log=path_log, path_save=path_save, path_train=path_train, tdls=tdls,
            day_limit=day_limit)


class GetDomainInfomation(GetDomainInfo):
    def __init__(self, tlds=["net", "com"]):
        super().__init__(tlds=tlds)