import sqlite3

conn = sqlite3.connect('wills.sqlite', timeout=1)

#final = [ {'Estate Number': '000000000001', 'Type': 'RE', 'Status': 'CLOSED', 'Date Opened': '05/02/2005', 'Date Closed': '05/02/2005', 'Reference': '', 'Decedent Name': 'HERVEY W. SHUCK', 'Date of Death': '1/1/1111', 'Date of Filing': '05/02/2005', 'Will': 'NO WILL', 'Date of Will': '', 'Date of Probate': '', 'Aliases': '', 'Personal Reps': '', 'Attorney': '', 'Last Docket Entry': '"05/02/2005 | 1 | 1244 | MISCELLANEOUS MATTERS (PERMANENT RETENTION ITEMS ONLY) | 1"'}, {'Estate Number': "0000000000069"}]

cur = conn.cursor()
#cur.execute('DELETE FROM records')
'''sql = ("""CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, " 
        death_date VARCHAR,
        ref_number VARCHAR,
        will_date VARCHAR,
        attorney VARCHAR,
        personal_reps VARCHAR,
        closed_date VARCHAR,
        will_status VARCHAR,
        type VARCHAR,
        opened_date VARCHAR,
        filing_date VARCHAR,
        probate_date VARCHAR,
        aliases VARCHAR,
        status VARCHAR,
        decedent VARCHAR,
        estate_num VARCHAR,
        last_docket_entry VARCHAR,
        county VARCHAR
        CONSTRAINT unq UNIQUE (estate_num, county); """)'''

cur.execute("""CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        death_date VARCHAR,
        ref_number VARCHAR,
        will_date VARCHAR,
        attorney VARCHAR,
        personal_reps VARCHAR,
        closed_date VARCHAR,
        will_status VARCHAR,
        type VARCHAR,
        opened_date VARCHAR,
        filing_date VARCHAR,
        probate_date VARCHAR,
        aliases VARCHAR,
        status VARCHAR,
        decedent VARCHAR,
        estate_num VARCHAR,
        last_docket_entry VARCHAR,
        county VARCHAR,
        UNIQUE(estate_num, county)); """)

#print(f"{row['Estate Number']}\"")
#headers = "death_date, " ref_number, will_date, attorney, personal_reps, closed_date, will_status, type, opened_date, filing_date, probate_date, aliases, status, decedent, estate_num, last_docket_entry"
#table = 'records'
#values = f"\"{row['Date of Death']}\", \"{row['Reference']}\", \"{row['Date of Will']}\", \"{row['Attorney']}\", \"{row['Personal Reps']}\", \"{row['Date Closed']}\", \"{row['Will']}\", \"{row['Type']}\", \"{row['Date Opened']}\", \"{row['Date of Filing']}\", \"{row['Date of Probate']}\", \"{row['Aliases']}\", \"{row['Status']}\", \"{row['Decedent Name']}\", \"{row['Estate Number']}\", {row['Last Docket Entry']}"

#sql = f"INSERT into {table} ({headers}) VALUES ({values})"
#sql = "INSERT INTO records (estate_num) VALUES (:'Estate Number')"

#cur.executemany(sql, final)
#cur.execute(f"INSERT INTO records (death_date,ref_number) VALUES ({row['Estate Number']},'1')", row)
#cur.execute(f"INSERT INTO records (ref_number,will_date,attorney,personal_reps,closed_date,will_status,type,opened_date,filing_date,probate_date,aliases,status,decedent,estate_num,last_docket_entry) VALUES ({row['Date of Death']},{row['Reference']},{row['Date of Will']},{row['Attorney']},{row['Personal Reps']},{row['Date Closed']},{row['Will']},{row['Type']},{row['Date Opened']},{row['Date of Filing']},{row['Date of Probate']},{row['Aliases']},{row['Status']},{row['Decedent Name']},{row['Estate Number']},{row['Last Docket Entry']})", row)

conn.commit()
conn.close()
