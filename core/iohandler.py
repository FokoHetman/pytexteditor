class IOHandler:
  def __init__(self):
    pass
  def eval(self, command, program):
    match command:
      case "q":
        self.quit(program)
      case "w":
        self.savefile(program)
      case "wq":
        self.savefile(program)
        self.quit(program)
  def savefile(self, program):
    with open(program.filename, "w") as f:
      f.write(''.join(program.lines))
  def quit(self, program):
    program.clear_screen()
    import sys
    sys.exit(0)
