import json
from copy import deepcopy

from django.shortcuts import render
from django.http import HttpResponse, Http404
# from django.http import JsonResponse

from checksums.settings import SECRET_KEY
from api.models import Url
from api.digest import build_url_string, create_hmac_digest


def _remove_key(d, key):
  """Returns a copy of the dictionary with specified key removed
  """
  r = deepcopy(d)
  del r[key]
  return r


def createchecksum(request):
  """Returns a HMAC digest
  """
  request_str = build_url_string(request.POST)
  request_params = {}
  for key, value in request.POST.iteritems():
    request_params[key] = value

  # Create the checksum
  digest = create_hmac_digest(SECRET_KEY, request_str)

  # Save URL and checksum to database
  Url.objects.create(
    url=request_params['url'],
    params=json.dumps(_remove_key(request_params, 'url')),
    checksum=digest
  )

  # Send the URL string as the response
  response_str = request_str + "&checksum=%s" % (digest,)
  return HttpResponse(response_str)


def verifychecksum(request):
  """Takes a request and verifies the checksum
  """
  # Remove checksum parameter and build checksum string
  request_str = build_url_string(_remove_key(request.GET, 'checksum'))
  request_params = {}
  for key, value in request.GET.iteritems():
    request_params[key] = value

  # Get the checksum and remove it from request_params
  checksum = request_params['checksum']
  request_params = _remove_key(request_params, 'checksum')

  # Get Url object from database matching url and params
  try:
    url = Url.objects.get(
      url=request_params['url'],
      params=json.dumps(_remove_key(request_params, 'url'))
    )
  except:
    raise Http404("Could not find Url object")
  else:
    if url.checksum == checksum:
      return HttpResponse('verified')
    else:
      raise Http404("Url object checksum does not match")
