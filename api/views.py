import json
from copy import deepcopy

from django.shortcuts import render
from django.http import HttpResponse, Http404
# from django.http import JsonResponse

from checksums.settings import SECRET_KEY
from api.digest import build_hash_string, create_hmac_digest
from api.utils import parse_url_params, build_url_string


def createchecksum(request):
  """Returns a HMAC checksum digest
  """
  request_params = parse_url_params(request.GET)

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
  request_params = parse_url_params(request.GET)

  # Get the checksum and remove it from request_params
  checksum_to_verify = request_params.pop('checksum', None)

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
