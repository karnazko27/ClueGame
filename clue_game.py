#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# clue_game.py - simulation of boardgame Clue

import collections

Clue = collections.namedtuple('Clue',
                ['suspect', 'weapon', 'room'])


class MurderEnvelope:
    def __init__(self):
        self._clues = [Clue(suspect, weapon,
                            room) for suspect in suspects
                       for weapon in weapons
                       for room in rooms]

    def __len__(self):
        return len(self._clues)

    def __getitem__(self, position):
        return self._clues[position]


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.objects = []
        self.connected_rooms = {}

    def add_object(self, obj):
        self.objects.append(obj)

    def add_connection(self, direction, room):
        self.connected_rooms[direction] = room


class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.clue = None

    def set_clue(self, clue):
        self.clue = clue


class Player:
    def __init__(self, current_room):
        self.current_room = current_room
        self.inventory = []

    def move(self, direction):
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print("You have moved to the", self.current_room.name)
            self.look_around()
        else:
            print("You can't go that way!")

    def look_around(self):
        print(self.current_room.description)
        if self.current_room.objects:
            print("You see the following objects:")
            for obj in self.current_room.objects:
                print(obj.name)

    def take_object(self, object_name):
        for obj in self.current_room.objects:
            if obj.name.lower() == object_name.lower():
                self.inventory.append(obj)
                self.current_room.objects.remove(obj)
                print("You have taken the", obj.name)
                return
        print("There is no such object here.")

    def use_object(self, object_name):
        for obj in self.inventory:
            if obj.name.lower() == object_name.lower():
                if obj.clue:
                    print(obj.clue)
                else:
                    print("You can't find any clues from this object.")
                return
        print("You don't have that object in your inventory.")

# define suspects, weapons, and rooms
suspects = ['Plum', 'White', 'Scarlet', 'Green', 'Mustard',
            'Peacock']
weapons = ['Rope', 'Dagger', 'Wrench', 'Pistol', 'Candlestick',
           'Lead Pipe']
rooms = ['Courtyard', 'Game Room', 'Study', 'Dining Room',
         'Garage', 'Living Room', 'Kitchen', 'Bedroom',
         'Bathroom']

# Create murder envelope
murder_envelope = MurderEnvelope(suspects, weapons, rooms)

# Get first clue from the envelope
mystery_clue = murder_envelope[0]

# Create rooms
living_room = Room("Living Room", "You are in the cozy living room.")
kitchen = Room("Kitchen", "You are in the messy kitchen.")
bedroom = Room("Bedroom", "You are in the dimly lit bedroom.")

# Create objects
note = Object("Note", "A handwritten note with mysterious symbols.")
key = Object("Key", "A rusty key that seems important.")
candle = Object("Candle", "A partially burnt candle.")

note.set_clue("The key to the mystery is hidden under the old rug.")
key.set_clue("The door to the secret room can be unlocked with this key.")

# Add objects to rooms
living_room.add_object(note)
kitchen.add_object(key)
bedroom.add_object(candle)

# Connect rooms
living_room.add_connection("east", kitchen)
kitchen.add_connection("west", living_room)
kitchen.add_connection("north", bedroom)
bedroom.add_connection("south", kitchen)

if __name__ == '__main__':
    # Create player and start the game
    player = Player(living_room)

    print("Welcome to the Clue Game!")
    player.look_around()

    # Game loop
    while True:

        print(
            "Available commands: move <direction>, look, take <object>, use <object>, solve mystery <suspect> <weapon> <room>, quit")
        command = input("Enter a command: ").split()
        print("Suspects: ", suspects)
        print("Weapons: ", weapons)
        print("Rooms: ", rooms)
        print("Type 'quit' to quit anytime")

        if not command:
            continue

        if command[0] == "move":
            if len(command) >= 2:
                player.move(command[1])
            else:
                print("Please provide a valid direction.")
        elif command[0] == "look":
            player.look_around()
        elif command[0] == "take":
            if len(command) >= 2:
                player.take_object(command[1])
            else:
                print("Please provide an object name.")
        elif command[0] == "use":
            if len(command) >= 2:
                player.use_object(command[1])
            else:
                print("Please provide an object name.")
        elif command[0] == "solve":
            if len(command) >= 5:
                if command[1] == "mystery":
                    if command[2] in suspects and command[3] in weapons and command[4] in rooms:
                        if command[2] == mystery_clue.suspect and command[3] == mystery_clue.weapon and command[
                            4] == mystery_clue.room:
                            print("Congratulations! You've solved the mystery!")
                        else:
                            print("That's not the correct solution. Keep investigating!")
                    else:
                        print("Please select valid options for suspect, weapon, and room.")
            else:
                print("Please provide a suspect, weapon, and room for your guess.")
        elif command[0] == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Invalid command. Try again.")

