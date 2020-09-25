#!/usr/bin/python3

from tkinter import *

class Interface(Frame):
    '''Classe de l'interface graphique'''
    def __init__(self):
        '''Initialisation de la fenetre avec la page d'accueil'''

        self.fenetre = Tk()

        self.content = Frame(self.fenetre)
        self.content.pack()

        self.menu()
        self.fenetre.mainloop()

    def quit(self):
        self.fenetre.destroy()

    def refresh(self):
        '''
        Supprime tout le contenu et recrée une Frame content dans fenetre
        Toutes les fonctions ci-dessous doivent commencer par l'appel de cette fonction
        '''

        self.content.destroy()
        self.content = Frame(self.fenetre)
        self.content.pack()


    def notAvailable(self):
        '''
        Indique que le contenu n'est pas encore disponible
        et renvoie sur la page d'accueil
        '''
        self.refresh()

        self.txt = Label(self.content, text="Ce contenu n'est pas encore disponible")
        self.txt.pack()
        
        self.buttonDuel = Button(self.content,text="Page d'accueil", command=self.menu)
        self.buttonDuel.pack()


    def menu(self):
        '''Page d'accueil'''
        def duel():
            def duel1p():
                import duel1p
                duel1p.main(self)

            self.refresh()

            self.button1p = Button(self.content,text="1 joueur", command = duel1p)
            self.button1p.pack()

            self.button2p = Button(self.content,text="2 joueurs",command = self.notAvailable)
            self.button2p.pack()


        self.refresh()

        self.txt = Label(self.content, text="Hello World",)
        self.txt.pack()
        
        self.buttonDuel = Button(self.content,text="Mode Duel", command=duel)
        self.buttonDuel.pack()


        self.buttonq = Button(self.content,text="Quit", command=self.quit)
        self.buttonq.pack()

####################################################################################################
    
def main ():
    Interface()

####################################################################################################

main()
