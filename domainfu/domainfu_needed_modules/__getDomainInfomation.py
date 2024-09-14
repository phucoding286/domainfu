from whois import whois


class GetDomainInfo:
    def __init__(self, tlds=["net", "com"]):
        self.tlds = tlds


    def domain_information(self, domain):
        try:
            domain_infomations = whois(domain)
        except:
            return "error"
        
        # các key truy vấn thông tin
        keys = ["domain_name", "registrar", "whois_server", "referral_url", "updated_date", "creation_date",
                "expiration_date", "name_servers", "status", "emails", "dnssec", "name", "org", "address",
                "city", "state", "registrant_postal_code", "country"]
        
        # chuyển thông tin tên miền dạng json thành chuổi thông tin
        update_domain_infomation = ""
        for key in keys:
            try:
                update_domain_infomation += str(f"{domain_infomations[key]}, ")
            except:
                continue
        
        # cộng thêm tlds
        for tld in self.tlds:
            if domain.split(".")[1] in tld:
                update_domain_infomation = update_domain_infomation+tld
                break

        return update_domain_infomation