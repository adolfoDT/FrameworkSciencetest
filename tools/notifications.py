import boto3



def send_email(companies_names):
    print("enter")

    companies_names = " ,".join([company for company in companies_names])
    
    SENDER = "FrameworkScienceTest <diaz.taracenaAWS@gmail.com>"
    AWS_REGION = "us-east-2"
    SUBJECT = "WARNING!"
    CHARSET = "UTF-8"
    emails = ["diaz.taracenaAWS@gmail.com"]
    BODY_HTML = """<p>These companies: {companies_names} were inserted, to the Table company_records_fra, please check
    on the database is the record is not repeated
    </p>""".format(companies_names= companies_names )
    BODY_TEXT = """
    These company: {companies_names} were inserted, to the Table = company_records_fra, please check
    on the database is the record is not repeated
    """

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        for each_email in emails:
            response = client.send_email(
                                Destination={
                                    'ToAddresses': [
                                        each_email,
                                    ],
                                },
                                Message={
                                    'Body': {
                                        'Html': {
                                            'Charset': CHARSET,
                                            'Data': BODY_HTML,
                                        },
                                        'Text': {
                                            'Charset': CHARSET,
                                            'Data': BODY_TEXT,
                                        },
                                    },
                                    'Subject': {
                                        'Charset': CHARSET,
                                        'Data': SUBJECT,
                                    },
                                },
                                Source=SENDER,
                            )
    except Exception as error:
        print("Errors were found in sending the notification, the deails are: {}.".format(error) )
        return False
    else:
        print("The notifications were sent!")
        return True
            
