#!/bin/sh

python -c "
import os

if not os.path.exists('secrets'):
    os.mkdir('secrets')

for f in (
    'database_password.txt',
    'secret_cookie_password.txt',
):
    if not os.path.exists('secrets/' + f):
        file('secrets/' + f, 'w').write(os.urandom(16).encode('hex') + '\n')
"

docker-compose build
