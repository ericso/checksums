An app that calculates a checksum from a given callback url to verify on a subsequent call.

Routes:

    GET /api/createchecksum - Returns the provided URL with a checksum value
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

Usage:

  Make a get request to /api/createchecksum:

    GET /api/createchecksum/?url=http://www.example.com/?param1=val1

  The request will return a string with the sent url and a checksum:

    http://www.example.com/?param1=val1&checksum=somechecksum

  To verify the checksum:

    GET /api/verifychecksum/?url=http://www.example.com/?param1=val1&checksum=somechecksum

  The request will either return 200 OK with "verified" in the content or a 404 error if not verified
