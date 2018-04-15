# mail_tracker
A project for System Programming @ TU-Sfoia

## Setup
* Install Postfix for the SMTP server. Use the default configuration\

```bash
sudo apt install postfix
```

* Install pyenv

```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

* Remove these lines from .bashrc

```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

* Install python 3.6.4 and create an environment

```bash
pyenv install 3.6.4
pyenv virtualenv 3.6.4 mail-tracker-env
pyenv activate mail-tracker-env
```

* Install python requirements.

```bash
pip install -r requirements.txt
```

* Run the db migrations

```bash
cd mail_tracker_web
python manage.py migrate
```

* Run the webserver

```bash
cd mail_tracker_web
python manage.py runserver
```

* Run the POP3 processing application in a different tab
```bash
cd pop3_client
python client.py
```
