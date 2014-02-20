#!/usr/bin/env python
import ConfigParser
import sys
from optparse import OptionParser
from os.path import expanduser
from mava_client import MavaClient
from mava_exception import MavaException

class MyOptionParser(OptionParser):
      def error(self, msg):
                pass

file = "%s/.supermava" % expanduser('~')
config = []

def validate_env(env, file=file):
  Config =  ConfigParser.ConfigParser()
  Config.read(file)
  try:
    global config
    config = Config.items(env)
  except:
    message = ("I do not know any environment called %s.\nTry supermava -l") % env
    raise MavaException(message)

def validate(p, args):
  try:
    if len(args) < 2:
      p.print_help()
      raise MavaException("Invalid number of arguments")
    validate_env(args[0])
  except MavaException, ex:
    print ex.message
    exit(-1)

def list():
  Config = ConfigParser.ConfigParser()
  Config.read(file)
  sections = Config.sections()
  print "Environments found in config:"
  for section in sections:
    print section

def honor_options(options):
  for key in vars(options).iterkeys():
    if vars(options)[key]:
      getattr(sys.modules[__name__], key)() 
      exit()

def main():
  p = MyOptionParser(description='First Gen CS-API client',
                                         prog='supermava',
                                         version='supermava 0.1',
                                         usage='%prog environment action')
  p.add_option('-l', '--list', action="store_true",\
      help="Lists valid environments in supermava config",\
      default=False)
  p.add_option('-a', '--actions', action="store_true",\
      help="Lists all possible actions", default=False)
  options, arguments = p.parse_args()
  honor_options(options)

  validate(p, arguments)
 
  action = arguments[1:]
  try:
    mavaClient = MavaClient(config)
    mavaClient.execute(*action)
    exit()
  except MavaException, ex:
    print ex.message

if __name__ == "__main__":
  main()
