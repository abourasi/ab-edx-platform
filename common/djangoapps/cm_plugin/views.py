import re
import logging
from urllib.parse import urlparse
from django.http import JsonResponse
from django.shortcuts import render

log = logging.getLogger(__name__)

def set_cookie(request):
    referrer = request.GET.get('return_to_url')

    allowedDomains = ['edcast.com', 'edcast.me', 'edcastcloud.com']
    if not is_edcast_url(request.META['HTTP_REFERER'], allowedDomains):
        return JsonResponse({"error": "invalid url"}, status=404)

    response = render(request, 'cm_plugin/cookie.html', {'referrer': referrer})
    response.set_cookie(key='visited', value='true')

    return response

def is_edcast_url(url, allowedDomains):
    parsed_uri = urlparse(url)

    if parsed_uri.scheme is not None and (parsed_uri.scheme not in ['http', 'https']):
        return False

    domain = '{uri.netloc}'.format(uri=parsed_uri)
    domainArray = domain.split('.')
    arrayLength = len(domainArray)

    domain = domainArray[arrayLength - 2] + '.' + domainArray[arrayLength - 1]

    if url is not None and (domain in allowedDomains):
        return True
    else:
        return False
