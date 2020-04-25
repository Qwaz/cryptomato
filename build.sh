#!/bin/sh

python3 -c "
import binascii
import os

if not os.path.exists('secrets'):
    os.mkdir('secrets')

for f in (
    'database_password.txt',
    'secret_cookie_password.txt',
):
    if not os.path.exists('secrets/' + f):
        open('secrets/' + f, 'w').write(binascii.hexlify(os.urandom(16)).decode() + '\n')
"

docker-compose build
