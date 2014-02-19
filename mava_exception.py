class MavaException(Exception):
  def __init__(self, message):
    message = "Mava says: %s" % message
    super(MavaException, self).__init__(message)
