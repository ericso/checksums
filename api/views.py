import json
from copy import deepcopy

from django.shortcuts import render
from django.http import HttpResponse, Http404
# from django.http import JsonResponse

from checksums.settings import SECRET_KEY
from api.digest import build_url_string, build_hash_string, create_hmac_digest


def _remove_key(d, key):
  """Returns a copy of the dictionary with specified key removed
  """
  r = deepcopy(d)
  del r[key]
  return r


def createchecksum(request):
  """Returns a HMAC checksum digest
  """
  request_params = {}
  for key, value in request.GET.iteritems():
    request_params[key] = value

  # Build checksum string and create the checksum
  request_str = build_url_string(deepcopy(request_params))
  checksum = create_hmac_digest(
    SECRET_KEY,
    build_hash_string(deepcopy(request_params))
  )

  # Send the URL string as the response
  response_str = request_str + "&checksum=%s" % (checksum,)
  return HttpResponse(response_str)


def verifychecksum(request):
  """Takes a request and verifies the checksum
  """
  request_params = {}
  for key, value in request.GET.iteritems():
    request_params[key] = value

  # Get the checksum and remove it from request_params
  checksum_to_verify = request_params.pop('checksum', None)
  # request_params = _remove_key(request_params, 'checksum')

  # Remove checksum parameter, build checksum string, get checksum
  request_str = build_url_string(deepcopy(request_params))

  checksum = create_hmac_digest(
    SECRET_KEY,
    build_hash_string(deepcopy(request_params))
  )

  if checksum_to_verify == checksum:
    return HttpResponse('verified')
  else:
    raise Http404("Url object checksum does not match")

  # # Get Url object from database matching url and params
  # try:
  #   url = Url.objects.get(
  #     url=request_params['url'],
  #     params=json.dumps(_remove_key(request_params, 'url'))
  #   )
  # except:
  #   raise Http404("Could not find Url object")
  # else:
  #   if url.checksum == checksum:
  #     return HttpResponse('verified')
  #   else:
  #     raise Http404("Url object checksum does not match")
