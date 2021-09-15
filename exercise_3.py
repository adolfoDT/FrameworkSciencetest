from tools.sql_tools import general_records


#For solve this problem i would use a AWS services, i will treat this as a ETL process assuming that we are
# in the part of Transform the data, so i will create an API for receive the data from the Extract process
# suppossing that we received the data after insert the data to the database we will process the data
# we will check if exist a similar record in the table, if the record don´t exist we will insert it, otherwhise
# we will don´t insert the record and we will create another table 
# the database is hosted on AWS 
HOST   = "ltdata.cj7i5sksfdfm.us-east-2.rds.amazonaws.com"
USER   = "lt"
PASSWD = "poropo1994"

connection_sql =  general_records(HOST, USER, PASSWD)

connection_sql.general_query("*", "dbo.TB_archivosInstancias")


