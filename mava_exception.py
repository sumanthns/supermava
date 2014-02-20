class MavaException(Exception):
  def __init__(self, message):
    message = "\nMava says:\n %s" % message
    super(MavaException, self).__init__(message)
