#!/usr/bin/python3
# -*- encoding:utf-8 -*-
from tools.notifications import *
from tools.sql_tools import general_records
from datetime import datetime
import json



#For solve this problem i would use a AWS services, i will treat this as a ETL process assuming that we are
# in the part of Transform the data, so i will create an API for receive the data from the Extract process
# suppossing that we received the data after insert the data to the database we will process the data
# we will check if exist a similar record in the table, if the record don´t exist we will insert it, otherwhise
# we will don´t insert the record and we will create another table "logs_records"
# the database is hosted on AWS 
HOST   = "ltdata.cj7i5sksfdfm.us-east-2.rds.amazonaws.com"
USER   = "lt"
PASSWD = "poropo1994"

DATE = datetime.now()


def start(event):
    connection_sql =  general_records(HOST, USER, PASSWD)
    total_companies = list()
    for each_one in event:
        each_one.update({"last_date_time": DATE})
        company_name = each_one["company_name"]
        website_url = each_one["website_url"]
        linkedin_url = each_one["linkedin_url"]
        last_update_time = DATE

        query_info = """
        dbo.company_records_fra WHERE company_name LIKE '{}%' OR website_url LIKE '{}%' OR linkedin_url LIKE '{}%'
        """.format(company_name,website_url, linkedin_url )
        # print(query_info)

        result = connection_sql.general_query("id",query_info)

        #if there is a row, we insert the data in the log_table for save it and process the data and homologate it in a future 
        # in another process, for have sample data
        # assuming that the query returns a sample of the data, we can take the first id
        if len(result)> 0:
            print("THE RECORD EXIST ")
            id_data = result[0]["id"]
            
            print(id_data)
            columns = "Idrecords, Insert_date, Logs_record"
            logs = json.dumps(each_one, default=str)
            print("losgs")
            print(logs)
            values = "{},GETDATE(), '{}'".format(id_data, logs )


            connection_sql.insert_query("dbo.logs_records",columns,values )

        # otherwise if there is not any row, we insert a new one and send a notification to the user for corroborate that is not repetead
        elif len(result) == 0:
            print("THE RECORD DON´T EXIST ")
            columns = "company_name, website_url, linkedin_url, last_update_time"
            values = "'{}','{}','{}',GETDATE()".format(company_name,website_url,linkedin_url )
            connection_sql.insert_query("dbo.company_records_fra",columns,values )
            total_companies.append(company_name)

    if len(total_companies)> 0:
        print("Sending email....")
        send_email(total_companies)
        
        
   
        #print(result)
   


if __name__ == "__main__":
    try:
        event =[{
            "company_name": "Facebook",
            "website_url": "facebook.com",
            "linkedin_url": "https://www.linkedin.com/company/facebook/"
        },
        {
        "company_name": "SaleMove",
            "website_url": "salemove.com",
            "linkedin_url": "linkedin.com/company/salemove"
        },
        {
        "company_name": "Glia",
            "website_url": "glia.com",
            "linkedin_url": "linkedin.com/company/salemove"
        },
        {
        "company_name": "Snapchat",
            "website_url": "",
            "linkedin_url": ""
        },
        {
        "company_name": "Snapchat, LLC",
            "website_url": "",
            "linkedin_url": ""
        }
        ]

        start(event)

    except Exception as Error:
        print("Something wents wrong : {}".format(Error))
