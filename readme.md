### Application project for MOOC.FI Cyber Security Base 2025 course

The purpose of the code in this repository is to showcase various security flaws described in the OWASP Top 10 (2021) report with potential fixes for them.
This repository contains code that is purposefully **insecure** and **not suitable for production**
(less so with the fixes implemented discussed in commented blocks throughout the codebase,
but the options file, for example, is still not production ready in it's current configuration).

Installation:
Install Python 3.12 or newer and Django 5.0 or newer.

After cloning the repository change the secret key in [settings.py](/csb_project1_onykan/settings.py)
and then run the following commands:

`python manage.py makemigrations`

followed by

`python manage.py migrate`

to initialize the database.

Run `python manage.py createsuperuser` to create a superuser to manage the admin panel at `*root*/admin`.

Run `python manage.py runserver` to start the development server.

Licensed under the MIT license. See "[license.md](/license.md)" for more information.