import requests
from bs4 import BeautifulSoup
import pandas as pd


# ----------------------------------- RESPONSE ----------------------------------- #
def func(page):
    URL = "https://www.hklawsoc.org.hk/en/Serve-the-Public/The-Law-List/Hong-Kong-Law-Firms"
    parameters = {
        "location": "Hong%20kong,Hong%20Kong%20Island",
        "sort": "NameAsc",
        "pageIndex": page
    }

    response = requests.get(url=URL, params=parameters).text
    soup = BeautifulSoup(response, features="html.parser")

    tags = soup.select(selector="td a")
    names = []
    links = []
    n = 2

    for tag in tags:
        if n % 2 == 0:
            name = tag.getText("a")
            link = tag.get("href")
            special_resp = requests.get(url=link).text
            special_soup = BeautifulSoup(special_resp, features="html.parser")
            mail = special_soup.select_one(selector="table tr a")
            mail = mail.getText()
            if '@' not in mail:
                mail = "Email is missing"

            names.append(name)
            links.append(mail)
        n += 1
    return names, links


# ----------------------------------- TABLE ----------------------------------- #
name_s = []
link_s = []
for p in list(range(1, 28)):
    print(p)
    na, li = func(p)
    for i in na:
        name_s.append(i)
    for j in li:
        link_s.append(j)

dictionary = {'Firm Name': name_s, 'Mail': link_s}
table = pd.DataFrame(dictionary, index=pd.RangeIndex(start=1, stop=len(name_s)+1, name='Index'))
table.to_csv("new_data.csv")
