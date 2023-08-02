#!/usr/bin/python3
"""
This program displays random jokes
"""

Funjokes = [
        "Why was 6 afraid of 7?\n\t> Because 7 ate 9.",
        "Why can't you trust atoms?\n\t> Because they make up everything.",
        "Why won’t it hurt if you hit your friend with a 2-liter of soda?\n\t> Because it’s a soft drink!",
        "Why did the mushrooms get invited to all the best parties?\n\t> He was a fun-gi!",
        "Why do you smear peanut butter on the road?\n\t> To go with the traffic jam.",
        "What gets more wet the more it dries?\n\t> A towel!",
        "Hear about the new restaurant called Karma?\n\t> There’s no menu: You get what you deserve.",
        "What do pampered cows produce?\n\t> Spoiled milk.",
        "What does a house wear?\n\t> Address!",
]

from random import randint

print( jokes[randint(0, len(jokes) - 1)] )
