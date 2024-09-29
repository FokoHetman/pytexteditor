import sys, os
import core.getch
import core.logger
import core.iohandler

ioh = core.iohandler.IOHandler()
logger = core.logger.Logger()
getch = core.getch._Getch()

back = chr(8)
modes = {"control": 0, "command": 1, "input": 2}

class Program:
  def __init__(self):
    self.cursorpos = (1,1)
    self.lines = []
    self.io = ""
    self.filename = ""
    self.mode = modes["control"]
    self.display = ""
  def read_file(self, filename):
    self.filename = filename
    with open(filename, "r") as f:
      self.lines = f.readlines()
  def write_file(self, filename):
    with open(filename, "w") as f:
      f.write(''.join(self.lines))
  def clear_screen(self):
    print("\033[2J")
  def update_cursor(self):
    text = "\033[H" + "\033["+str(self.cursorpos[1])+";"+str(self.cursorpos[0])+"H"
    match self.mode:
      case 0:
        text += "\033[?16;0;0;c"
      case _:
        text += "\033[?5;0;0;c"
    print(text, end="", flush=True)
    #print(f"\033[{str(self.cursorpos[0])}G")
  def render_text(self):
    termsize = os.get_terminal_size()
    self.display = "\033[48;2;97;97;97m"+ self.filename + (termsize.columns-len(self.filename))*" " + "\033[0m";
    for i in self.lines:
      self.display+=i
    for i in range(termsize.lines - len(self.display.split("\n"))-2):
      self.display += "\n"
    self.display += "\033[48;2;160;0;120m" + self.io + (termsize.columns-len(self.io)-1)*" " + str(self.mode) + "\033[0m";
    print("\033[2J\033[H" + self.display)


  def move_cursor(self, vec):
    self.cursorpos = (self.cursorpos[0] + vec[0], self.cursorpos[1] + vec[1])
    if self.cursorpos[1]<1:
      self.cursorpos = (self.cursorpos[0], 1)
    elif self.cursorpos[1]>len(self.lines):
      self.cursorpos = (self.cursorpos[0], len(self.lines))

    if self.cursorpos[0]<1:
      self.cursorpos = (1, self.cursorpos[1])
    elif self.cursorpos[0]>len(self.lines[self.cursorpos[1]-2]):
      self.cursorpos = (len(self.lines[self.cursorpos[1]-2]), self.cursorpos[1])
    return self.cursorpos

  def type_text(self, text):
    match text:
      case "":
        if self.cursorpos[0]>1:
          self.lines[self.cursorpos[1]-2] = self.lines[self.cursorpos[1]-2][:self.cursorpos[0]-2] + self.lines[self.cursorpos[1]-2][self.cursorpos[0]-1:]
          self.move_cursor((-1,0))
        else:
          pre_lines = self.lines[:self.cursorpos[1]-3]
          ln = len(self.lines[self.cursorpos[1]-3][:-1])
          pre_lines.append(self.lines[self.cursorpos[1]-3][:-1] + self.lines[self.cursorpos[1]-2])
          pre_lines += self.lines[self.cursorpos[1]-1:]
          self.lines = pre_lines
          self.move_cursor((ln,-1))


      case "\n":
        pre_lines = self.lines[:self.cursorpos[1]-2]
        pre_lines.append(self.lines[self.cursorpos[1]-2][:self.cursorpos[0]-1]+"\n")
        post_lines = [self.lines[self.cursorpos[1]-2][self.cursorpos[0]-1:]]
        post_lines += self.lines[self.cursorpos[1]-1:]
        self.lines = pre_lines
        #self.lines.append("\n")
        self.lines+=post_lines
        self.move_cursor((-9999,1))
      case _:
        self.lines[self.cursorpos[1]-2] = self.lines[self.cursorpos[1]-2][:self.cursorpos[0]-1] + text + self.lines[self.cursorpos[1]-2][self.cursorpos[0]-1:]
        self.move_cursor((len(text),0))


if len(sys.argv)>1:
  program = Program()
  for i in sys.argv[1::]:
    program.read_file(i)
    while True:
      program.clear_screen()
      program.render_text()
      #print(program.cursorpos)
      #print("\033[H")
      program.update_cursor()
      ch = getch()
      match ch:
        case '\r':
          match program.mode:
            case 2:
              program.type_text('\n')
            case 1:
              ioh.eval(program.io[1::], program)
              program.io = ""
        case '\033':
          program.io = "Click [ESC] twice to leave Input/Command mode."
          ch = getch()
          match ch:
            case '[':
              program.io = ""
              match getch():
                case 'A':
                  program.move_cursor((0,-1))
                case 'B':
                  program.move_cursor((0,1))
                case 'C':
                  program.move_cursor((1,0))
                case 'D':
                  program.move_cursor((-1,0))
                case _:
                  logger.warn("Runtime Leak")
            case _:
              match program.mode:
                case 0:
                  pass
                case _:
                  program.mode = modes["control"]
        case ':':
          match program.mode:
            case 0:
              program.mode = modes["command"]
              program.io = ":"
            case 1:
              program.io += ":"
            case 2:
              program.type_text(":")
        case 'i':
          match program.mode:
            case 0:
              program.mode = modes["input"]
            case 1:
              program.io += "i"
            case 2:
              program.type_text("i")
        #case '':
        #  match program.mode:
        #    case 1:
        #      program.io = program.io[:-1]
        #    case 2:
        #      program.type_text("SPECIALKEY_BACKSPACE")
        case _:
          match program.mode:
            case 0:
              program.io = "You're in Control mode! use `i` to enter into Input mode or `:` to enter Command mode." + ch
            case 1:
              program.io += ch
            case 2:
              program.type_text(ch)



else:
  logger.warn("Invalid usage, displaying help page.")
  logger.info("USAGE:\npython main.py [file]")
