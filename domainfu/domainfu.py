from domainfu_find_modules.domainfu_train import TrainingML
from domainfu_find_modules.domainfu_find import DomainFind
from domainfu_find_modules.pred_again import PredAgain

print("scripts created by Phu Tech")
print("facebook: https://www.facebook.com/profile.php?id=61562099241369")
print("youtube: https://www.youtube.com/@phucoding286")
print("github: https://github.com/phucoding286")
print()


def chat_ui_clsf_algorithm():
    print("chọn các thuật toán tìm kiếm tên miền sau")
    print("1. tổng hợp nhiều thuật toán machine learning (có thể thiếu chính xác) (ml)")
    print("2. thuật toán random forest (ml)")
    print("3. thuật toán Logistic Regression (được viết để chạy trên termux, không nên dùng trên máy tính) (ml)")

    inp = None
    while True:
        try:
            inp = int(input("nhập lựa chọn của bạn: "))
            print()
            break
        except:
            print("vui lòng nhập tùy chọn hợp lệ")

    if inp == 1: d = "ml"
    elif inp == 2: d = "rdfr"
    elif inp == 3: d = "logi"
    else: d = "rdfr"
    
    return d


def chat_ui_clsf_choose():
    print("1. đào tạo AI dự đoán trong script")
    print("2. tìm và dự đoán tên miền tự động")
    print("3. dự đoán lại từ tệp tin tên miền đã lưu")

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
    d1 = chat_ui_clsf_algorithm()
    d2 = chat_ui_clsf_choose()
    path_log="./needed_data/log_domain.txt"
    path_save="./needed_data/domain_saved.txt"
    path_train="./needed_data/domain_train.txt"
    tlds = ["net", "com"]
    day_limit = 7

    trainml_instance = TrainingML(path_train, tlds)
    df_instance = DomainFind(path_log, path_save, path_train, tlds, day_limit, d1)

    if d2 == 1: trainml_instance.clasify_via_chatui()
    elif d2 == 2: df_instance.run_all_script()
    elif d2 == 3: PredAgain(path_train, path_save, d1)
