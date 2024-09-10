from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
WPUSER = config('ftorres')
WPPASS = config('WPPASS')

usrnm = WPUSER
passw = WPPASS
frmids = [7, 3, 4, 5]