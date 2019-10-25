#!/bin/bash

set -e
set -u

DATABASE_FILE=registry.db

if [ -f $DATABASE_FILE ]; then
    rm $DATABASE_FILE
fi

sqlite3 $DATABASE_FILE < prj-tables.sql
sqlite3 $DATABASE_FILE < prj-testdata.sql
