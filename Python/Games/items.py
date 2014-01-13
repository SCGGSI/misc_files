class Item:
    def __init__(self, name = 'item'):
        self.weight = 1
        self.value = 1
        self.name = name
        
        
class Weapon(Item):
    def __init__(self, wpn_type, name = 'item', dmg = 1, eqp = 1):
        self.name = name
        self.wpn_type = wpn_type
        self.dmg = dmg
        self.eqp = 1
        
        
class Clothing(Item):
    def __init__(self, name = 'item', clth_type = 'Cloth', bdy_prt = 'Body'):
        self.name = name
        self.clth_type = clth_type
        self.bdy_prt = bdy_prt
        
        
class Knife(Item):
    def __init__(self):
        self.value = 5
        self.dmg = 2
        self.name = 'Knife'
        
        
class Claws(Item):
    def __init__(self):
        self.dmg = 1
        self.name = 'Claws'

    
knife = Knife()
claws = Claws()

Plain_Shirt = Clothing(name = 'Plain Shirt')
Pants = Clothing(name = 'Pants', bdy_prt = 'Legs')
Old_Shoes = Clothing(name = 'Shoes', bdy_prt = 'Feet')
Nothing = Item(name = 'Nothing')
