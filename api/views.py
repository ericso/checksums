import json
import hmac

from django.shortcuts import render
from django.http import HttpResponse
# from django.http import JsonResponse

from checksums.settings import SECRET_KEY


def createchecksum(request):

  # get URL params
  request_params = {}
  request_str = ''
  for key, value in request.POST.iteritems():
    request_params[key] = value
    if key == 'url':
      request_str = value + "?"
    else:
      request_str += "%s=%s&" % (key, value)
  request_str = request_str[:-1]

  # print(request_params)
  # print(request_str)

  # Create the HMAC digest and append
  digester = hmac.new(
    key=SECRET_KEY,
    msg=request_str
  )
  digest = digester.hexdigest()
  response_str = request_str + "&checksum=%s" % (digest,)

  # Save URL and checksum to database


  # Send the URL string as the response
  return HttpResponse(response_str)



def verifychecksum(request):
  return HttpResponse()
