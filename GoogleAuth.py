#!/bin/env python3
"""
	This script will read through a Google Auth backup
	and print the QR codes for each entry.
	This will let you import them into a new (non-rooted) phone.
"""

from urllib.parse import urlencode
import sqlite3, qrcode
"""
	Database file stored at:
	/data/data/com.google.android.apps.authenticator2/databases/databases

	Schema:
	CREATE TABLE accounts(
		_id INTEGER PRIMARY KEY,
		email TEXT NOT NULL,
		secret TEXT NOT NULL,
		counter INTEGER DEFAULT 0,
		type INTEGER,
		provider INTEGER DEFAULT 0,
		issuer TEXT DEFAULT NULL,
		original_name TEXT DEFAULT NULL
	);
"""

authdb = sqlite3.connect('GoogleAuth.db')

cursor = authdb.cursor()
accounts = cursor.execute('SELECT * FROM accounts')

authURL = 'otpauth://totp/{0}?{1}'

for index,row in enumerate(accounts, start=1):
	# URL format: https://github.com/google/google-authenticator/wiki/Key-Uri-Format
	# We only needs certain fields out of the database to build our URL
	fields = {
		"secret": row[2]
	}
	if row[6] is not None:
		fields['issuer'] = row[6]

	account = authURL.format(row[1].replace(' ', '+'), urlencode(fields))
	img = qrcode.make(account)
	img.save('codes/{0:02d}-{1}.png'.format(index, row[1].replace('/', '_').replace(' ', '_')))

cursor.close()
authdb.close()
