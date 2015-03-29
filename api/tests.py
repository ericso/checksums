from copy import deepcopy

from django.test import TestCase

from checksums.settings import SECRET_KEY
from api.digest import build_url_string, build_hash_string, create_hmac_digest


def _get_params(url):
  params = url.split('?')[1]
  params = params.split('&')

  pairs = {}
  for pair in params:
    pairs[pair.split('=')[0]] = value = pair.split('=')[1]
  return pairs


class ApiTest(TestCase):
  """Test class for api
  Routes:
  GET /api/createchecksum - Returns the provided URL with a checksum value
  GET /api/verifychecksum - Returns a 200 or 404 response depending on whether the provided checksum verifies against provided URL
  """

  def setUp(self):
    self.url_params = {
      'url': "http://www.google.com",
      'q': 'foo',
      'fb': 'x',
      'g': 'y',
    }

  def tearDown(self):
    pass


  ### Test Methods ###
  def test_api_createchecksum_returns_200(self):
    response = self.client.get(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    self.assertEqual(response.status_code, 200)


  def test_api_createchecksum_returns_checksum(self):
    response = self.client.get(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    # Build the response content from previously set data
    check_content = build_url_string(deepcopy(self.url_params))

    # Create the HMAC digest and append
    digest = create_hmac_digest(
      SECRET_KEY,
      build_hash_string(deepcopy(self.url_params))
    )
    check_content += "&checksum=%s" % (digest,)
    self.assertEqual(response.content, check_content)


  def test_api_verifychecksum_verifies_correctly(self):
    response = self.client.get(
      '/api/createchecksum/',
      self.url_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    params = _get_params(response.content)
    returned_checksum = params['checksum']

    check_params = deepcopy(self.url_params)
    check_params['checksum'] = returned_checksum

    response = self.client.get(
      '/api/verifychecksum/',
      check_params,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, 'verified')


  def test_api_verifychecksum_returns_404_on_verification_failure(self):
    # POST request to create entry in database
    self.client.get(
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
