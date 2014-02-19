import json
from mava_exception import MavaException
import requests

class MavaClient(object):
  def __init__(self, config):
    if len(config) > 0:
      print "Mava is happy"
      self.__dict__ = dict(config)
      self.authenticate()
    else:
      raise MavaException("Invalid arguments")

  def authenticate(self):
    data = {
        "auth": {
          "passwordCredentials":
            {
              "username": self.username,
              "password": self.password
             }
          }
    }
    headers = {
        "Content-Type": "application/json"
        }
    resp = requests.post("%stokens" % self.auth_url,
        data=json.dumps(data), headers=headers)
    if resp.status_code == 200:
      self.parse_content(resp.json())
    else:
      raise MavaException("Authentication failed!!")


  def parse_content(self, content):
    self.__dict__["auth_token"] = content["access"]["token"]["id"]
    services = content["access"]["serviceCatalog"]
    service_dict = {"server_url": service["endpoints"][0]["publicURL"]\
        for service in services if service["name"] == "cloudServers"}
    self.__dict__["server_url"] = service_dict["server_url"]

  def list(self):
    headers = {
        "X-Auth-Token": self.auth_token
        }
    try:
      resp = requests.get("%s/servers" % self.server_url,\
          headers=headers, verify=False)
      if resp.status_code == 200:
        return resp.json()
      else:
        raise MavaException("Servers list failed!!")
    except Exception, ex:
      raise MavaException(ex.message)

  def show(self, *args):
    if not len(args) == 1:
      raise MavaException("Gimme one server at a time")
    headers = {
        "X-Auth-Token": self.auth_token
        }
    try:
      resp = requests.get("%s/servers/%s" % (self.server_url, args[0]),\
          headers=headers, verify=False)
      if resp.status_code == 200:
        return resp.json()
      else:
        raise MavaException("Server Show failed.\nErrorCode=%s\nContent=%s"\
            % (str(resp.status_code), resp.text))
    except Exception, ex:
      raise MavaException(ex.message)


