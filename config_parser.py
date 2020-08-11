from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)

print(config['APIs']['get_groups_api'] + '/123/reports')
