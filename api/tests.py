import json
from copy import deepcopy

from django.test import TestCase

from checksums.settings import SECRET_KEY
from api.models import Url
from api.digest import build_url_string, create_hmac_digest


class ApiTest(TestCase):
  """Test class for api
  Routes:
  POST /api/createchecksum - Returns the provided URL with a checksum value
  GET /api/verifychecksum - Returns a 200 or 404 response depending on whether the provided checksum verifies against provided URL
  """

  def setUp(self):
    """Create a test location in the database
    """
    self.url_params = {
      'url': "http://www.google.com",
      'q': 'foo',
      'fb': 'x',
      'g': 'y',
      'superman': 'batman',
      'bobloblaw': 'blahblahblah',
    }

  def tearDown(self):
    """Clear test database
    """
    pass


  ### Test Methods ###
  def test_api_createchecksum_returns_200(self):
    response = self.client.post(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    self.assertEqual(response.status_code, 200)


  def test_api_createchecksum_returns_checksum(self):
    response = self.client.post(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    # Build the response content from previously set data
    response_content = build_url_string(self.url_params)
    print('response_content in test: %s' % (response_content,))

    # Create the HMAC digest and append
    digest = create_hmac_digest(SECRET_KEY, response_content)
    response_content += "&checksum=%s" % (digest,)

    self.assertEqual(response.content, response_content)


  def test_api_verifychecksum_verifies_correctly(self):
    # POST request to create entry in database
    self.client.post(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    # Build the response content from previously set data
    check_content = build_url_string(self.url_params)

    # Create the HMAC digest and append
    digest = create_hmac_digest(SECRET_KEY, check_content)

    check_params = deepcopy(self.url_params)
    check_params['checksum'] = digest

    response = self.client.get(
      '/api/verifychecksum/',
      check_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, 'verified')


  def test_api_verifychecksum_returns_404_on_verification_failure(self):
    # POST request to create entry in database
    self.client.post(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    verify_params = self.url_params
    verify_params['checksum'] = 'not a real checksum'
    response = self.client.get(
      '/api/verifychecksum/',
      verify_params,
      HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    self.assertEqual(response.status_code, 404)
