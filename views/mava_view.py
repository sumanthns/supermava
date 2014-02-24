import json
from quik import FileLoader
import os

class MavaView(object):
  def __init__(self):
    dir_ = os.path.dirname(__file__)
    self.filename = os.path.join(dir_, "../templates")

class SliceView(MavaView):
  def __init__(self):
    super(SliceView, self).__init__()
    self.filename = "%s/slice" % self.filename
    self.loader = FileLoader(self.filename)

  def list(self, result):
    template = self.loader.load_template('list.txt')
    print template.render(result, loader=self.loader).encode('utf-8')

  def show(self, result):
    template = self.loader.load_template('show.txt')
    print template.render(result, loader=self.loader).encode('utf-8')

