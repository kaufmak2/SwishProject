import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {}
config['DEFAULT']['api_key'] = '800c934905374c26ccf15885be69965e'
config['DEFAULT']['sql_user'] = 'root'
config['DEFAULT']['sql_key'] = 'celtics'
with open('config.ini', 'w') as configfile:
	config.write(configfile)
