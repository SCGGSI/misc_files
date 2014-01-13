from items import *

class Class:
    def __init__(self, name, maxHP = 20, maxMP = 20, Strength = 1, Magic = 1, 
                 Inventory = [], gold = 0, Spells = []):
        self.name = name
        self.maxHP = maxHP
        self.maxMP = maxMP
        self.HP = self.maxHP
        self.MP = self.maxMP
        self.Strength = Strength
        self.Magic = Magic
        self.Inventory = Inventory
        self.gold = gold
        self.Spells = []
        self.equipped = Equipped() 
        self.bdy_parts = ['RH', 'LH', 'Hands', 'Body', 'Head', 'Legs', 'Feet'] 
        
    def attack(self, target, wpn):
        if wpn.name == 'Nothing':
            atk_dmg = self.Strength
        else:
            atk_dmg = self.Strength * wpn.dmg

        if atk_dmg >= target.HP:
            target.HP = 0
        else:
            target.HP -= atk_dmg

    def bdy_parts_menu(self):
        return [str(each + ' \t\t' + self.equipped.bdy_part_dict[each].name)
                for each in self.bdy_parts] 

    def add_to_inv(self, item):
        self.Inventory.append(item)
        
    def equip_item(self, item, body_part):
        if self.equipped.bdy_part_dict[body_part] == Nothing:
            self.equipped.bdy_part_dict[body_part] = item           
        else:
            self.add_to_inv(self.equipped.bdy_part_dict[body_part])
            self.equipped.bdy_part_dict[body_part] = item

        self.Inventory.remove(item)

    def print_inv(self):
        print '\t\tINVENTORY\t\t'
        print '-' * 40
        print '\nNUMBER\tNAME'
        print '-' * 40
        print
        
        for i, each in enumerate(self.Inventory):
            print i + 1, '\t', each.name

        print
            
    def print_equipped(self):
        print '\t\tEQUIPPED\t\t'
        print '-' * 40
        print '\nBODY PART\tNAME'
        print '-' * 40
        print
        menu = self.bdy_parts_menu()
        for each in menu:
            print each

        print
            
            
class Equipped:
    def __init__(self, RH = Nothing, LH = Nothing, Hands = Nothing, Body =
                 Plain_Shirt, Head = Nothing, Legs = Pants, Feet = Nothing):
        self.RH = RH
        self.LH = LH
        self.Hands = Hands
        self.Body = Body
        self.Head = Head
        self.Legs = Legs
        self.Feet = Feet    
        self.Feet = Feet    
        self.bdy_part_dict = {'RH' : self.RH,
                              'LH' : self.LH,
                              'Hands' : self.Hands,
                              'Body' : self.Body,
                              'Head' : self.Head,
                              'Legs' : self.Legs,
                              'Feet' : self.Feet}
        
