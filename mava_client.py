import json
from mava_exception import MavaException
import requests
import mava_actions

class MavaClient(object):
  def __init__(self, config):
    if len(config) > 0:
      self.__dict__ = dict(config)
      self.authenticate()
      print "Mava is happy"
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
    try:
      resp = requests.post("%stokens" % self.auth_url,
          data=json.dumps(data), headers=headers)
      if resp.status_code == 200:
        self.parse_content(resp.json())
      else:
        raise Exception("Authentication failed!!")
    except Exception, ex:
      raise MavaException(ex.message)


  def parse_content(self, content):
    self.__dict__["auth_token"] = content["access"]["token"]["id"]
    services = content["access"]["serviceCatalog"]
    service_dict = {"server_url": service["endpoints"][0]["publicURL"]\
        for service in services if service["name"] == "cloudServers"}
    self.__dict__["server_url"] = service_dict["server_url"]

  def execute(self, *args):
    action_ = "Action%s" % args[0].capitalize()
    action_args = args[1:]
    try:
      getattr(mava_actions, action_)(*action_args, **self.__dict__)
    except Exception, ex:
      raise  MavaException("Something went wrong with this action.\n%s" % ex.message)
