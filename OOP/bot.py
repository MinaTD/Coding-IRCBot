#!usr/bin/env python
import socket


class IRC:


    def __init__(self):
        self.ircsock   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.botnick   = "Jarvisbis"
        self.adminname = "Mina" 
        self.exitcode  = "bye " + self.botnick

    # Connection to the server
    def connect(self, server = "chat.freenode.net", botnick = "Jarvisbis"):
        self.ircsock.connect((server, 6667)) 
        self.ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8"))
        self.ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))

    # join Channel
    def joinchan(self, chan):
        self.ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) 
        self.ircmsg = ""

        while self.ircmsg.find("End of /NAMES list.") == -1:  
            self.ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            self.ircmsg = self.ircmsg.strip('\n\r')
            print(self.ircmsg)

    def ping(self):
        self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

    def sendmsg(self, msg, target="##RoiLion"):
        self.ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

    def main(self):
        channel = "##RoiLion"
        self.joinchan(channel)
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
                        self.sendmsg("Ouais merci, je sais ! on m'appelle le BG du web")
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

irc = IRC()
irc.connect()
irc.main()