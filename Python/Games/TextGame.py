from items import *
from NPCs import *
import math

PROMPT = '>>> '
        
def Create_Character():
    Name = raw_input('What is your name?\n' + PROMPT)

    print "Hello %s.\n" % (Name)
    
    return Name

def battle(target, source, battle_type = 'Random'):
    print "\nA wild %s appeared." %target.name
    print "What do you do?\n"    
    
    actions = ['Attack with Right Hand', 'Attack with Left Hand', 'Do Nothing']
    
    while target.HP > 0:
        
        # Fix the logic of User losing.
        if source.HP <= 0:
            print '%s defeated you! :( You lose :(' % target.name
            break        
        
        print '\t\tBATTLE MENU'
        print '-' * 40
        print '\nCurrent HP: %s\t%s HP: %s' % (source.HP, target.name,
                                               target.HP)
        print
            
        action = menu_choice(actions)
    
        if 'Attack' in action:
            if 'Right' in action:
                RL = 'RH'
            else:
                RL = 'LH'

            print source.equipped.bdy_part_dict[RL].name
            
            print 'You attack the %s with your %s.' \
                  % (target.name, source.equipped.bdy_part_dict[RL].name)
            source.attack(target, source.equipped.bdy_part_dict[RL])
        
            print '%s now has %s HP.' % (target.name, target.HP)
            
        elif action == 'Do Nothing':
            print "You do nothing for a turn."
        
        if target.HP > 0:
            # Check HP percent to decide on healing
            HP_percent = target.HP / target.maxHP

            if HP_percent <= 0.25:
                # determine if there are potions in inventory
                pass
            
            print '\n%s attacks.\n\n' % target.name
            target.attack(source, claws)
            
    print "You defeated the %s and won %s gold.\n" % (target.name, target.gold)
    
    source.gold += target.gold

    print "-" * 40
    print "\nBATTLE OVER.\n"
    print "-" * 40
    print "\n\n"
    
            
def menu_choice(menu_list):
    for i, each in enumerate(menu_list):
        print i + 1, each
        
    action_not_ok = True

    while action_not_ok:
        print
        try:
            action_num = int(raw_input(PROMPT))

            if action_num in range(1, len(menu_list) + 1):
                action_not_ok = False
            else:
                print "\nPlease enter a number between 1 and %s" % len(menu_list)

        except:
            print "\nPlease enter a number between 1 and %s" % len(menu_list)        
        
    return menu_list[action_num - 1]

def main_screen(source, message, menu = []):
    print '\n' * 40
    print 'HP: %s/%s\tMP: %s/%s\tGold: %s' \
          % (source.HP, source.maxHP, source.MP, source.maxMP, source.gold)
    print '-' * 40
    print '\n\n\n'

    message_length = int(math.ceil(len(message) / 80))
    menu_length = len(menu)

    print message

    if len(menu):
        print '\n' * int(26 - (message_length + menu_length))
        print '\t\tMENU'
        print '-' * 40
        print
        action = menu_choice(menu)

    else:
        print '\n' * int(28 - message_length)
        action = raw_input('Press ENTER to continue.\n\n' + PROMPT)

    return action
    
def main():

    try:
        import sys
        import os
        
        if 'idlelib.run' in sys.modules:
            print "You are running this program in IDLE. Please run it in the",
            print "console for the best experience.\n\n"

        else:
            os.system("mode con cols=80 lines=40")
        
    except:
        pass
    
    User = Class(Create_Character())
    
    User.add_to_inv(knife)

    User.equip_item(knife, 'RH')
    Caterpie = Class("Caterpie", gold = 3)

    main_screen(User, 'You wake up in a dark cave.')

    main_screen(User, 'Choose your action by entering the corresponding '
                'number of an action in a list')

    action = main_screen(User,
                         'Open your inventory, or view your equipped items.',
                         ['Open Inventory', 'View Equipped'])                

    
    # battle(Caterpie, User)

if __name__ == "__main__":
    main()
