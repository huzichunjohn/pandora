import json
import requests
from requests.exceptions import ConnectionError, SSLError, Timeout

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import Domain

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DnspodMixin(object):

    @staticmethod
    def get_default_headers():
        return {
            "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)",
        }

    @staticmethod
    def get_default_data():
        return {
            "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
            "format": "json",
            "lang": "cn"
        }
    
    def get_dnspod_response(self, url, data=None, headers=None):
        self.data = data if data else self.get_default_data()
        self.headers = headers if headers else self.get_default_headers()

        try:
            response = requests.post(url, data=self.data, headers=self.headers)
        except (ConnectionError, SSLError):
            return {
                'code': 502,
                'error': 'Bad gateway'
            }
        except (Timeout):
            return {
                'code': 504,
                'error': 'Gateway time out'
            }

        data = response.json()
        return {
            'code': 200,
            'data': data
        }

class DomainList(DnspodMixin, APIView):
    """
    List all domains, or create a new domain.
    """
    def get_lines(self, domain_id, domain_grade="D_Free"):
        url = "https://dnsapi.cn/Record.Line"
        data = self.get_default_data()
        data.update({
            "domain_id": domain_id,
            "domain_grade": domain_grade
        })
        self.headers = self.get_default_headers()

        result = self.get_dnspod_response(url)
        status = result['code']
        data = result['data']

        if status == 200 and data['status']['code'] == "1":
            return data['line_ids']
        else:
            Exception("failed to get lines")

    def get(self, request, format=None):
        url = "https://dnsapi.cn/Domain.List"
        result = self.get_dnspod_response(url)
        status = result['code']

        if status == 200:
            body = result['data']
        else:
            body = result

        return Response(body, status)

    def post(self, request, format=None):
        url = "https://dnsapi.cn/Domain.Create"
        domain = request.data['domain']

        data = self.get_default_data()
        data.update({"domain": domain})

        result = self.get_dnspod_response(url, data)
        status = result['code']

        if status == 200:
            body = result['data']
        else:
            body = result

        if status == 200 and body['status']['code'] == "1":
            domain_name = body['domain']['domain']
            domain_id = int(body['domain']['id'])
            Domain.objects.get_or_create(name=domain_name, domain_id=domain_id)

        return Response(body, status)
        
class DomainDetail(DnspodMixin, APIView):
    """
    Retrieve, update or delete a domain instance.
    """
    #def get(self, request, domain_id, format=None):
    #    url = "https://dnsapi.cn/Domain.Info"

    #    data = self.get_default_data()
    #    data.update({"domain_id": domain_id})

    #    result = self.get_dnspod_response(url, data)
    #    status = result['code']

    #    if status == 200:
    #        body = result['data']
    #    else:
    #        body = result

    #    return Response(body, status) 


    def get(self, request, domain_id, format=None):
        url = "https://dnsapi.cn/Record.List"
        
        data = self.get_default_data()
        data.update({"domain_id": domain_id})

        result = self.get_dnspod_response(url, data)
        status = result['code']

        if status == 200:
            body = result['data']
        else:
            body = result

        return Response(body, status)

    def post(self, request, domain_id, format=None):
        url = "https://dnsapi.cn/Record.Create"
        sub_domain = request.data['sub_domain']
        record_type = reqeust.data['record_type']
        record_line_id = reqeust.data['record_line_id']
        value = request.data['value']

        data = self.get_default_data()
        data.update({
            "domain_id": domain_id,
            "sub_domain": sub_domain,
            "record_type": record_type,
            "record_line_id": record_line_id,
            "value": value
        })

        result = self.get_dnspod_response(url, data)
        status = result['code']

        if status == 200:
            body = result['data']
        else:
            body = result

        return Response(body, status)

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, domain_id, format=None):
        url = "https://dnsapi.cn/Domain.Remove"

        data = self.get_default_data()
        data.update({"domain_id": domain_id})

        result = self.get_dnspod_response(url, data)
        status = result['code']
        data = result['data']

        if status == 200 and data['status']['code'] == "1":
            try:
                domain = Domain.objects.get(domain_id=domain_id)
                domain.delete()
            except Domain.DoesNotExist:
                pass

            body = result['data']
        else:
            body = result

        return Response(body, status)

class RecordDetail(DnspodMixin, APIView):
    def get(self, reqeust, domain_id, record_id, format=None):
        url = "https://dnsapi.cn/Record.Info"

        data = self.get_default_data()
        data.update({
            "domain_id": domain_id,
            "record_id": record_id
        })

        result = self.get_dnspod_response(url, data)
        status = result['code']
        data = result['data']

        if status == 200:
            body = result['data']
        else:
            body = result

        return Response(body, status)

    def delete(self, reqeust, domain_id, record_id, format=None):
        url = "https://dnsapi.cn/Record.Remove"

        data = self.get_default_data()
        data.update({
            "domain_id": domain_id,
            "record_id": record_id
        })

        result = self.get_dnspod_response(url, data)
        status = result['code']
        data = result['data']

        if status == 200:
            body = result['data']
        else:
            body = result

        return Response(body, status)
