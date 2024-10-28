import sys, os
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from domainfu.domainfu_needed_modules.__getDomainOnEmailFake import GetDomainEmailFake
from domainfu.domainfu_needed_modules.__getDomainInfomation import GetDomainInfo
from domainfu.domainfu_predict_modules_ml.__predictDomainMachineLearning import PredictDomain

import threading
import time
import colorama
colorama.init()


# theme for wating
def waiting_theme(timeout, content=""):
    for i in range(timeout):
        i += 1
        print(colorama.Fore.YELLOW + f"\r{i}s" + colorama.Style.RESET_ALL, end=" -> ")
        print(colorama.Fore.BLUE + content + colorama.Style.RESET_ALL, end="")
        time.sleep(1)
    print()


# domain object for check and filter domains
domain_object = GetDomainEmailFake(
    path_log="./domainfu/needed_data/log_domain.txt",
    path_save="./domainfu/needed_data/domain_saved.txt",
    path_train="./domainfu/needed_data/domain_train.txt",
    verbose=False
)
# predict domains can using for cloudsigma via ML and datatrain of domains used for cloudsigma beforce
predict_object = PredictDomain(
    path_train="./domainfu/needed_data/domain_train.txt"
)
# domain info object for get info of domain input via whois
domain_info_object = GetDomainInfo(
    tlds=['net', 'com']
)



# get and filter domain then return boolen json for classify domains
def get_and_filter_domain():
    domain = domain_object.get_domain()
    domain_check_log = domain_object.check_log(domain)
    tld_check = domain_object.check_tlds(domain)
    uptime_check = domain_object.check_up_time(domain)
    return {
        "domain": domain,
        "log": not bool(domain_check_log),
        "tld_check": bool(tld_check),
        "uptime": bool(uptime_check)
    }


# get domain infomation for classify via ML later
def get_domain_infomation(domain):
    domain_infomation = domain_info_object.domain_information(domain)
    return {"domain_info": domain_infomation}


# predict domain and return result with language
def predict_domain(domain_info):
    try:
        predict_result = int(predict_object.predict(domain_info))
    except Exception as e:
        return {"error": 'đã có lỗi khi dự đoán tên miền'}
    if bool(predict_result):
        return {"predict_result": "domain có thể dùng được", "status_clsf": bool(predict_result)}
    else:
        return {"predict_result": "domain có thể không dùng được", "status_clsf": bool(predict_result)}


# run needed script
def domainfu_run(save_path=domain_object.path_save, log_path=domain_object.path_log):

    def domain_writer(status: str, domain: str, save_path):
        try:
            # lưu vào file lưu trữ
            with open(save_path, "a") as file:
                file.write(f"{domain_result['domain']} -> {status}\n")
                print(colorama.Fore.GREEN + f"\nđã lưu tên miền -> {domain} thành công" + colorama.Style.RESET_ALL)
            # lưu vào log
            with open(log_path, "a") as file:
                file.write(f"{domain_result['domain']}\n")
                print(colorama.Fore.GREEN + f"đã lưu tên miền -> {domain} vào log thành công" + colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.RED + f"\nđã có lỗi khi lưu tên miền -> {domain}, mã lỗi: {e}" + colorama.Style.RESET_ALL)

    domain_result = get_and_filter_domain()

    if domain_result['log']:
        return {'status': "bad", 'message': f"{domain_result['domain']} -> đã tồn tại trong log!"}
    elif not domain_result['tld_check']:
        return {'status': 'bad', 'message': f"{domain_result['domain']} -> không tồn tại trong tlds đã quy định"}
    elif not domain_result['uptime']:
        return {'status': 'bad', 'message': f"{domain_result['domain']} -> số ngày hoạt động nhỏ hơn mức quy định"}
    else:
        domain_info = get_domain_infomation(domain_result['domain'])
        predict_domain_result = predict_domain(domain_info['domain_info'])
        
        if "error" in predict_domain_result:
            return {'status': 'bad', 'message': predict_domain_result['error']}
        elif predict_domain_result['status_clsf']:
            domain_writer(status="good", domain=domain_result['domain'], save_path=save_path)
            return {'status': 'good', 'message': f"công cụ tin rằng domain -> {domain_result['domain']} phù hợp tiêu chuẩn"}
        else:
            domain_writer(status="bad", domain=domain_result['domain'], save_path=save_path)
            return {'status': 'bad', 'message': f"công cụ tin rằng domain -> {domain_result['domain']} không dùng được"}



