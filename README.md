# Django Backend - Notes API

### Prerequisites:

Install python and pip

Clone this repository to your local machine. Follow below steps starting from the root directory:


## Getting started:

1. Create a virtual environment
   `py -m venv env`

2. Activate virtual environment

    ```
    For windows: env\Scripts\activate.bat
    For Mac: source env/bin/activate
    ```

3. Installing dependencies

    ```
    pip install django
    pip install djangorestframework
    ```

4. Syncing database

    ```
    py manage.py makemigrations
    py manage.py migrate
    ```

5. Run server
   `py manage.py runserver`


### Prerequisites to test API:

Install VS Code and install extension REST Client by Huachao Mao

Open test-api.rest file and start sending request to the backend API


## Database Tables

> USER : Fields ( id, username, email, password )

> NOTE : Fields ( note_id, email, title, content, date_created )

> EDIT_NOTE : Fields ( note_id, user_id, date_edited, content )

> SHARE_NOTE : Fields ( note_id, user_id )
