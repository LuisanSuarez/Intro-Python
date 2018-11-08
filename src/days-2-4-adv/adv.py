from room import Room
from player import Player
from item import Treasure, Item
import textwrap

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player(room['outside'])
stop = False

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

# Rooms are initiliazed with no items. To add them, use the
# Room.add_items(*items) method. You may pass in a  list,
# individual items, or a combination of both
# e.g. Room.add_items('sword', 'shield', ['treasure, 'crown', 'chalice'])

# room['outside'].add_items('rocks', ['skull', 'abandoned armor'])

chest = Treasure('Treasure Chest - [chest]' , """An old pirate relic, overflowing with 
    bullions and gems""", 'chest')
ring = Treasure("Princess Fiora's Ring - [ring]", """A ring granting the wearer god-like beauty and charm,
    but removing the ability to love""", 'ring' )
crown = Treasure("King Arthur's Crown - [crown]", """Rumored among mystics and trobadours to grant
the wearer the ability to read the minds of others""", 'crown')
grail = Treasure('Holy Grail - [grail]', """The enchanted chalice of life. It looks benign 
    now, but perhaps in the proper hands...""", 'grail')

room['treasure'].add_items(chest, grail)
room['narrow'].add_items(ring)
room['overlook'].add_items(crown)



allowed_moves = ['n', 'e', 's', 'w', 'q', 'i', 'items', 'inventory', 'quit', 'score']

def action(phrase):
    verb = phrase[0]
    noun = phrase[1]
    if verb in ['get', 'take', 'lift', 'grab', ]:
        for item in player.room.item_list:
            if item.value == noun:
                player.room.remove_items(item)
                player.add_items(item)
                item.on_take()
                print ('This ran')
                print (f'Thou hath picked up one {item}')
            else:
                print ('The item thou look for is not here')
    elif verb in ['drop', 'leave', 'forget', 'dump', 'discard', 'abandon' ]:
        print ('is this running? yes')
        for item in player.item_list:
            if item.value == noun:
                player.remove_items(item)
                player.room.add_items(item)
                print (f'Thou hath dropped thy {item}')
            else:
                print ('Thou hath not the item thou speak of')
    else:
        print ('I understand not thy command. Please choose another one')


def single(move):
    move = move[0]   
    if move in allowed_moves:
        if move == 'n':
            try:
                player.room = player.room.n_to
                print ('Thou attemps to move north-ward')
            except AttributeError:
                print('You may not move in that direction. Try again')
        elif move == 'e':
            try:
                player.room = player.room.e_to
                print ('Thou attemps to move east-ward')
            except AttributeError:
                print('You may not move in that direction. Try again')
        elif move == 's':
            try:
                print ('Thou attemps to move south-ward')
                player.room = player.room.s_to
            except AttributeError:
                print('You may not move in that direction. Try again')
        elif move == 'w':
            try:
                print ('Thou attemps to move west-ward')
                player.room = player.room.w_to
            except AttributeError:
                print('You may not move in that direction. Try again')
        elif move in ['inventory', 'i', 'items']:
            print ('~ ~ Thy current inventory ~ ~')
            if player.item_list:
                for item in player.item_list:
                    print (item)
            else:
                print ('Thou hath nothing')
            # print (player.item_list if player.item_list else 'Thou hath nothing')
        elif move == 'score':
            print ('~ ~ Thy current score ~ ~')
            print (player.score)
        elif move == 'q' or move == 'quit':
            print ('Farewell, you coward')
            global stop
            stop = True
    else:
        print ('Please enter a cardinal direction or "q" to quit')

print ('before we start')
print (player.room)
print (player.room.item_list)
print ('NOW WE START')
while stop == False:
    print (' ')
    print ('Thy current location:', player.room)
    print ( textwrap.wrap(player.room.description) )
    print ('~ ~ Items found in this room ~ ~')
    if player.room.item_list:
        for item in player.room.item_list:
            print (item)
    else:
        print ('  Nothing to see here...  ')
    # print ( print item.name for item in player.room.item_list)
    command = input('What shall thou do next?     ')
    print ()
    try:
       command = command.lower()
    except AttributeError:
        print ('Please enter an english instruction')
        continue
    command = command.split()
    if len(command) == 1:
        single(command)
    elif len(command) == 2:
        action(command)
    else:
        print ('Thy hath not been understood. Tryeth again')


