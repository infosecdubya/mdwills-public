import certifi
import urllib
import urllib3
import requests
import csv

from bs4 import BeautifulSoup
from csv import DictReader, DictWriter

'''http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)'''

headers = {
    'authority': 'registers.maryland.gov',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ga_20SW2ZJYGC=GS1.1.1695135165.2.0.1695135165.0.0.0; _ga_R1LE8KQW1T=GS1.2.1695397839.1.0.1695397839.0.0.0; _ga_KD4VER2PRG=GS1.1.1699378769.2.0.1699378769.60.0.0; _ga_LJCC9XG5J9=GS1.1.1699888973.8.0.1699888973.0.0.0; _ga_GFHX73E8E3=GS1.1.1699888974.3.0.1699888974.0.0.0; _ga=GA1.1.423128016.1694884462; _ga_29XSCDN3RL=GS1.1.1701711516.4.0.1701711516.0.0.0; ASP.NET_SessionId=jswpljbyey1bcg4eeitfndjq',
    'origin': 'https://registers.maryland.gov',
    'referer': 'https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

url = 'https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx'
resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
session = requests.Session()
#print(session.headers)
#print(session.cookies.get_dict())

soup = BeautifulSoup(resp.content, "html.parser")

crumbs = {}

for tag in soup.find_all("input", type="hidden"):
    crumbs[tag["name"]] = tag["value"]

cookies = session.cookies.get_dict()
#print(cookies)
# TODO get GA cookies from header or maybe don't need them?
"""'_ga_20SW2ZJYGC': 'GS1.1.1695135165.2.0.1695135165.0.0.0',
'_ga_R1LE8KQW1T': 'GS1.2.1695397839.1.0.1695397839.0.0.0',
'_ga_KD4VER2PRG': 'GS1.1.1699378769.2.0.1699378769.60.0.0',
'_ga_LJCC9XG5J9': 'GS1.1.1699888973.8.0.1699888973.0.0.0',
'_ga_GFHX73E8E3': 'GS1.1.1699888974.3.0.1699888974.0.0.0',
'_ga': 'GA1.1.423128016.1694884462',
'_ga_29XSCDN3RL': 'GS1.1.1701711516.4.0.1701711516.0.0.0',"""

headers = {}
"""    'authority': 'registers.maryland.gov',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ga_20SW2ZJYGC=GS1.1.1695135165.2.0.1695135165.0.0.0; _ga_R1LE8KQW1T=GS1.2.1695397839.1.0.1695397839.0.0.0; _ga_KD4VER2PRG=GS1.1.1699378769.2.0.1699378769.60.0.0; _ga_LJCC9XG5J9=GS1.1.1699888973.8.0.1699888973.0.0.0; _ga_GFHX73E8E3=GS1.1.1699888974.3.0.1699888974.0.0.0; _ga=GA1.1.423128016.1694884462; _ga_29XSCDN3RL=GS1.1.1701711516.4.0.1701711516.0.0.0; ASP.NET_SessionId=jswpljbyey1bcg4eeitfndjq',
    'origin': 'https://registers.maryland.gov',
    'referer': 'https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}"""

data = {
    '__VIEWSTATE': crumbs["__VIEWSTATE"],
    '__VIEWSTATEGENERATOR': crumbs["__VIEWSTATEGENERATOR"],
    '__EVENTVALIDATION': crumbs["__EVENTVALIDATION"],
    'txtEstateNo': '',
    'txtLN': '',
    'cboCountyId': '13',
    'txtFN': '',
    'txtMN': '',
    'cboStatus': '',
    'cboType': '',
    'DateOfFilingFrom': '12/22/2023',
    'DateOfFilingTo': '01/22/2024',
    'txtDOF': '',
    'cboPartyType': 'Decedent',
    'cmdSearch': 'Search',
}

response = requests.post(
    'https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx',
    cookies=cookies,
    headers=headers,
    data=data,
)

soup2 = BeautifulSoup(response.content, "html.parser")

#print(session.cookies.get_dict())
#print(session.headers)

'''Build'''
estates = {}

for a in soup2.find_all('a', href=True, target="_self"):
        if 'Docket' in a["href"]:
            estates[a.text] = a["href"]
            #print(a["href"])

#print(estates)

''' for estate in estates:
    print(estates[estate]) '''

'''for tag in soup.find_all("input", type="hidden"):
    print((tag["name"] + "=" + tag["value"][0:15] ))

#print(soup.prettify()) '''

final = []

for estate in estates:
    estateRecord = requests.post(
        f'https://registers.maryland.gov/RowNetWeb/Estates/{estates[estate]}',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    soup3 = BeautifulSoup(estateRecord.content, "html.parser")
    #print(soup3)

# print(soup3.prettify)

    records = []
    rows = []

    for span in soup3.find_all('span', class_=["RowLabel"]):
        # print(span.text)
        records.append(span.text.strip(":"))

    # [print(x) for x in records]

    #for record in records
    for span in soup3.find_all('span', class_=["RowData"]):
        #rows[span["RowLabel"].text] = span["RowData"]
        #rows[record] = span.text
        rows.append(span.text.strip())

    print(rows)

    table = soup3.find('table', class_="docket-history-data")

    tr = table.find_all("tr")[-1]
    docket = [i.text.strip() for i in tr.find_all("td", valign="top")]
    
    #print(rows)
    #print(records)

    zipped = dict(zip(records, rows))
    zipped["Last Docket Entry"] = " | ".join(docket)

    final.append(zipped)
    #final.append({"Last Docket Entry": " | ".join(docket)})



fields = ['Date of Death', 'Reference', 'Date of Will', 'Attorney', 'Personal Reps', 'Date Closed', 'Will', 'Type', 'Date Opened', 'Date of Filing', 'Date of Probate', 'Aliases', 'Status', 'Decedent Name', 'Estate Number', 'Last Docket Entry']

#print(fields)

#print(final)

with open('estates.csv', 'w', newline = '\n') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(final)

    #[print(x + ": " + final[x]) for x in final]

#print(soup3.prettify)