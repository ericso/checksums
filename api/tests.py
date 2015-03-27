import json
import hmac

from django.test import TestCase

from checksums.settings import SECRET_KEY
from api.models import Url



class ApiTest(TestCase):
  """Test class for api
  Routes:
  POST /api/createchecksum - Returns the provide URL with a checksum value
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
    }
    # self.model_params = {
    #   'url': "http://www.google.com",
    #   'url_params': json.dumps(self.url_params),
    # }

    # new_url = Url.objects.create(**self.model_params)
    # new_url.save()

  def tearDown(self):
    """Clear test database
    """
    # Url.objects.all().delete()


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
    response_content = ''
    for key, value in self.url_params.iteritems():
      if key == 'url':
        response_content = self.url_params['url'] + '?'
      else:
        response_content += "%s=%s&" % (key, value)
    response_content = response_content[:-1]

    # Create the HMAC digest and append
    digester = hmac.new(
      key=SECRET_KEY,
      msg=response_content
    )
    digest = digester.hexdigest()
    response_content += "&checksum=%s" % (digest,)

    print("from request: %s" % (response.content,))
    print("built locally: %s" % (response_content,))

    self.assertEqual(response.content, response_content)


  # def test_api_verifychecksum_returns_404(self):
  #   verify_params = self.model_params
  #   verify_params['checksum'] = 'not a real checksum'
  #   response = self.client.get(
  #     '/api/verifychecksum/',
  #     verify_params,
  #     HTTP_X_REQUESTED_WITH='XMLHttpRequest',
  #   )
  #   self.assertEqual(response.status_code, 404)
