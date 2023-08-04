#!/usr/bin/env python3
import speech_recognition as sr 
import pywhatkit



def run_voicemate():
    #Method to play music from youtube
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)

run_voicemate()