# run domainfu tool with multi process
def domainfu_thread(thread_num=20):

    def __dmfu_run():
        r = domainfu_run()
        if r['status'] == 'bad':
            print("\r " + 75 * " ", end="")
            print(colorama.Fore.RED + f"\r[!] {r['message']}" + colorama.Style.RESET_ALL, end="")
        else:
            print("\r " + 75 * " ", end="")
            print(colorama.Fore.GREEN + f"\r[!] {r['message']}" + colorama.Style.RESET_ALL, end="")

    threads = []
    for _ in range(thread_num):
        thread = threading.Thread(target=__dmfu_run)
        threads.append(thread)
        thread.start()
        time.sleep(0.2)
    for thread in threads:
        thread.join()



# main program for domainfu script and domainfu multiprocess script
def domainfu_run_main():
    while True:
        try:
            thread_num = int(input(colorama.Fore.YELLOW + "[*] nhập vào số luồng\n-> " + colorama.Style.RESET_ALL))
            break
        except:
            print(colorama.Fore.RED + "[!] vui lòng nhập 'số' luồng!" + colorama.Style.RESET_ALL)

    print(colorama.Fore.YELLOW + "[!] bạn có thể dùng tổ hợp CTRL+C để thoát khỏi chương trình" + colorama.Style.RESET_ALL)
    waiting_theme(timeout=5, content="vui lòng đợi 5s để chạy tool")

    print()
    while True:
        try:
            domainfu_thread(thread_num)
        except KeyboardInterrupt:
            print(colorama.Fore.YELLOW + "đã nhận CTRL+C, bạn đang thoát trình tìm domain..." + colorama.Style.RESET_ALL)
            return 0


def read_domain(path_save=domain_object.path_save):
    with open(path_save, "r") as file:
        ds_domain_saved = file.read().splitlines()

    contour_len = len(" -------------------------------")
    for i in range(len(ds_domain_saved)):
        ds_domain_saved[i] = f"| {ds_domain_saved[i]}"
        for _ in range(len(ds_domain_saved[i]), contour_len-1):
            ds_domain_saved[i] += " "
        ds_domain_saved[i] += "|"

    print(colorama.Fore.YELLOW + "[*] domains đã thu thập bên dưới ↓" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + " -------------------------------" + colorama.Style.RESET_ALL)
    for dv in ds_domain_saved:
        print(colorama.Fore.GREEN + f"{dv}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + " -------------------------------" + colorama.Style.RESET_ALL)

    input(colorama.Fore.YELLOW + "[*] nhấn enter để thoát\n-> " + colorama.Style.RESET_ALL)
    return 0


def clear_domains(path_save=domain_object.path_save):
    with open(path_save, "w") as file:
        file.write("")
        input(colorama.Fore.GREEN + "[*] đã làm sạch file lưu trữ tên miền, enter để quay lại\n-> " + colorama.Style.RESET_ALL)


def UI():
    while True:
        print(colorama.Fore.YELLOW + " -----------------------------------------" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| facebook -> Programing Sama             |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| youtube -> Phu Tech                     |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| github -> @phucoding286                 |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| version -> PC                           |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + " -----------------------------------------" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| [1] -> tìm kiếm tên miền với công cụ AI |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| [2] -> kiểm tra các tên miền đã lưu     |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + "| [3] -> clear sạch tất cả tên miền       |" + colorama.Style.RESET_ALL)
        print(colorama.Fore.YELLOW + " -----------------------------------------" + colorama.Style.RESET_ALL)
        
        choose_input = input(colorama.Fore.YELLOW + "\n[i] nhập vào số thứ tự tương ứng tool bạn muốn chạy\n-> " + colorama.Style.RESET_ALL)

        print()
        if choose_input.strip().lower() == "1":
            domainfu_run_main()
        elif choose_input.strip().lower() == "2":
            read_domain()
        elif choose_input.strip().lower() == "3":
            clear_domains()