from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)

groupId = 123
print(config['APIs']['get_reports_by_group_id'])
