from copy import deepcopy

from django.test import TestCase

from checksums.settings import SECRET_KEY
from api.digest import build_hash_string, create_hmac_digest
from api.utils import parse_url_params, build_url_string

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
    # Create the string to be passed to the API in the url parameter
    url_param_string = build_url_string(deepcopy(self.url_params))

    response = self.client.get(
      '/api/createchecksum/?url=' + url_param_string,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    # Create the HMAC digest and append
    checksum = create_hmac_digest(
      SECRET_KEY,
      build_hash_string(deepcopy(self.url_params))
    )
    check_content = url_param_string + "&checksum=%s" % (checksum,)
    self.assertEqual(response.content, check_content)


  def test_api_verifychecksum_verifies_correctly(self):
    # Create the string to be passed to the API in the url parameter
    url_param_string = build_url_string(deepcopy(self.url_params))

    response = self.client.get(
      '/api/createchecksum/?url=' + url_param_string,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    response_string = response.content
    response_params = _get_params(response.content)
    returned_checksum = response_params['checksum']
    check_content = response_string + "&checksum=" + returned_checksum

    response = self.client.get(
      '/api/verifychecksum/?url=' + check_content,
      HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, 'verified')


  def test_api_verifychecksum_returns_404_on_verification_failure(self):
    # Create the string to be passed to the API in the url parameter
    url_param_string = build_url_string(deepcopy(self.url_params))
    verify_fail_string = url_param_string + "&checksum=notavalid"

    response = self.client.get(
      '/api/verifychecksum/?url=' + verify_fail_string,
      HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    self.assertEqual(response.status_code, 404)
