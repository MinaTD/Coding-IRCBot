#!usr/bin/env python
from irc import *


class Bot(Irc):

        def __init__(self, botnick, adminname, channel):
            Irc.__init__(self, botnick, adminname, channel)


""" ===================== Test ====================== """
server = "chat.freenode.net"
channel = "##RoiLion"
botnick = "Jarvisbis"
adminname = "Mina"

irc = Bot(botnick, adminname, channel)
irc.connect(server)
irc.main()