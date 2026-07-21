# Login and Signup Pages

- [Login and Signup Pages](#login-and-signup-pages)
- [Setup your db for Login Credentials](#setup-your-db-for-login-credentials)
- [Create the login page](#create-the-login-page)
- [Create the signup page](#create-the-signup-page)
- [Setup the index.py](#setup-the-indexpy)
- [Add logout link to the navbar](#add-logout-link-to-the-navbar)

## Setup your db for Login Credentials

- Add your table for users
  - table name: `users`
  - fields

    - `user_id serial primary key not null`
    - `user_name varchar(32) unique`
    - `user_password varchar(64) not null`
    - `user_modified_on timestamp without time zone default now()`
    - `user_delete_ind boolean default false`

## Create the login page

- See `IE271caseapp/apps/login.py` for the layout

  - Use `type='password'` for `dbc.Input` to hide texts in passwords

- It looks like movieprofile in this case but you can always design it differently
- Check the callback for the login process

  - Querying the credentials into the database
  - Using a hash on the password before checking credentials
  - If trigger is...
    - login button -- query if the credentials are in the db
    - logout (via `sessionlogout` variable) -- reset the session variables to values that correspond to logging out

## Create the signup page

1. Copy `login.py` and paste in the same page. You should have `login copy.py`.
2. Rename the copy into `signup.py`.
3. Simply rename the fields to make it look like a signup page. We are assuming that each user only need a username and password since this is only a demo. In real-life, this might not be the case.
4. Create the callbacks for the signup page. See `IE271caseapp/apps/signup.py` for the relevant source code.
-* Find how passwords are **_hashed_** prior to saving to the db

_Optional_: You may also want the following controls to the signup page:

- Checking for strong passwords
- Checking for duplicate usernames
- Feedbacks for duplicate usernames

## Setup the index.py

1. Go to index.py.
2. Add `dcc.Store` elements to save login credentials (i.e. details necessary during the session)
   - `sessionlogout` -- bool, indicator on whether the session is logged-in or not
   - `currentuserid` -- int, stores the user_id of the current user; if logged-out, has a value -1
   - `currentrole` -- int, stores the role_id (if any) of the current user; if logged_out, has a value of -1
3. Put the `Navbar` inside a `Div` so we can hide it when the user is not logged in
4. Edit the callback to add `login.py` and `signup.py`
   1. Note how login-states are checked prior to routing to the correct pages
      - `login` and `signup` pages are only accessible if the user is not signed in (i.e. session userid = -1)
   2. The `sessionlogout` variable, bool, is decided based on various indicators for login-status.
   3. The navbar is hidden (or shown) based on the value of `sessionlogout`.

## Add logout link to the navbar

1. Add a link so you can logout.
2. Incorporate the logout URL to `index.py` so it leads to the proper landing page.
