import os

from dotenv import dotenv_values

environment = os.environ.get('FLASK_ENV', 'development')
print(environment)

params = []
if environment == 'test':
    params = dotenv_values(".test.env")
elif environment == 'prod':
    params = dotenv_values(".prod.env")
elif environment == 'dev':
    params = dotenv_values(".dev.env")
else:
    params = dotenv_values(".dev.env")

