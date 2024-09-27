import core.getch


getch = core.getch._Getch()
while True:
  getch()
  print("\033[2J\033[2;2H hello")

