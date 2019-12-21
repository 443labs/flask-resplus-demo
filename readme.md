# Flask Restplus Demo

**Contributors**
* Mark Belles
* Jeremy Couser
* Jason Coon

**Abstract**

The goal of this project is to provide a simple example of a real-world backend server application, using off the shelf Python modules.

Each functional area will be documented, and provide a portfolio reference point for explaining each area.

**Tech Stack**

The following modules comprise our technology stack.

* Database: 
  * Engine: Postgresql
  * ORM: SqlAlchemy `pip install sqlalchemy`
  * Migrations: Alembic `pip install alembic`
* REST:
  * Flask `pip install flask`
  * Flask-Restplus `pip install flask-restplus`
  * Flask-Restplus-Patched `pip install flask-restplus-patched` (to add support for Marshmallow)
  * Flask-Marshmallow `pip install flask-marshmallow` (serialization and validation of DTOs)
* Authentication: 
  * Flask-Login `pip install flask-login`
  * Flask-Oauth `pip install flask-oauth`
  * Authentication Schemes: Basic, Hmac, API-Key, OAuth

----
# Initial Setup

The following steps should be taken after cloning the respository.

**Prerequisites**
* Python 3.6.1 (recommend pyenv for version management)
* Postgresql

Run the following commands from a terminal in the root folder of the project:

```
# create a virtual environment
python3 -m venv venv

# add the src folder to the virtual environment, to avoid haivng to specify PYTHONPATH if running from the command line (optional)
echo "$(pwd)/src" > venv/lib/python3.6/site-packages/MY_VENV_PYTHONPATH.pth

# activate the virtual environment
. venv/bin/activate

# upgrade pip
pip install --upgrade pip

# install requirements
pip install -r requirements.txt

# create the db
createdb flask-restplus-demo

# run any pending migrations
alembic upgrade head

# launch locally
python3 src/egl/app.py

```

At this point the server is running, so you may exercise it accordingly (curl, wget, fetch, postman, swagger ui, etc.)

----
# Swagger UI

Visit <http://0.0.0.0:5000/api/v1> in your browser.

----
# Containerization

More to come...

----
# Freezing Requirements

Please run the following command to freeze requirements in a consistent manner, when adding new modules to the project.

`pip freeze | LC_COLLATE=C sort > requirements.txt`
