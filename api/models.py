from django.db import models


class Url(models.Model):
  """Stores a url base, JSONified string of the url parameters, and an
  HMAC digest representing the checksum of the full url
  """
  url = models.CharField(max_length=256)
  params = models.CharField(max_length=512)
  checksum = models.CharField(max_length=512)
