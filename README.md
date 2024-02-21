Django Backend API

Getting started:

Prerequisites: Python and pip installed

1. Create a virtual environment
   py -m venv env

2. Activate virtual environment
   env\Scripts\activate.bat # For Mac: source env/bin/activate

3. Installing dependencies
   pip install django
   pip install djangorestframework

4. Syncing database
   py manage.py makemigrations
   py manage.py migrate

5. Run server
   py manage.py runserver
