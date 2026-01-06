#!/bin/bash

set -euo pipefail

SERVER=thinkstation-home
DIR=/var/www/html/blog/

rsync -avz --delete public/ ${SERVER}:${DIR}

exit 0