from requests import get
from bs4 import BeautifulSoup
import re

def process_soup_content(soup_content):
    first_segment = soup_content[0].text
    second_segment = soup_content[3].text
    
    tax_id = clean_string(re.search(r'統一編號 (.*)', first_segment)[0])
    company_name = clean_string(re.search(r'公司名稱\n\n(.*)', first_segment)[0])
    address = clean_string(re.search(r'公司所在地\n\n(.*)', first_segment)[0])
    industry = clean_string(re.search(r'行業\n\n(.*)', second_segment)[0])
    
    return f"{tax_id}\t{company_name}\t{address}\t{industry}"
    
def clean_string(string):
    symbols = ["\n", "\t", "\xa0"]
    labels = ["統一編號", "公司名稱", "公司所在地", "行業"]
    to_remove = symbols + labels
    
    for item in to_remove:
        string = string.replace(item, "")
    
    return string.strip()

def download(url):
    response = get(url)
    soup = BeautifulSoup(content)
    soup_content = soup.find_all("div", {"class": "table-responsive"})
    
    with open("output.txt", "a") as f:
        f.write(process_soup_content(soup_content))
