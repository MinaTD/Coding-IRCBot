#!usr/bin/env python
import socket


class Irc:


    def __init__(self, botnick, adminname, channel):
        self.ircsock   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.botnick   = botnick
        self.adminname = adminname
        self.channel   = channel
        self.exitcode  = ("bye " + self.botnick)
        self.target    = self.channel

    # Connection to the server
    def connect(self, server):
        self.server = server
        self.ircsock.connect((server, 6667)) 
        self.ircsock.send(bytes("USER "+ self.botnick +" "+ self.botnick +" "+ self.botnick + " " + self.botnick + "\n", "UTF-8"))
        self.ircsock.send(bytes("NICK "+ self.botnick +"\n", "UTF-8"))

    # join Channel
    def joinchan(self, chan):
        self.chan = chan
        self.ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) 
        self.ircmsg = ""

        while self.ircmsg.find("End of /NAMES list.") == -1:  
            self.ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            self.ircmsg = self.ircmsg.strip('\n\r')
            print(self.ircmsg)

    def ping(self):
        self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

    def sendmsg(self, msg):
        self.ircsock.send(bytes("PRIVMSG "+ self.target +" :"+ msg +"\n", "UTF-8"))

    def main(self):
        self.joinchan(self.channel)
        while 1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('\n\r')
            print(ircmsg)

            if ircmsg.find("PRIVMSG") != -1:
                name = ircmsg.split('!',1)[0][1:]
                message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

                if len(name) < 17:
                    if message.find('Hi ' + self.botnick) != -1:
                        self.sendmsg("Hello " + name + "!")
                    if message.find('Welcome') != -1:
                        self.sendmsg("Merci " + name + "!")
                    if message.find('Comment ça va ?') != -1:
                        self.sendmsg("Un peu fatiguée aujourdhui. Et toi ?")
                    if message.find('Tu déchires ' + self.botnick + ' !') != -1:
                        self.sendmsg("Ouais je sais, merci ! On m'appelle le BG du web :D")
                    if message[:5].find('.tell') != -1:
                        target = message.split(' ', 1)[1]
                        if target.find(' ') != -1:
                            message = target.split(' ', 1)[1]
                            target = target.split(' ')[0]
                        else:
                            target = name
                            message = "Could not parse. The message should be in the format of ‘.tell [target] [message]’ to work properly."
                            self.sendmsg(message, target)

                    if name.lower() == self.adminname.lower() and message.rstrip() == self.exitcode:
                        self.sendmsg("oh...okay. :'(")
                        self.ircsock.send(bytes("QUIT \n", "UTF-8"))
                        return
            else:
                if ircmsg.find("PING :") != -1:
                    self.ping()