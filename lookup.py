import sys
import urllib
from datetime import datetime
from enum import Enum
from typing import Type

import time
import csv
import click
import requests
import urllib3
from bs4 import BeautifulSoup

SEARCH_URL = "https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx"

class EstateCounty(Enum):
    Unset = ""
    Allegany = '1'
    AL = '1'
    AnneArundel = '2'
    AA = '2'
    Baltimore = '3'
    BA = '3'
    Calvert = '4'
    CA = '4'
    Caroline = '5'
    CAL = '5'
    Carroll = '6'
    CAR = '6'
    Cecil = '7'
    CE = '7'
    Charles = '8'
    CH = '8'
    Dorchester = '9'
    DO = '9'
    Frederick = '10'
    FR = '10'
    Garrett = '11'
    GA = '11'
    Harford = '12'
    HA = '12'
    Howard = '13'
    HO = '13'
    Kent = '14'
    KE = '14'
    Montgomery = '15'
    MO = '15'
    PrinceGeorges = '16'
    PG = '16'
    QueenAnnes = '17'
    QA = '17'
    StMarys = '18'
    SM = '18'
    Somerset = '19'
    SO = '19'
    Talbot = '20'
    TA = '20'
    Washington = '21'
    WA = '21'
    Wicomico = '22'
    WI = '22'
    Worcester = '23'
    WO = '23'
    BaltimoreCity = '24'
    BC = '24'


class EstateStatus(Enum):
    Unset = ""
    Archived = "ARCHIV"
    Closed = "CLOSED"
    Open = "OPEN"
    Pending = "PENDIN"


class EstateType(Enum):
    Unset = ""
    ForeignProceeding = "FP"
    FP = "FP"
    LimitedOrder = "LO"
    LO = "LO"
    ModifiedAdministration = "MA"
    MA = "MA"
    MotorVehicle = "MV"
    MV = "MV"
    NonPropate = "NP"
    NP = "NP"
    RegularEstate = "RE"
    RE = "RE"
    RegularEstateJudicial = "RJ"
    RJ = "RJ"
    SmallEstate = "SE"
    SE = "SE"
    SmallEstateJudicial = "SJ"
    SJ = "SJ"
    UnprobatedWillOnly = "UN"
    UN = "UN"


class PartyType(Enum):
    Decedent = "Decedent"
    D = "Decedent"
    PersonalRepresentative = "Personal Representative"
    PR = "Personal Representative"


def get_enum_names(enum_type: Enum) -> list[str]:
    names = list(enum_type.__members__.keys())
    if "Unset" in names:
        names.remove("Unset")
        names.insert(0, "")
    return names


