"""Utilities for dealing with HMAC hashing
"""
import hmac
import json

def build_url_string(params):
  """Given a dictionary, return a url string of the from

    http://www.google.com?q=foo&fb=x&g=y

  Args:
    params (dict): named url parameters
      url: base string e.g. http://www.google.com
  """
  # Build the response content from previously set data
  return_str = params['url'] + '?'
  params.pop('url', None)

  # params = sorted(params.keys())
  # print(params)

  for key, value in params.iteritems():
    return_str += "%s=%s&" % (key, value)
  return return_str[:-1]


def build_hash_string(params):
  """Given a dictionary, return a frozenset of the dictionary

  Args:
    params (dict): named url parameters
  """
  # Build the response content from previously set data
  return_set = {}
  for key, value in params.iteritems():
    return_set[key] = value
  return json.dumps(return_set)


def create_hmac_digest(secret_key, message):
  """Given a key and a message, create an HMAC digest of the message

    This uses the HMAC.hexdigest() function.
    The digester is created with the default MD5 hashing algorithm.

  Args:
    key (string): a secret key used in the hmac digest algorithm
    message (string): the message to digest
  """
  digester = hmac.new(
    key=secret_key,
    msg=message
  )
  return digester.hexdigest()
