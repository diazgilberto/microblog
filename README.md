# Flask Tutorial

### Environment Commands:
#### Flask
- `export FLASK_APP=<app_entry_file.py>`
- `export FLASK_ENV=development`
- `flask db migrate '<migration message>'`
- `flask db upgrade`

### Requirements:
#### User Login Page
- Should be able to create and account
- Should reject the creation of new account if username or email already exist
- Username and email should be unique
- Session should be stored
- If user already logged in, and try to login again, should redirect to index
- Should remember username if user allows
- User should be able to recover password
- Application should have protected routes, available for logged in users only
#### User Profile Page
- Track last time user visit page
- Should have default gravatar
#### Error Handling
We want to send an email immediately a 500 occurs 
##### `confing.py` with environment variable with the same name
- `MAIL_SERVER = os.environ.get('MAIL_SERVER')`
- `MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)`
- `MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None` encrypted connection or not
- `MAIL_USERNAME = os.environ.get('MAIL_USERNAME')`
- `MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')`
- `python -m smtpd -n -c DebuggingServer localhost:8025` local mail server

