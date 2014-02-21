import json

class MavaTemplate(object):
  def list(self, result):
    max_id = max([str(server['id']) for server in result['servers']], key=len) 
    max_id_length = len(max_id) if len(max_id) > 2 else 2
    max_name = max([server['name'] for server in result['servers']], key=len)
    max_name_length = len(max_name) if len(max_name) > 4 else 4
    print ("+-" + "-" * max_id_length + "-+-" + "-" * max_name_length + "-+")
    print ("| Id " + " " * (max_id_length-2) + "| Name " + " " * (max_name_length-5) + " |")
    print ("+-" + "-" * max_id_length + "-+-" + "-" * max_name_length + "-+")
    for server in result['servers']:
      print ("| %s" % server['id'] + " " * (max_id_length - len(str(server['id']))) + " | " + server['name'] + " " * (max_name_length - len(server['name'])) + " |")
    print ("+-" + "-" * max_id_length + "-+-" + "-" * max_name_length + "-+")

