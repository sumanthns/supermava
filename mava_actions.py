import json
from mava_exception import MavaException
import requests
import random
from templates.mava_template import MavaTemplate

class MavaAction(object):
  def __init__(self, *args, **kwargs):
    self.validate(*args)
    self.execute(*args, **kwargs)

class ActionList(MavaAction):
  def validate(self, *args):
    if not len(args) == 0:
      raise Exception("List should not contain any args.\nHelp:supermava <env> list")

  def execute(self, *args, **kwargs):
    headers = {
        'X-Auth-Token': kwargs['auth_token']
        }
    try:
      resp = requests.get("%s/servers" % kwargs["server_url"],\
          headers=headers, verify=False)
      if resp.status_code == 200:
        MavaTemplate().list(resp.json())
      else:
        raise Exception("Servers list Failed!!\nError: %s\nContent: %s"\
            % (str(resp.status_code), resp.text))
    except Exception, ex:
      raise ex 


class ActionShow(MavaAction):
  def validate(self, *args):
    if not len(args) == 1:
      raise Exception("Gimme one server at a time.\nHelp:supermava <env> show <slice_id>")

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

class ActionBoot(MavaAction):
  def validate(self, *args):
    if not len(args) == 2:
      raise Exception("Cant boot with given arguments.\nHelp:supermava <env> boot <image_id> <flavor_id>")

  def execute(self, *args, **kwargs):
    data = {
        "server":{
          "name": "test_%s" % (''.join(random.choice('abcde12345') for x in range(3))),
          "imageId": int(args[0]),
          "flavorId": int(args[1])
          }
        }
    headers = {
        "X-Auth-Token": kwargs['auth_token']
        }
    try:
      resp = requests.post("%s/servers" % kwargs['server_url'],\
          data=json.dumps(data), headers=headers, verify=False)
      if resp.status_code == 202:
        print resp.json()
      else:
        raise Exception("Server boot failed.\n ErrorCode=%s\nContent=%s"\
            % (str(resp.status_code), resp.text))
    except Exception, ex:
      raise ex
