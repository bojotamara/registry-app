#!/bin/bash

set -e
set -u

CS_HOST=haiyang3@ui04.cs.ualberta.ca

bash ./scripts/rebuild-db.sh
bash ./scripts/compress.sh

scp ./prjcode.tgz $CS_HOST:~/registry-app/prjcode.tgz
scp ./registry.db $CS_HOST:~/registry-app/registry.db

ssh $CS_HOST
