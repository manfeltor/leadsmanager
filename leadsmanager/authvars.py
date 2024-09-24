from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
WPUSER = config('WPUSER')
WPPASS = config('WPPASS')
SRTOK = config('SRTOK')

usrnm = WPUSER
passw = WPPASS
frmids = [7, 3, 4, 5]

