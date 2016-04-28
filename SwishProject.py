import requests #for HTTP Get
import json  #parsing the JSON
import pymysql  #to connect to MYSQL
import pandas as pd  #to get a date range
import datetime
import configparser

###Get Today's Date and converts to string
def get_today():
	date=str(datetime.date.today())
	return date

# ###Create Date Range in order to get past data
def get_date_range(start_date, end_date):
	date_range=pd.date_range(start_date,end_date).tolist()
	date_list = []
	for item in date_range:
		date_str = str(item.year)
		date_month = convert_date(item.month)
		date_day = convert_date(item.day)
		date_str += "-" + date_month + "-" + date_day
		date_list.append(date_str)
	return date_list

##Convert date to YYYY-MM-DD format
def convert_date(date):
	if (date < 10):
		date = "0" + str(date)
	else:
		date = str(date)
	return date


##Connect to API given date and api_key
def get_json(date, api_key):
	url = 'https://api.swishanalytics.com/nba/players/fantasy?&date=' + date + '&apikey=' + api_key
	r=requests.get(url, verify=False)
	request_json = r.json()
	return request_json


##Add data to SQL database
def add_today(results):
	for item in results:
		cur.execute("INSERT INTO PlayerProjections (date,season,teamAbbr,oppAbbr,positionAbbr,name,starter,minutes,points,rebounds,assists,steals,turnovers,blocks,threesMade, \
		doubleDoublePct,tripleDoublePct,draftkingsFpts,yahooFpts,fanduelFpts,draftkingsFptsActual,yahooFptsActual,fanduelFptsActual) VALUES \
	 (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s, %s, %s)" \
		, (item["date"], item['season'], item['teamAbbr'], item["oppAbbr"], item["positionAbbr"], item["name"], item["starter"], item["minutes"] \
		, item["points"], item["rebounds"], item["assists"], item["steals"], item["turnovers"], item["blocks"], item["threesMade"], item["doubleDoublePct"], \
		item["tripleDoublePct"], item["draftkingsFpts"], item["yahooFpts"], item["fanduelFpts"],item["draftkingsFptsActual"], item["yahooFptsActual"], item["fanduelFptsActual"]))

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['api_key']

conn=pymysql.connect(host="localhost",port=3306,user=config['DEFAULT']['sql_user'],password=config['DEFAULT']['sql_key'],db="Swish") ##connects to SQL database
cur=conn.cursor() 



today_json = get_json(get_today(), api_key)['data']['results']

add_today(today_json)


conn.commit()
cur.close()
conn.close()