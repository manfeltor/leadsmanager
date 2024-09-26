from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
WPUSER = config('WPUSER')
WPPASS = config('WPPASS')
SRTOK = config('SRTOK')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')

usrnm = WPUSER
passw = WPPASS
frmids = [7, 3, 4, 5]

