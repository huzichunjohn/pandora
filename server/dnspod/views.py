import json
import requests
from requests.exceptions import ConnectionError, SSLError, Timeout

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

DEFAULT_HEADERS = {
    "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
}

DEFAULT_PAYLOADS = {
    "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
    "format": "json",
    "lang": "cn"
}

class ProxyView(APIView):
    def proxy(self, url, data, headers):
        try:
            response = requests.post(url, data=data, headers=headers)
        except (ConnectionError, SSLError):
            status = requests.status_codes.codes.bad_gateway
            return Response({
                'code': status,
                'error': 'Bad gateway'
            }, status)
        except (Timeout):
            status = requests.status_codes.codes.gateway_timeout
            return Response({
                'code': status,
                'error': 'Gateway time out'
            }, status)

        return HttpResponse(response.text, status=response.status_code,
                content_type='application/json; charset=utf-8')

class DomainList(ProxyView):
    """
    List all domains, or create a new domain.
    """
    def get(self, request, format=None):
        url = "https://dnsapi.cn/Domain.List"
        data = DEFAULT_PAYLOADS
        headers = DEFAULT_HEADERS

        return self.proxy(url, data=data, headers=headers)

    def post(self, request, format=None):
        url = "https://dnsapi.cn/Domain.Create"
        data = request.data.copy()
        data.update(DEFAULT_PAYLOADS)
        headers = DEFAULT_HEADERS

        return self.proxy(url, data=data, headers=headers)

class DomainDetail(APIView):
    """
    Retrieve, update or delete a domain instance.
    """
    def get(self, request, pk, format=None):
        pass

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass
