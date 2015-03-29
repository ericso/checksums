"""General utilities"""

from copy import deepcopy

def parse_url_params(d):
  """Returns a dictionary of the url parameters of a request of the form:

    GET /api_endpoint/?url=http://www.google.com/?param1=value1&param2=value2
  """
  request_params = {}
  for key, value in d.iteritems():
    if key == 'url' and '?' in value:
      request_params[key] = value.split('?')[0]
      first_key = value.split('?')[1].split('=')[0]
      first_value = value.split('?')[1].split('=')[1]
      request_params[first_key] = first_value
    else:
      request_params[key] = value
  return request_params


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

  for key, value in params.iteritems():
    return_str += "%s=%s&" % (key, value)
  return return_str[:-1]
