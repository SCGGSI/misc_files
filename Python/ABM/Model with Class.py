import numpy as np

class Person:
    def __init__(self, index):
        self.Random = np.random.rand()
        if self.Random <= 0.05:
            self.Health = "Sick"
        else:
            self.Health = "Well"

        if self.Health == "Sick":
            self.DaysSick = 0
        else:
            self.DaysSick = -1

        if self.Random < 0.25:
            self.Location = 1
        elif self.Random < 0.5:
            self.Location = 2
        elif self.Random < 0.75:
            self.Location = 3
        else:
            self.Location = 4

        self.index = index

    def Update(self):
        if self.Health == "Sick":
            self.DaysSick += 1

        if self.DaysSick >= 4:
            self.DaysSick = -1
            self.Health = "Well"


class Location:
    def __init__(self, categ = "House", autoplace = True):
        if "ret" in categ:
            self.categ = "Retail"
        elif "bus" in categ:
            self.categ = "Business"
        elif "pub" in categ:
            self.categ = "Public"
        else:
            self.categ = "House"

        self.adj = []
        self.inside = []

        if self.categ == "House":
            self.open = 0
            self.close = 24
        elif self.categ == "Public":
            self.open = 7
            self.close = 8
        elif self.categ == "Business":
            self.open = 9
            self.close = 5
        else:
            self.open = 10
            self.close = 9

        if autoplace:
            self.Place()

    def Nearby(self):
        pass

    def Place(self):
        pass

    def IsOpen(self):
        if self.open <= Time <= self.close:
            return True
        else:
            return False

    def PlaceInside(self, ind):
        self.inside.append(ind)

def CreateHouseHold():
    size = np.random.randint(1, 6)

    index = len(People)

    for i in range(1, size + 1):
        

People = [Person(x) for x in range(0, 100)]
Time = 9
