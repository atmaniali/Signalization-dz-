
# Signalisation Dz

It's a ecommerce site when user can chose a Traaffic Signs and dimension and adding it in his cart. 


## Authors

- [@atmaniali](https://github.com/atmaniali/)


## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## Features

- admine pannel
- user authentication
- tracking order
- Cross platform


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`


## Installation

Clone the project

```bash
  git clone https://github.com/atmaniali/Signalization-dz-.git
```

Go to the project directory

```bash
  cd Signalization-dz
```

Create virtual environment

```bash
  python -m venv venv
```

Activate virtual environment on windows

```bash
  venv/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Create `.env` file in directory

```bash
    touch .env
```

Add 
- SECRET_KEY = hash code to secure django application type string
- DEBUG = type boolean if it's true. they will show error in page
- ALLOWED_HOSTS = it's a list off local host separate by ","
- SESSION_COOKIE_SECURE = it's type boolean
- CSRF_COOKIE_SECURE = it's type boolean
- MY_EMAIL_HOST = smtp.gmail.com
- MY_EMAIL_HOST_USER = gmil of site
- MY_EMAIL_HOST_PASSWORD = password
- MY_EMAIL_PORT = 587
- MY_EMAIL_USE_TLS = True
- SECURE_HSTS_SECONDS = type number 86400
- SECURE_HSTS_PRELOAD = boolean True
- SECURE_HSTS_INCLUDE_SUBDOMAINS = boolean True
- SECURE_BROWSER_XSS_FILTER=True
- SECURE_CONTENT_TYPE_NOSNIFF=True
- SECURE_SSL_REDIRECT=True


