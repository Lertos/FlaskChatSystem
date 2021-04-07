import requests
import db_manager

username = 'Lertos'
token = ''
domain_name = 'Lertos.pythonanywhere.com'

database = db_manager.mysql_pool
database.resetDailyStats()

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        username=username, domain_name=domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)