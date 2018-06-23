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
