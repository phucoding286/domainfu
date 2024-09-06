from __trainingMLPredictDomain import TrainingML
from __domainFinding import DomainFind

print("scripts created by Phu Tech")
print("facebook: https://www.facebook.com/profile.php?id=61562099241369")
print("youtube: https://www.youtube.com/@phucoding286")
print("github: https://github.com/phucoding286")
print()

def chat_ui_clsf_choose():
    print("1. đào tạo AI dự đoán trong script")
    print("2. tìm và dự đoán tên miền tự động")

    d = None
    while True:
        try:
            d = int(input("nhập tùy chọn của bạn: "))
            print()
            break
        except:
            print("vui lòng nhập số tương ứng với các tùy chọn trên")
    
    return d

if __name__ == "__main__":

    d = chat_ui_clsf_choose()
    path_log="./domainfu/log_domain.txt"
    path_save="./domainfu/domain_saved.txt"
    path_train="./domainfu/domain_train.txt"
    tlds = ["net", "com"]
    day_limit = 7

    trainml_instance = TrainingML(path_train, tlds)
    df_instance = DomainFind(path_log, path_save, path_train, tlds, day_limit)

    if d == 1: trainml_instance.clasify_via_chatui()
    elif d == 2: df_instance.run_all_script()