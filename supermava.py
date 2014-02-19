#!/usr/bin/env python
import ConfigParser
import optparse
from os.path import expanduser
from mava_client import MavaClient
from mava_exception import MavaException

file = "%s/.supermava" % expanduser('~')
config = []

def run(client, action):
  try:
    result = getattr(client, action[0])(*action[1:])
    print result
  except MavaException, ex:
    print ex.message

def validate_env(env, file=file):
  Config =  ConfigParser.ConfigParser()
  Config.read(file)
  try:
    global config
    config = Config.items(env)
  except:
    message = ("I do not know any environment called %s.\nTry supermava -l") % env
    raise MavaException(message)

def validate_action(action):
  try: 
    getattr(MavaClient, action)
  except:
    message = "I do not know any action called %s.\nTry: supermava -a" % action
    raise MavaException(message) 

def validate(p, args):
  if len(args) < 2:
    p.print_help()
    raise MavaException("Invalid number of arguments")
  validate_env(args[0])
  validate_action(args[1])

def list_env():
  Config = ConfigParser.ConfigParser()
  Config.read(file)
  sections = Config.sections()
  print "Environments found in config:"
  for section in sections:
    print section

def main():
  p = optparse.OptionParser(description='First Gen CS-API client',
                                         prog='supermava',
                                         version='supermava 0.1',
                                         usage='%prog environment action')
  p.add_option('-l', '--list', action="store_true",\
      help="Lists valid environments in supermava config",\
      default=False)
  p.add_option('-a', '--actions', action="store_true",\
      help="Lists all possible actions", default=False)
  options, arguments = p.parse_args()
  if options.list:
    list_env()
    exit()
  if options.actions:
    list_actions()
    exit()

  try:
    validate(p, arguments)
  except MavaException, ex:
    print ex.message
    exit()
  action = arguments[1:]
  mavaClient = MavaClient(config)
  run(mavaClient, action)
  exit()

if __name__ == "__main__":
  main()
