import os
from decouple import config

x = config('MAIL_ADDRESS')
y = config('MAIL_PASSWORD')

print(x)
print(y)