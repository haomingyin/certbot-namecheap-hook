import requests
import os
import copy
import xml.etree.ElementTree as etree


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
    """
    Namecheap API: domains.dns [https://www.namecheap.com/support/api/methods.aspx]
    """

    def __init__(self):
        self._base_url = "https://api.namecheap.com/xml.response"
        self._api_user = os.environ['API_USER']
        self._api_key = os.environ['API_KEY']
        self._username = os.environ['USERNAME']
        self._client_ip = os.environ['CLIENT_IP']
        domain_name = os.environ['CERTBOT_DOMAIN']
        # top level domain
        tld = self._tld = os.environ.get('TLD', domain_name.rsplit('.', 1)[-1])
        # second level domain
        sld = self._sld = domain_name[:-(len(tld) + 1)].rsplit('.', 1)[-1]
        # third, fourth, next (nth) level domain
        self._nld = domain_name[:-(len(tld) + len(sld) + 2)]

    def __str__(self):
        return "{0}?ApiUser={1}&ApiKey={2}&UserName={3}&ClientIP={4}&SLD={5}&TLD={6}"\
            .format(self._base_url, self._api_user, self._api_key, self._username, self._client_ip, self._sld, self._tld)

    def _process_response(self, resp):
        ns = "{http://api.namecheap.com/xml.response}"
        root = etree.fromstring(resp.text)
        status = root.attrib["Status"]
        if status.lower() == "error":
            error = root.findall("./{0}Errors/{0}Error".format(ns))[0].text
            print("[Namecheap] Error: " + error)
        else:
            cmd = root.findall("./{0}RequestedCommand".format(ns))[0].text
            print("[Namecheap] Ok: " + cmd)
        return resp

    def format_record_name(self, name):
        assert type(name) == str, "Host name should be a valid string"

        if not self._nld:
            return name

        return "{0}.{1}".format(name, self._nld)

    def get(self):
        return self._process_response(requests.get(str(self)))

    def post(self):
        return self._process_response(requests.post(str(self)))


class GetHosts(DomainsDNS):
    """
    Namecheap API: domains.dns.getHosts [https://www.namecheap.com/support/api/methods/domains-dns/get-hosts.aspx]
    """

    def __init__(self):
        super().__init__()
        self._command = "namecheap.domains.dns.getHosts"

    def get_records(self):
        res = self.get().text
        ns = "{http://api.namecheap.com/xml.response}"

        records = []
        for i in etree.fromstring(res).iter(ns + "host"):
            records.append(Record(i.attrib))
        return records

    def __str__(self):
        return super().__str__() + "&Command={}".format(self._command)


class SetHosts(DomainsDNS):
    """
    Namecheap API: domains.dns.setHosts [https://www.namecheap.com/support/api/methods/domains-dns/set-hosts.aspx]
    """

    def __init__(self):
        super().__init__()
        self._command = "namecheap.domains.dns.setHosts"
        self._records = []

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
        cnt = 1
        for i in self._records:
            i.index, cnt = cnt, cnt + 1
            res += str(i)
        return res


def get_set_hosts():
    set_hosts = SetHosts()
    for record in GetHosts().get_records():
        set_hosts.add_record(record)
    return set_hosts


def set_challenge_record():
    hosts = get_set_hosts()
    # Allow host to append any next level values
    Name = hosts.format_record_name("_acme-challenge")
    # This will cause multi-domain values to fail as they require multiple TXT records
    # hosts.remove_record(Name, "TXT")
    hosts.add_record(
        Record({
            "Name": Name,
            "Type": "TXT",
            "Address": os.environ["CERTBOT_VALIDATION"],
            "TTL": 60
        }))
    print(str(hosts))
    # hosts.post()


def remove_challenge_record():
    hosts = get_set_hosts()
    # Allow host to append any next level values
    Name = hosts.format_record_name("_acme-challenge")
    hosts.remove_record(Name, "TXT")
    hosts.post()
