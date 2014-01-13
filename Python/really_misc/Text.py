import os
import msvcrt

class Frog:
    X = 0
    Y = 0

    def __init__(self, x, y):
            self.X = x
            self.Y = y

    def Draw(self):
            for y in range(self.Y):
                    print ""
            print ' ' * self.X + '#'



    def Update(self):
            if msvcrt.kbhit() == True:
                    if msvcrt.getch() == 'a':
                            if self.X > 0:
                                    self.X = self.X - 1
                    if msvcrt.getch() == 'd':
                                    self.X = self.X + 1
                    if msvcrt.getch() == 'w':
                                    self.Y = self.Y - 1
                    if msvcrt.getch() == 's':
                                    self.Y = self.Y + 1






frog = Frog(0,0)


def Draw():
    os.system('cls')
    frog.Draw()

def Loop():
    while 1:      
        frog.Update()
        Draw()

Loop()
