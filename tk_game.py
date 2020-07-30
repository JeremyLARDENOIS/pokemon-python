#!/usr/bin/python3

from tkinter import *

class Interface(Frame):
    '''Classe de l'interface graphique'''
    def __init__(self):
        '''Initialisation de la fenetre avec la page d'accueil'''

        self.fenetre = Tk()

        self.content = Frame(self.fenetre)
        self.content.pack()

        self.txt = Label(self.content, text="Hello World",)
        self.txt.pack()
        
        self.buttonDuel = Button(self.content,text="Mode Duel", command=self.duel)
        self.buttonDuel.pack()


        self.buttonq = Button(self.content,text="Quit", command=self.quit)
        self.buttonq.pack()

        self.fenetre.mainloop()
    
    def quit(self):
        self.fenetre.destroy()

    def refresh(self):
        '''Supprime tout le contenu et recrée une Frame content dans fenetre'''
        self.content.destroy()
        self.content = Frame(self.fenetre)
        self.content.pack()

    def duel(self):
        self.refresh()

        self.button1p = Button(self.content,text="1 joueur")
        self.button1p.pack()

        self.button2p = Button(self.content,text="2 joueurs")
        self.button2p.pack()

def main ():
    interface = Interface()


main()
