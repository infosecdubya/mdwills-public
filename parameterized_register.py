import certifi
import urllib
import urllib3
import requests
import csv
import time
import click

from bs4 import BeautifulSoup
from csv import DictReader, DictWriter

def create_estate_file(): 

    headers = {}

    url = 'https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx'
    resp = requests.get(url)
    session = requests.Session()

    soup = BeautifulSoup(resp.content, "html.parser")

    crumbs = {}

    for tag in soup.find_all("input", type="hidden"):
        crumbs[tag["name"]] = tag["value"]

    cookies = session.cookies.get_dict()

    for i in range(1, 3):
        county = str(i)

        data = {
            '__VIEWSTATE': crumbs["__VIEWSTATE"],
            '__VIEWSTATEGENERATOR': crumbs["__VIEWSTATEGENERATOR"],
            '__EVENTVALIDATION': crumbs["__EVENTVALIDATION"],
            'txtEstateNo': '',
            'txtLN': '',
            'cboCountyId': county,
            'txtFN': '',
            'txtMN': '',
            'cboStatus': '',
            'cboType': '',
            'DateOfFilingFrom': '02/02/2024',
            'DateOfFilingTo': '02/09/2024',
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

        estates = {}

        for a in soup2.find_all('a', href=True, target="_self"):
                if 'Docket' in a["href"]:
                    estates[a.text] = a["href"]

        final = []

        for estate in estates:
            estateRecord = requests.post(
                f'https://registers.maryland.gov/RowNetWeb/Estates/{estates[estate]}',
                cookies=cookies,
                headers=headers,
                data=data,
            )

            soup3 = BeautifulSoup(estateRecord.content, "html.parser")

            records = []
            rows = []

            for span in soup3.find_all('span', class_=["RowLabel"]):
                # print(span.text)
                records.append(span.text.strip(":"))

            for span in soup3.find_all('span', class_=["RowData"]):
                #rows[span["RowLabel"].text] = span["RowData"]
                #rows[record] = span.text
                rows.append(span.text.strip())

            table = soup3.find('table', class_="docket-history-data")

            try:
                tr = table.find_all("tr")[-1]
            except AttributeError:
                pass

            docket = [i.text.strip() for i in tr.find_all("td", valign="top")]
            
            zipped = dict(zip(records, rows))
            zipped["Last Docket Entry"] = " | ".join(docket)

            final.append(zipped)

        fields = ['Date of Death', 'Reference', 'Date of Will', 'Attorney', 'Personal Reps', 'Date Closed', 'Will', 'Type', 'Date Opened', 'Date of Filing', 'Date of Probate', 'Aliases', 'Status', 'Decedent Name', 'Estate Number', 'Last Docket Entry']

        date = time.strftime("%Y%m%d")

        filename = f'estates{date}.csv'

        if i == 1: 
            with open(filename, 'w', newline = '\r\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                writer.writerows(final)

        else:
            with open(filename, 'a', newline = '\r\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                #writer.writeheader()
                writer.writerows(final)
    
    #return filename
    
# Using the special variable 
# __name__ 
if __name__ == "__main__": 
	create_estate_file()