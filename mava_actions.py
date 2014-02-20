import json
from mava_exception import MavaException
import requests

class MavaAction(object):
  def __init__(self, *args, **kwargs):
    self.validate(*args)
    self.execute(*args, **kwargs)

class ActionList(MavaAction):
  def validate(self, *args):
    if not len(args) == 0:
      raise Exception("List should not contain any args.\nsupermava <env> list")

  def execute(self, *args, **kwargs):
    headers = {
        'X-Auth-Token': kwargs['auth_token']
        }
    try:
      resp = requests.get("%s/servers" % kwargs["server_url"],\
          headers=headers, verify=False)
      if resp.status_code == 200:
        print resp.json()
      else:
        raise Exception("Servers list Failed!!\nError: %s\nContent: %s"\
            % (str(resp.status_code), resp.text))
    except Exception, ex:
      raise ex 


class ActionShow(MavaAction):
  def validate(self, *args):
    if not len(args) == 1:
      raise Exception("Gimme one server at a time.\nsupermava <env> show <slice_id>")

  def execute(self, *args, **kwargs):
    headers = {
        "X-Auth-Token": kwargs['auth_token']
        }
    try:
      resp = requests.get("%s/servers/%s" % (kwargs['server_url'], args[0]),\
          headers=headers, verify=False)
      if resp.status_code == 200:
        print resp.json()
      else:
        raise Exception("Server Show failed.\nErrorCode=%s\nContent=%s"\
            % (str(resp.status_code), resp.text))
    except Exception, ex:
      raise ex 
