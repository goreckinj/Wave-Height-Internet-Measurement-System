import configparser

config = configparser.ConfigParser()
config['EDBSettings'] = {'edbHost': 'localhost',
                         'edbPort': '5432',
                         'edbName': 'whms',
                         'edbUser': 'postgres',
                         'edbPass': '2ztt'}

config['Email'] = {'email': 'goreckinj@msoe.edu'}

with open('whims.ini', 'w') as f:
    config.write(f)
