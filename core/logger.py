class Logger:
  def __init__(self, info_color="255;255;255", warn_color = "255;255;0", error_color = "255;0;0"):
    self.info_color = info_color
    self.warn_color = warn_color
    self.error_color = error_color
  def info(self, *argv):
    out = "\033[38;2;"+self.info_color+"m"
    for i in argv:
      out+=i
    out+="\033[0m"
    print(out)
  def warn(self, *argv):
    out = "\033[38;2;"+self.warn_color+"m"
    for i in argv:
      out+=i
    out+="\033[0m"
    print(out)
  def error(self, *argv):
    out = "\033[38;2;"+self.error_color+"m"
    for i in argv:
      out+=i
    out+="\033[0m"
    print(out)
