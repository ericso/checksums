An app that calculates a checksum from a given callback url to verify on a subsequent call.

Routes:

    POST /api/createchecksum - Returns the provided URL with a checksum value
    GET /api/verifychecksum - Returns a 200 or 404 response depending on whether the provided checksum verifies against provided URL


Clone this repo:

    git clone git@github.com:ericso/checksums.git


Create a virtual environment, or not. But if you do, use virtualenvwrapper:

  https://virtualenvwrapper.readthedocs.org/en/latest/

    mkvirtualenv checksums

Run the app:

    pip install -r requirements
    python manage.py runserver


Run the tests:

    python manage.py test
