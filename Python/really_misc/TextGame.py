PROMPT = '>>> '

class Class:
    def __init__(self, name):
        self.maxHP = 20
        self.maxMP = 20
        self.HP = self.maxHP
        self.MP = self.maxMP
        self.Strength = 1
        self.Magic = 1
        self.Inventory = []
        self.Gold = 0
        self.Spells = []
        self.name = name
        
    def attack(self, target, wpn_type, wpn):
        atk_dmg = self.Strength * wpn.dmg
        if atk_dmg >= target.HP:
            target.HP = 0
        else:
            target.HP -= atk_dmg

    def add_to_inv(self, item):
        self.Inventory.append(item)

    def print_inv(self):
        print '\t\tINVENTORY\t\t'
        print '-' * 40
        print '\nNUMBER\tNAME'
        print '-' * 40
        print
        
        for i, each in enumerate(self.Inventory):
            print i + 1, '\t', each.name


class Item:
    def __init__(self):
        self.weight = 1
        self.value = 1


class Knife(Item):
    def __init__(self):
        self.value = 5
        self.dmg = 2
        self.name = 'Knife'

        
def Create_Character():
    Classes = ["Wizard", "Knight", "Rogue"]
    ClassNotOk = True

    print "Please select your class."
    
    while ClassNotOk:
        for i, each in enumerate(Classes):
            print i + 1, each

        User_Class_Num = raw_input(PROMPT)

        if User_Class_Num == '1':
            User_Class = 'Wizard'
            ClassNotOk = False
        elif User_Class_Num == '2':
            User_Class = 'Knight'
            ClassNotOk = False
        elif User_Class_Num =='3':
            User_Class = 'Rogue'
            ClassNotOk = False
        else:
            print "You must enter a 1, 2, or 3.\n\n"
            ClassNotOk = True

    print "You have selected a %s." % User_Class
    Name = raw_input('What is your name?\n' + PROMPT)

    print "%s the %s.\n\nAnd so the journey begins...\n" % (Name, User_Class)

def battle(target, battle_type = 'Random'):
    print "\nA wild %s appeared." %target.name
    print "What do you do?\n"    
    
    actions = ['Attack', 'Do Nothing']

    print "\t\tBATTLE MENU\n"
    print '-' * 40
    
    for i, each in enumerate(actions):
        print i + 1, each

    action_not_ok = True

    while action_not_ok:
        action_num = raw_input(PROMPT)

def main():
    Create_Character()

    User = Class("User")
    knife = Knife()
    
    print "You have %s HP" % User.HP
    print "Here's a knife."

    User.add_to_inv(knife)

    print "Here's what you have."

    User.print_inv()

    Caterpie = Class("Caterpie")

    action = actions[int(raw_input(PROMPT)) - 1]

    if action == 'Attack':
        print "You attack the caterpie."
        User.attack(Caterpie, 'Strength', knife)

        print "Caterpie has %s HP now." % Caterpie.HP
        
    else:
        print "You did nothing."

if __name__ == "__main__":
    main()
