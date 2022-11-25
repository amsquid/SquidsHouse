def get_config():
	config = {}

	with open('./config.dat', 'r') as configFile:
		data = configFile.read()

		data.strip()
		lines = data.split('\n')

		for line in lines:
			config_item = line.split('=')

			key = str(config_item[0])
			value = str(config_item[1].replace('\n', ''))
			
			config[key] = value

	return config

def get_info():
	info = {}

	with open('./info.dat', 'r') as infoFile:
		data = infoFile.read()

		lines = data.split('\n')

		for line in lines:
			info_item = line.split('=')

			key = str(info_item[0])
			value = str(info_item[1].replace('\n', ''))
			
			info[key] = value
	
	return info