import requests
import os
import copy
import itertools
import xml.etree.cElementTree as ET
from enum import Enum


class Record():
    def __init__(self, record_dict):
        assert type(record_dict) == dict, "record_dict should be a dictionary"
        self.index = ""
        self.name = record_dict.get('Name', 'undefined')
        self.record_type = record_dict.get('Type', 'A')
        self.address = record_dict.get('Address', '127.0.0.1')
        self.mx_pref = record_dict.get('MXPref', 10)
        self.ttl = record_dict.get('TTL', 300)

    def __str__(self):
        res = "&HostName{0}={1}&RecordType{0}={2}&Address{0}={3}&TTL{0}={4}".format(
            self.index, self.name, self.record_type, self.address, self.ttl)
        if self.record_type == "MX":
            return res + "&MXPref{0}={1}".format(self.index, self.mx_pref)
        return res

    def __repr__(self):
        return str(self)


class DomainsDNS():
    def __init__(self):
        self._base_url = "https://api.namecheap.com/xml.response"
        self._api_user = os.environ['API_USER']
        self._api_key = os.environ['API_KEY']
        self._username = os.environ['USERNAME']
        self._client_ip = os.environ['CLIENT_IP']
        self._sld = os.environ['SLD']
        self._tld = os.environ['TLD']

    def __str__(self):
        return "{0}?ApiUser={1}&ApiKey={2}&UserName={3}&ClientIP={4}&SLD={5}&TLD={6}"\
            .format(self._base_url, self._api_user, self._api_key, self._username, self._client_ip, self._sld, self._tld)

    def __repr__(self):
        return "DomainsDNS -- URL: " + str(self)

    def get(self):
        return requests.get(str(self))

    def post(self):
        return requests.post(str(self))


class GetHosts(DomainsDNS):
    def __init__(self):
        super().__init__()
        self._command = "namecheap.domains.dns.getHosts"

    def __str__(self):
        return super().__str__() + "&Command={}".format(self._command)

    def __repr__(self):
        return "GetHosts -- URL: " + str(self)


class SetHosts(DomainsDNS):
    def __init__(self, records=[]):
        super().__init__()
        self._command = "namecheap.domains.dns.setHosts"
        self._records = []
        self.add_records(records)

    def add_records(self, records):
        assert type(records) == list
        [self.add_record(i) for i in records]
        return self

    def add_record(self, record):
        assert type(record) == Record
        self._records.append(copy.copy(record))
        return self

    def remove_record(self, name, record_type):
        assert type(name) == str, "Host name should be a valid string"
        self._records = [
            i for i in self._records
            if i.name != name or i.record_type != record_type
        ]
        return self

    def __str__(self):
        res = super().__str__() + "&Command={}".format(self._command)
        cnt = itertools.count(1)
        for i in self._records:
            i.index = next(cnt)
            res += str(i)
        return res

    def __repr__(self):
        return "SetHosts -- URL: " + str(self)


def main():
    res = GetHosts().get().text
    root = ET.fromstring(res)
    ns = "{http://api.namecheap.com/xml.response}"

    set_hosts = SetHosts().add_records(
        [Record(i.attrib) for i in root.iter(ns + "host")])

    set_hosts.add_record(
        Record({
            "Name": "_acme-challenge",
            "Type": "TXT",
            "Address": "test 123"
        }))

    print(set_hosts)
    set_hosts.remove_record("_acme-challenge", "TXT")
    print(set_hosts)

    # print(SetHosts(records).post().text)


def hello():
    print("Hello World!")
