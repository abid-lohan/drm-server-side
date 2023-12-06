#!/bin/sh
touch development.db
sqlite3 development.db < users.sql
python3 server/server.py