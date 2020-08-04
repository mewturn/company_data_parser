from requests import get
from bs4 import BeautifulSoup
import re

def process_soup_content(soup_content):
    text = " ".join([i.text for i in soup_content])
    try:
        tax_id = re.search(r'統一編號 (.*)', text)
        company_name = re.search(r'公司名稱\n\n(.*)', text) or re.search(r'營業人名稱\n\n(.*)', text)
        address = re.search(r'公司所在地\n\n(.*)', text) or re.search(r'營業地址\n\n(.*)', text)
        industry = re.search(r'行業\n\n(.*)', text)
        
        if tax_id and company_name and address and industry:
            tax_id = clean_string(tax_id[0])
            company_name = clean_string(company_name[0])
            address = clean_string(address[0])
            industry = clean_string(re.sub(r'[0-9]', '', industry[0]))

            return f"{tax_id}\t{company_name}\t{address}\t{industry}"
        return

    except Exception as e:
        print(e)
    
def clean_string(string):
    symbols = ["\n", "\t", "\xa0"]
    labels = ["統一編號", "公司名稱", "公司所在地", "行業", "營業人名稱", "營業地址"]
    to_remove = symbols + labels
    
    for item in to_remove:
        string = string.replace(item, "")
    
    return string.strip()

def download(client_id, tax_id):
    print(f"Processing {client_id} ({tax_id})")
    try:
        url = f"http://datagovtw.com/company.php?id={tax_id}"
        response = get(url)
        soup = BeautifulSoup(response.content)
        soup_content = soup.find_all("div", {"class": "table-responsive"})

        with open("output.txt", "a") as f:
            text = f"{client_id}\t{process_soup_content(soup_content)}\n"
            f.write(text)

    except Exception as e:
        print(repr(e))
