import sys, os
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)


def install_need_package():
    print()
    print("[*] gợi ý thiết bị cần nhập -> [mobile windows linux]")
    device_input = input("[!] chúng tôi cần biết loại thiết bị bạn đang dùng để tải các gói phù hợp\n-> ")
    
    if device_input.lower().strip().startswith("mobile"):
        os.system("pip install requests colorama python-whois bs4")
    else:
        os.system("pip install requests colorama python-whois bs4 scikit-learn")
    
    print()
    input("[*] đã xong! nhấn enter để quay lại\n-> ")


while True:
    print("[1] -> tải các gói cần thiết")
    print("[2] - vào tool domainfu pc")
    
    print()
    choose_input = input("[!] nhập lựa chọn của bạn\n-> ")

    if choose_input.strip().lower() == "1":
        install_need_package()
    if choose_input.strip().lower() == "2":
        from domainfu_new_ui.domainfu import UI
        UI()
    os.system("cls") if sys.platform.startswith("win") else os.system("clear")