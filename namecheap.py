import requests
import os
import xml.etree.cElementTree as ET
from enum import Enum

class Record():
    def __init__(self, index, recordDict):
        self.index = index
        self.name = recordDict.get('Name', 'undefined')
        self.recordType = recordDict.get('Type', 'A')
        self.address = recordDict.get('Address', '127.0.0.1')
        self.MXPref = recordDict.get('MXPref', 10)
        self.ttl = recordDict.get('TTL', 300)

    def __str__(self):
        res = "&HostName{0}={1}&RecordType{0}={2}&Address{0}={3}&TTL{0}={4}".format(self.index, self.name, self.recordType, self.address, self.ttl)
        if self.recordType == "MX":
            return res + "&MXPref{0}={1}".format(self.index, self.MXPref)
        return res

    def __repr__(self):
        return str(self)


class DomainsDNS():
    def __init__(self):
        self.baseUrl = "https://api.namecheap.com/xml.response"
        self.apiUser = os.environ['API_USER']
        self.apiKey = os.environ['API_KEY']
        self.username = os.environ['USERNAME']
        self.clientIp = os.environ['CLIENT_IP']
        self.sld = os.environ['SLD']
        self.tld = os.environ['TLD']
    
    def __str__(self):
        return "{0}?ApiUser={1}&ApiKey={2}&UserName={3}&ClientIp={4}".format(self.baseUrl, self.apiUser, self.apiKey, self.username, self.clientIp)

    def __repr__(self):
        return "DomainsDNS -- URL: " + str(self)

    def get(self):
        return requests.get(str(self))

    def post(self):
        return requests.post(str(self))


class GetHosts(DomainsDNS):
    def __init__(self):
        super().__init__()
        self.command = "namecheap.domains.dns.getHosts"

    def __str__(self):
        return super().__str__() + "&Command={}".format(self.command)

    def __repr__(self):
        return "GetHosts -- URL: " + str(self)
        

class SetHosts(DomainsDNS):
    def __init__(self, records):
        super().__init__()
        self.command = "namecheap.domains.dns.setHosts"
        self.records = records
    
    def __str__(self):
        res = super().__str__() + "&Command={}".format(self.command)
        for i in self.records:
            res += str(i)
        return res

    def __repr__(self):
        return "SetHosts -- URL: " + str(self)


def main():
    resp = GetHosts().get().text
    print(resp)
    root = ET.fromstring(resp)
    records = []
    index = 1
    namespace = "{http://api.namecheap.com/xml.response}"

    for host in root.iter(namespace + "host"):
        record = Record(index, host.attrib)
        records.append(record)
        index += 1

    print(SetHosts(records))


main()