@click.command()
@click.option(
    "-e",
    "--estate-number",
    default="",
    help="Estate number",
)
@click.option(
    "-c",
    "--county",
    type=click.Choice(get_enum_names(EstateCounty)),
    default=EstateCounty.Unset.value,
    help="County",
)
@click.option(
    "-fn",
    "--first-name",
    default="",
    help="First name",
)
@click.option(
    "-mn",
    "--middle-name",
    default="",
    help="Middle name",
)
@click.option(
    "-ln",
    "--last-name",
    default="",
    help="Last name",
)
@click.option(
    "-eln",
    "--exact-last-name",
    is_flag=True,
    default=False,
    help="Exact last name match",
)
@click.option(
    "-es",
    "--estate-status",
    type=click.Choice(get_enum_names(EstateStatus)),
    default=EstateStatus.Unset.value,
    help="Estate Status",
)
@click.option(
    "-et",
    "--estate-type",
    type=click.Choice(get_enum_names(EstateType)),
    default=EstateType.Unset.value,
    help="Estate Type",
)
@click.option(
    "-pt",
    "--party-type",
    type=click.Choice(get_enum_names(PartyType)),
    default=PartyType.Decedent.value,
    help="Party Type",
)
@click.option(
    "-df",
    "--date-from",
    default="",
    help="Filing date from (MM/DD/YYYY)",
)
@click.option(
    "-dt",
    "--date-to",
    default="",
    help="Filing date to (MM/DD/YYYY)",
)
@click.option(
    "-de",
    "--date-exact",
    default="",
    help="Exact filing date (MM/DD/YYYY)",
)
def cli(
    estate_number: str,
    county: str | int,
    first_name: str,
    middle_name: str,
    last_name: str,
    exact_last_name: bool,
    estate_status: str,
    estate_type: str,
    party_type: str,
    date_from: str,
    date_to: str,
    date_exact: str,
) -> None:
    if (date_from or date_to) and date_exact:
        print("[!] date-from/date-to and date-exact are mutually exclusive")
        sys.exit()

    if date_from:
        #sys.exit()
        #date_from = datetime.strftime(date_from, "%m/%d/%Y")
        date_from = date_from

    if date_to:
        date_to
        #date_to = getattr(EstateStatus, es).value

    if date_exact:
        #date_exact = datetime.strftime(date_exact, "%m/%d/%Y")
        date_exact

    if county:
        county = getattr(EstateCounty, county).value

    if estate_status:
        estate_status = getattr(EstateStatus, estate_status).value

    if estate_type:
        estate_type = getattr(EstateType, estate_type).value

    if party_type:
        party_type = getattr(PartyType, party_type).value

    if exact_last_name:
        exact_last_name = "on"

    params = {
        "txtEstateNo": estate_number,
        "cboCountyId": county,
        "txtFN": first_name,
        "txtMN": middle_name,
        "txtLN": last_name,
        "chkExactMatchLastName": exact_last_name,
        "cboStatus": estate_status,
        "cboType": estate_type,
        "DateOfFilingFrom": date_from,
        "DateOfFilingTo": date_to,
        "txtDOF": date_exact,
        "cboPartyType": party_type,
    }

    run(params)

def run(params: dict) -> None:
    headers = {}

    url = 'https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx'
    resp = requests.get(url)
    session = requests.Session()

    soup = BeautifulSoup(resp.content, "html.parser")

    crumbs = {}

    for tag in soup.find_all("input", type="hidden"):
        crumbs[tag["name"]] = tag["value"]

    cookies = session.cookies.get_dict()

    session = requests.Session()
  
    counties = []

    data = {
        '__VIEWSTATE': crumbs["__VIEWSTATE"],
        '__VIEWSTATEGENERATOR': crumbs["__VIEWSTATEGENERATOR"],
        '__EVENTVALIDATION': crumbs["__EVENTVALIDATION"],
        'txtEstateNo': '',
        'txtLN': '',
        'cboCountyId': params["cboCountyId"],
        'txtFN': '',
        'txtMN': '',
        'cboStatus': '',
        'cboType': '',
        'DateOfFilingFrom': params["DateOfFilingFrom"],
        'DateOfFilingTo': params["DateOfFilingTo"],
        'txtDOF': params["txtDOF"],
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

    with open(filename, 'w', newline = '\r\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(final)

    """else:
        with open(filename, 'a', newline = '\r\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            #writer.writeheader()
            writer.writerows(final)"""

##########################

    print("[*] Viewing search page")
    resp = requests.get(SEARCH_URL)
    resp.raise_for_status()
    bs = BeautifulSoup(resp.content, "html.parser")

    # add ASP.NET hidden params
    for tag in bs.find_all("input", type="hidden"):
        params[tag["name"]] = tag["value"]

    # get values in the Set-Cookie response header
    cookies = get_set_cookies(resp.headers)

    # print("[*] Running search")
    # resp = requests.post(
    #    SEARCH_URL,
    #    # cookies=cookies,
    #    # headers=headers,
    #    data=params,
    # )
    # resp.raise_for_status()
    # print(resp.text)


def get_set_cookies(headers: dict) -> dict:
    cookies = {}
    values = headers["Set-Cookie"]
    values = values.split("; ")
    for cookie in values:
        if "=" in cookie:
            key, val = cookie.split("=", maxsplit=1)
        else:
            key, val = cookie, None
        cookies[key] = val

    return cookies


if __name__ == "__main__":
    cli()
