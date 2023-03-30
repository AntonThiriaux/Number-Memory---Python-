#_____Fonctions_Imports________début_______________________________

from tkinter import *
import random
from threading import Timer
from tkinter import ttk
import os
import math
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#_____Fonctions_Imports_________fin________________________________



#_____Menu_Principal___________début_______________________________

master_root = Tk()
master_root.geometry("600x400")
master_root.title("        Memory geniuses menu")

background_color = "#eb405c" #rouge rose
font_color = "#FFFFFF" #white
master_root.configure(bg=background_color)

player_name = "Guest"

#_____Menu_Principal___________fin_________________________________



#_____Menu_Login______________début____________________________________________________

global login_window
global name_window

def account_session(username):
  '''
  Fonction permettant a l'utilisateur de voir les informations personnelles tels que la mediane
  la moyenne, l'ecart-type, le nombre de parties jouées, l'étendue de ses scores, l'evolution 
  avec un graphique. Si le joueur n'as pas joué encore une seul partie une fenetre s'affichera 
  en lui demandant de jouer d'abord une partie avant de voir ses statistiques.
  '''

  player_scores = list()

  with open(username) as file: #overture du fichier joueur
    for line in file:
      player_scores.append(line) #ajout des scores dans la list "player_scores"

  player_scores = player_scores[2::]
  player_scores = [elements.replace('\n','') for elements in player_scores]
  graph_scores = player_scores

  if len(player_scores) < 2:

    error_window = Toplevel()
    error_window.geometry('350x150+125+110')
    error_window.overrideredirect(True)
    error_window.config(bg=background_color)

    def error_window_destroy():
      '''
      Fonction s'affiche si le joueur n'as pas encore fait deux parties
      mais a clicker sur le bouton information.
      '''
      error_window.destroy()

    error_label = Label(error_window,text="Désolé, vous devez d'abord jouer\ndeux parties avant de pouvoir\nobserver vos statistiques. 😀", fg=font_color,            bg=background_color, justify='center')
    error_label.place(x=175, y=30,anchor=CENTER)
    
    error_button = Button(error_window, text="Continuer", command=error_window_destroy, bg=font_color, fg=background_color, activeforeground=font_color, activebackground=background_color, relief=FLAT, highlightthickness=0, bd=0)
    error_button.place(x=175,y=80,anchor=CENTER)
    

  else:

    global lb
    account = Tk()
    account.geometry('602x430')
    account.overrideredirect(True)
    account.config(bg=background_color)

    lb = Label(account, text='Observez vos statistiques:', font=('Arial', 12), fg=font_color, bg=background_color, justify='center')
    lb.place(x=300, y=40, anchor=CENTER)


    def int_min(t,j):
      '''
      Retourne l'indice de l'élément le plus petit d'une liste t a parti d'un indice j.
      '''
      
      n = len(t)
      imin = j
      mi = t[j]
      for k in range(j,n):
        if t[k] < mi:
          imin,mi = k,t[k]
      return imin


    def trie_selection(t):
      '''
      Retourne la liste 't' trié
      '''

      n = len(t)
      x = 0
      for r in range(n):
        i = int_min(t,r)
        if t[i]<t[x]:
          t[i], t[x] = t[x],t[i]
        r = r+1
        x = x+1
      return t

    def mediane(scores):
      '''
      Retourne la médiane d'une liste
      '''
      mediane = 0
      sort_scores = trie_selection(scores)
      n = len(sort_scores)
      if n % 2 == 0:
        mediane = (float(sort_scores[(n-1)//2])+float(sort_scores[(n+1)//2]))/2
      else:
        mediane = float(sort_scores[n//2])
      return mediane

    def meilleur_score(scores):
      '''
      Retourne le meilleur score dans la liste scores du joueur
      '''
      sort_scores = trie_selection(scores)
      return sort_scores[-1]


    
    def maximum(scores):
      '''
      Retourne la valeur maximale d'une liste
      '''
      max_scores = 0
      for index in range(len(scores)):
          if int(scores[index]) >= max_scores:
            max_scores = int(scores[index])

      return max_scores

    def minimum(scores):
      '''
      Retourne la valeur minimale d'une liste
      '''
      min_scores = maximum(scores)
      for index in range(len(scores)):
        if int(scores[index]) <= min_scores:
          min_scores = int(scores[index])

      return min_scores
    
    
    def etendue_score(scores):
      '''
      Retourne l'étendue des scores du joueur
      '''
      return maximum(scores)-minimum(scores)


    def evolution():
      '''
      Retourne en fonction de la liste evolution_scores si le joueur 
      est en amélioration ou pas sur ses deux derniers scores
      '''

      evolution_scores = list()

      with open(username) as file:
        for line in file:
          evolution_scores.append(line)
    
      evolution_scores = evolution_scores[2::]
      evolution_scores = [elements.replace('\n','') for elements in evolution_scores]
        
      dernier_score = evolution_scores[-1]
      avant_dernier_score = evolution_scores[-2]


      evolution_label = Label(account, text='', font=('typewriter', 9, 'italic'), bg=background_color, fg=font_color, justify='left')
      evolution_label.place(x=10,y=420,anchor=SW)

      if dernier_score > avant_dernier_score:
        evolution_label.config(text=f"Vous êtes en amélioration par rapport a\nvos deux derniers scores. Félicitations!")
      elif dernier_score < avant_dernier_score:
        evolution_label.config(text=f"Vous êtes en diminution par rapport a\nvos deux derniers scores. Continuez a vous\nentrainez et vous ferez de meilleurs scores.")
      else:
        evolution_label.config(text=f"Vous êtes en train de stagner. Ce n'est\npas mauvais mais essayez de vous\ndépasser et faire de meilleurs scores.")

    def graph(scores):
      '''
      Retourne grace a la librarie Matplotlib un graphique pour le nombre de fois que le joueur 
      a fait un certain nombre de score.
      '''
          

      player_scores_int = list()
      for elt in range(len(player_scores)):
        player_scores_int.append(int(player_scores[elt]))

      
      player_scores_finale = trie_selection(player_scores_int)
      
      
      def occurences_car(s):
        '''
        Retourne dans un dictionnaire le nombre d'occurences dans une liste.
        '''
        dic = {}
        for elt in s:
          if elt in dic.keys():
            dic[elt] += 1
          else:
            dic[elt] = 1
      
        return dic
        
      a_dictionary = occurences_car(player_scores_finale)
      
      keys = a_dictionary.keys()
      values = a_dictionary.values()
      fig = Figure(figsize = (2.9,2.8))
      plot1 = fig.add_subplot()
      plot1.bar(keys, values)
      canvas_scores = FigureCanvasTkAgg(fig, master = account)  
      canvas_scores.draw()
    
      # placing the canvas on the Tkinter window
      canvas_scores.get_tk_widget().place(x=608,y=430,anchor=SE)
      




    def moyenne(scores):
      '''
      Retourne la moyenne des scores d'une liste.
      '''
      moyenne = 0
      coef = 0
      for elements in range(len(scores)):
        moyenne += int(scores[elements])
        coef += 1
      if coef == 0:
        moyenne = 0
      else:
        moyenne = moyenne / coef
        moyenne = format(moyenne,".2f")
      return moyenne

    moyenne = moyenne(player_scores)

    def variance(scores):
      '''
      Retourne la variance des scores d'une liste.
      '''
      variance_scores = 0
      for index in range(len(scores)):
        variance_scores += (int(scores[index])-float(moyenne))**2

      variance_scores = float(format(variance_scores,".2f"))

      return variance_scores


    variance = variance(player_scores)
    

    def ecart_type(scores):
      '''
      Retourne l'ecart des scores d'une liste.
      '''
      ecart_type = variance ** 0.5

      ecart_type = format(ecart_type,'.2f')

      return ecart_type


    mediane = mediane(player_scores)
    etendue = etendue_score(player_scores)
    ecart = ecart_type(player_scores)
    meil_score = meilleur_score(player_scores)
    nb_partie_joue = len(player_scores)

    def petit_moins():
      global lb
      lb.config(font=('Arial',10))
      account.after(200,petit)

    def petit():
      global lb
      lb.config(font=('Arial',11))
      account.after(200,moyen)

    def moyen():
      global lb
      lb.config(font=("Arial",12))
      account.after(200,moyen_plus)

    def moyen_plus():
      global lb
      lb.config(font=("Arial",13))
      account.after(200,grand)

    def grand():
      global lb
      lb.config(font=('Arial', 14,'underline'))
      # reschedule event in 2 seconds

    account.after(50, petit_moins)

    def destroy_account_menu():
      account.destroy()

    lb_separateur_account = Label(account, text='____________________________________', font=("Cambria", 12, 'underline'), fg=font_color, bd=0, bg=background_color)
    lb_separateur_account.place(x=0, y=315)

    
    lb_info_moy_mediane_tout = Label(account, text=f"• La moyenne de vos scores est de {moyenne}.\n\n• La médiane observée est de {mediane}.\n\n• L'étendue est de {etendue}.\n\n• La variance est de {variance}.\n\n• L'écart-type est de {ecart}.\n\n• Votre meilleur score est de {meil_score}.\n\n• Nombre de parties jouées est de {nb_partie_joue}.", font=('typewriter', 9, 'italic'), bg=background_color, fg=font_color, justify='left')
    lb_info_moy_mediane_tout.place(x=10, y=110)
    

    graph_button = Button(account,text="Accédez à votre graphique", command=lambda:[graph(graph_scores), evolution()], borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('typewriter', 9), highlightthickness=0, bd=0, relief=FLAT)
    graph_button.place(x=465,y=120,anchor=CENTER)

    bt_home_main_menu = Button(account, text='⌂', command=destroy_account_menu, borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('Arial', 24), highlightthickness=0, bd=0, relief=FLAT)
    bt_home_main_menu.place(x=0, y=0)

    

def user_session(username_login):
  '''
  Personnalise le menu en fonction du nom du joueur.
  '''

  
  welcome.config(text=f'Bienvenue {username_login} à\nMemory Geniuses')
  login_window.destroy()
  name_window.destroy()

  account_button = Button(master_root, text="Infos", command= lambda:account_session(username_login), fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
  account_button.place(x=0, y=0)

  
  

def login():
  '''
  Fonction pour login ou register
  '''
  global name_window
  global player_name
  name_window = Toplevel()
  name_window.geometry('210x130+195+110')
  name_window.configure(bg=background_color)
  name_window.overrideredirect(True)

  def abandonner_login():
    name_window.destroy()

  def delete_login_success():
    login_success_window.destroy()


  def delete_login_error():
    login_error_window.destroy()


  def login_success(username):
    global player_name
    player_name=username
    user_session(username)

  def login_error():
    '''
    Fonction qui fait apparaitre une fenêtre lorsque le joueur n'entre pas le bon mot de passe ou nom d'utilisateur dans la fenêtre login
    '''
    global login_error_window
    login_error_window = Toplevel()
    login_error_window.geometry('300x200+150+110')
    login_error_window.configure(bg=background_color)
    login_error_window.overrideredirect(True)

    login_error_label = Label(login_error_window, text="Le nom d'utilisateur ou \nle mot de passe est incorrect.", font=("typewriter", 10, 'bold'), fg=font_color, bg=background_color, justify='center')
    login_error_label.place(x=150,y=40,anchor=CENTER)
    login_error_button = Button(login_error_window, text="Réessayer", command=delete_login_error, fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
    login_error_button.place(x=150,y=80,anchor=CENTER)
  
  def registration_error():
    username_exist_window.destroy()


  def name_already_exist():
    '''
    Affiche une fenêtre erreur si un nouveau compte veut etre crée sous un nom d'utilisateur qui existe déjà.
    '''
    global username_exist_window
    username_exist_window = Toplevel()
    username_exist_window.geometry('300x200+150+110')
    username_exist_window.configure(bg=background_color)
    username_exist_window.overrideredirect(True)

    username_exist_label = Label(username_exist_window,text="Désolé, ce nom d'utilisateur est déjà pris.\nVeuillez en utiliser un autre.", font=('typewriter', 9, 'italic'), bg=background_color, fg=font_color, justify='center')
    username_exist_label.place(x=150, y=30, anchor=CENTER)
    
    username_exist_button = Button(username_exist_window,text="Continuer", command=lambda:[login(), registration_error()], fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
    username_exist_button.place(x=150,y=100,anchor=CENTER)
    
  
    


    

  def register_user():
    '''
    Crée un fichier au nom de l'utilisateur et rentre son nom d'utilisateur et son mot de passe.
    '''
    username_info = username_entry_registration.get()
    password_info = password_entry_registration.get()
    
    username_entry_registration.delete(0, END)
    password_entry_registration.delete(0, END)

    list_of_files = os.listdir()
    if username_info in list_of_files:
      name_already_exist()

    else:

      file = open(username_info,"w")
      file.write(username_info + "\n")
      file.write(password_info + '\n')
      file.close()

    name_window.destroy()
    register_window.destroy()


  def login_verify():
    '''
    Vérifie que un utilisateur existe avec le bon mot de passe et nom d'utilisateur.
    '''
    username_verify_login = username_verify.get()
    password_verify_login = password_verify.get()

    username_entry.delete(0,END)
    password_entry.delete(0,END)

    list_of_files = os.listdir()
    if username_verify_login in list_of_files:
      file = open(username_verify_login,"r")
      verify = file.read().splitlines()
      if password_verify_login in verify:
        login_success(username_verify_login)
      else:
        login_error()
        
    else:
      login_error()


  def choisir_login_au_lieu_de_register():
    login_window.destroy()

  def choisir_register_au_lieu_de_login():
    register_window.destroy()


  def login_function():
    '''
    Permet au joueur de pouvoir se loger et entrer son nom d'utilisateur et mot de passe
    '''

    global login_window
    login_window = Toplevel()
    login_window.geometry('360x160+120+110')
    login_window.configure(bg=background_color)
    login_window.overrideredirect(True)


    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()


    global username_entry
    global password_entry

    back_bt = Button(login_window, text='❌', command=choisir_login_au_lieu_de_register, fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
    back_bt.place(x=360, y=-3, anchor=NE)

    information_label = Label(login_window,text="Veuillez remplir les informations ci-dessous", font=("typewriter", 9, 'underline','italic'), fg=font_color, bg=background_color, justify='center')
    information_label.place(x=0, y=0)

    username_label = Label(login_window, text = "Nom d'utilisateur: ", font=("typewriter", 9, 'bold'), fg=font_color, bg=background_color, justify='center')
    username_label.place(x=130,y=35,anchor=CENTER)
  
    username_entry = Entry(login_window, textvariable = username_verify, relief=FLAT)
    username_entry.insert(0, '* Username *')
    username_entry.focus_set()
    username_entry.place(x=150,y=60,anchor=CENTER)

    password_label = Label(login_window, text = "Mot de passe: ", font=("typewriter", 9, 'bold'), fg=font_color, bg=background_color, justify='center')
    password_label.place(x=120,y=85,anchor=CENTER)

    password_entry = Entry(login_window, show="*",textvariable = password_verify, relief=FLAT)
    password_entry.insert(0, 'password')
    password_entry.place(x=150, y=105, anchor=CENTER)

    login_button = Button(login_window, text = "Se connecter", command = login_verify,fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
    login_button.place(x=150,y=133,anchor=CENTER)
    login_window.bind('<Return>', lambda event=None:login_button.invoke())



  def register_function():
    '''
    Permet au joueur de pouvoir se crée un compte et donc de s'enregistrer sous un nom d'utilisateur et un mot de passe.
    '''

    global register_window

    global username_entry_registration
    global password_entry_registration

    register_window = Toplevel()
    register_window.geometry('360x160+120+110')
    register_window.configure(bg=background_color)
    register_window.overrideredirect(True)


    back_bt = Button(register_window, text='❌', command=choisir_register_au_lieu_de_login, fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
    back_bt.place(x=360, y=-3, anchor=NE)


    register_information = Label(register_window,text="Veuillez remplir les informations ci-dessous", font=("typewriter", 9, 'underline', 'italic'), fg=font_color, bg=background_color, justify='center')
    register_information.place(x=0, y=0)

    username_registration = Label(register_window,text="Creer un nom d'utilisateur:", font=("typewriter", 9, 'bold'), fg=font_color, bg=background_color, justify='center')
    username_registration.place(x=150,y=35,anchor=CENTER)
    
    username_entry_registration = Entry(register_window, relief=FLAT)
    username_entry_registration.insert(0, 'ex: Panda1')
    username_entry_registration.focus_set()
    username_entry_registration.place(x=150,y=60,anchor=CENTER)

    password_registration = Label(register_window,text="Créer un mot de passe:", font=("typewriter", 9, 'bold'), fg=font_color, bg=background_color, justify='center')
    password_registration.place(x=150,y=85,anchor=CENTER)
    password_entry_registration = Entry(register_window,relief=FLAT)
    password_entry_registration.insert(0, 'ex: Xva45/g')
    password_entry_registration.place(x=150,y=105,anchor=CENTER)

    def random_password_generator():
      '''
      Permet de générer un mot de passe aléatoire.
      '''
      lower = "abcdefghijklmnopqrstuvwxyz"
      upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
      number = "1234567890"
      symbols = "!@#$%^&*()?"
      password = lower + upper + number + symbols
      length = 10
      random_password = "".join(random.sample(password,length))
      password_entry_registration.delete(0,'end')
      password_entry_registration.insert(0,random_password)

    random_password_button = Button(register_window, text="génerer\naléatoirement", command=random_password_generator, font=('typewriter', 6), bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0)
    random_password_button.place(x=350,y=85,anchor=NE)

    register_button = Button(register_window, text='Créer un compte:', command=register_user,fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
    register_button.place(x=150,y=133,anchor=CENTER)
    register_window.bind('<Return>', lambda event=None:register_button.invoke())


  button_login = Button(name_window,text="Se connecter",command=login_function,fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
  button_login.place(x=100,y=25,anchor=CENTER)

  button_register = Button(name_window,text="Créer un compte", command=register_function, fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
  button_register.place(x=100,y=60,anchor=CENTER)

  retour_bt = Button(name_window, text='❌', command=abandonner_login, fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
  retour_bt.place(x=210, y=0, anchor=NE)

#______Menu_Login____________fin_______________________



#_____Menu_Jeu_Regles________début_________________________________

def menu():
  num = Toplevel()
  num.title('Number Memory')
  num.geometry('602x430')
  num.configure(bg=background_color)

  num.overrideredirect(True)

#_____Menu_Jeu_Regles_________fin__________________________________


#_____Jeu_bouton_home_________début________________________________

  def home():
    num.destroy()
  
#_____Jeu_Bouton_Home__________fin_________________________________
  


#_____Score_Save______________début________________________________
  def save_personnal_data(name,score):
    '''
    Permet de sauvegarder le score du joueur dans le fichier personnel de celui-ci.
    '''
    if score < 10:
      score = '00'+str(score)
    elif score < 100:
      score = '0'+str(score)
    personnal_file = open(name,'a')
    personnal_file.write(str(score)+'\n')
    personnal_file.close()
    




  def save_leaderboard_number_memory(name,score):
    '''
    Permet de sauvegarder, trier le score et verifier qu'il n'y a pas de doublons de nom dans un fichier text nommé leaderboard_number_memory.txt
    '''

    def check_duplicates(names,scores):
      '''
      Verifie qu'il n'y a pas de doublons de nom dans le fichier leaderboard
      Si il y en a: prendre le meilleur score des deux mêmes noms.
      '''
      duplicate_index = list()

      if len(names) == len(set(names)):
        sort_scores = dict(zip(names[::-1],scores[::-1]))
        sorted_scores = dict(sorted(sort_scores.items(), key=lambda x: x[1], reverse=True))
        return sorted_scores
      elif len(names) != len(set(names)):
        for index in range(len(names)):
          duplicate_index.append(int(index))

        if scores[duplicate_index[0]] > scores[duplicate_index[1]]:
          names.pop(duplicate_index[1])
          scores.pop(duplicate_index[1])
        else:
          names.pop(duplicate_index[0])
          scores.pop(duplicate_index[0])
      
        sort_scores = dict(zip(names[::-1],scores[::-1]))
        sorted_scores = dict(sorted(sort_scores.items(), key=lambda x: x[1], reverse=True))
        return sorted_scores

    def sort_leaderboard():
      '''
      Permet de trier le fichier leaderboard_number_memory.txt
      '''
      scores = list()
      names = list()
      with open("leaderboard_number_memory.txt") as file:
        for line in file:
          scores.append(line[0:3])
          names.append(line[6::])

      sorted_scores = check_duplicates(names,scores)

      f = open("leaderboard_number_memory.txt",'r+')
      f.seek(0)
      f.truncate(0)

      with open("leaderboard_number_memory.txt","a") as leader:
        for names,scores in sorted_scores.items():
          leader.write("{} : {}".format(scores,names))
        leader.close()

    player_name = name
    player_score = score
    if player_score <= 10:
      player_score = '00'+str(player_score)
    elif player_score <= 100:
      player_score = '0'+str(player_score)


    def save_score():
      '''
      Sauvegarde le score d'un joueur dans le fichier leaderboard_number_memory.txt
      '''
      file = open("leaderboard_number_memory.txt", "a")
      file.write("{} : {}\n".format(player_score, player_name))
      file.close()
      sort_leaderboard()
      


    if os.path.isfile('leaderboard_number_memory.txt') == True:
      save_score()
    else:
      file = open("leaderboard_number_memory.txt",'x')
      save_score()

#_____Score_Save_______________fin_________________________________



#_____Jeu_Commence____________début________________________________



  def number_memory(chrono, longeur, vitesse):
    '''
    Fonction du jeu number memory qui prend en compte trois parametres 
    "chrono", "longueur", "vitesse" en fonction de la difficulté choisi.
    '''
    global tps
    tps = chrono
    global pb_longeur
    global pb_vitesse
    pb_longeur = longeur
    pb_vitesse = vitesse
    #______________________variable importante__________________#
    global player_name
    #Tous les Golbals utilisés
    global score
    score = 0
    #____________________variable importante____________________#
    global minimum
    minimum = 1
    global maximum
    maximum = 9
    global level
    if chrono == 5.0:
      level = 1
    else:
      level = 0

    global n
    number_memory = Toplevel()
    number_memory.title("Number Memory")
    number_memory.geometry('602x430')
    num.destroy()
    number_memory.configure(bg=background_color)
    number_memory.overrideredirect(True)




#_____Menu_Retour_confirmation_début_______________________________

    def confirmation():
      '''
      Fonction permet à l'utilisateur de pouvoir quitter le jeu et retourner au menu principal
      '''

      def destroyer_wind():
        conf.destroy()

      def destroyer_all():
        number_memory.destroy()
        conf.destroy()

      conf = Tk()
      conf.title("Confirmation")
      conf.geometry("220x115+190+110")
      conf.configure(bg=background_color)

      conf.overrideredirect(True)


      label_confirm = Label(conf, text="Confirmez le retour \n en arrière au menu. \n ____________________________", font=("typewriter", 9, 'bold'), fg=font_color, bg=background_color, justify='center')
      label_confirm.place(x=110, y=40, anchor='center')

      bt_cancel = Button(conf, text="Annuler ❌", bg=background_color, fg=font_color, borderwidth=0, activeforeground=background_color, activebackground=font_color, command=destroyer_wind, highlightthickness=0, font=("typewriter", 10))
      bt_cancel.place(x=20, y=80)
      bt_confirm = Button(conf, text="Continuer ✔", bg=background_color, fg=font_color, borderwidth=0, activeforeground=background_color, activebackground=font_color, command=destroyer_all, highlightthickness=0, font=("typewriter", 10))
      bt_confirm.place(x=110, y=80)

#_____Menu_Retour_confirmation__fin________________________________




#_____Barre_de_Chargement______début_______________________________

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", background=font_color, relief=FLAT, darkcolor=background_color, lightcolor=background_color, bordercolor=background_color, highlightthickness=0)
    pb = ttk.Progressbar(number_memory, orient='horizontal', mode='determinate', length=pb_longeur, style="red.Horizontal.TProgressbar")
    pb.place(x=580, y=10, anchor='ne')
        #pb.place(x=580, y=10, anchor='ne')
    pb.start(pb_vitesse)
    
#_____Barre_de_Chargement_______fin________________________________




  #Bouton Home
    button_home = Button(number_memory, text='⌂', command=confirmation, borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('Arial', 24), highlightthickness=0, bd=0, relief=FLAT)
    #.grid(row = 0, column = 1)
    button_home.place(x=0, y=0)

#_____Jeu_Nombre_Afficher_______début______________________________
    def afficher_nombre():
      '''
      Fonction qui affiche un nombre aléatoire entre le minimum et le maximum.
      '''
      
      #Fonction Globals
      global label_n
      global label_pres
      global label_s
      global label_score
      global n

      label_pres = Label(number_memory, text="Retenez ce nombre!", font=("Cambria", 24, "underline"), fg=font_color, bd=0, bg=background_color)
          #.grid(row = 0, column=0)
      label_pres.place(x=300, y=85, anchor='center')

      label_s = Label(number_memory, text="Score:", font=("typewriter", 13, "bold"), fg=font_color, bg=background_color)
      label_s.place(x=300, y=17, anchor='center')
      label_score = Label(number_memory, text=score, font=("typewriter", 13), fg=font_color, bg=background_color)
      label_score.place(x=300, y=40, anchor='center')

      n = random.randint(minimum, maximum)

      label_n = Label(number_memory, text=n, font=("Cambria", 46), fg=font_color, bd=0, bg=background_color)
      label_n.place(x=300, y=200, anchor='center')
    
    afficher_nombre()

#_____Jeu_Nombre_Afficher________fin_______________________________




#_____Jeu_Nombre_Changer________début______________________________

    def change():
      '''
      Change le label du score et affiche une boite pour entrer le nombre 
      ainsi que le bouton valider
      '''

      #Fonction Global
      global level
      global pb_vitesse
      global pb_longeur
      global tps
      global Bt_continue
      global x
      global n
      global score
      global minimum
      global maximum
      global label_n
      global label_pres
      global label_s
      global label_score
      global player_name

      pb.destroy()
      label_n.config(text="")
      entry_x = Entry(number_memory, highlightthickness=0, bd=0)
      entry_x.focus_set()
      entry_x.place(x=300, y=180, anchor='center', width=180, height=32)
      label_pres.config(text="Ecrivez le!")



#_____Jeu_Nouveau_Nombre_______début_______________________________

      def nouveau_nombre():
        '''
        Crée un nouveau nombre avec toujours un caractère de plus a chaque tour.
        '''

        global pb_vitesse
        global pb_longeur
        global tps

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", background=font_color, relief=FLAT, darkcolor=background_color, lightcolor=background_color, bordercolor=background_color, highlightthickness=0)
        pb = ttk.Progressbar(number_memory, orient='horizontal', mode='determinate', length=pb_longeur, style="red.Horizontal.TProgressbar")
        pb.place(x=580, y=10, anchor='ne')
        pb.start(pb_vitesse)

        entry_x.destroy()
        Bt_continue.destroy()

        label_pres.config(text="Retenez ce nombre!")
        label_n.config(text=n)
        label_score.config(text=score)

        t = Timer(tps, change)
        t.start()

        def progress():
          pb.destroy()
        timer = Timer(tps, progress)
        timer.start()

#_____Jeu_Nouveau_Nombre_______fin_________________________________



#_____Jeu_Verifie_Nombre_______début_______________________________
      
      def valider():
        '''
        Compare le nombre afficher et le nombre écrit par l'utilisateur dans la boîte et vérifie si elles sont égales
        Si c'est le cas, un noveau nombre est génerée dans la fonction 'nouveau_nombre()'
        Sinon il affiche une fenêtre 'perdu'
        '''
        global Bt_continue
        global x
        global n
        global score
        global minimum
        global maximum
        global level
        global player_name
        global score

        def change_save():
          bt_save_score.config(text='Sauvé ✔', activebackground=background_color, activeforeground=font_color)


        if entry_x.get().isnumeric() == True:

          if int(entry_x.get()) == n:
            score += 1
            minimum = str(minimum) + '0'
            maximum = str(maximum) + '9'
            minimum = int(minimum) 
            maximum = int(maximum)

            n = random.randint(minimum, maximum)
            if score >= 20:
              label_n.config(text=n, font=("Cambria",24))
            elif score >= 12:
              label_n.config(text=n, font=("Cambria", 32))


          elif int(entry_x.get()) != n:
            lost = Toplevel()
            lost.geometry('602x430')
            lost.title('Number Memory')
            lost.configure(bg=background_color)
            lost.overrideredirect(True)
            def menuretour():
              number_memory.destroy()
              lost.destroy()
            
              
            label_lost = Label(lost, text='Dommage, vous avez perdu!', font=("Cambria", 18, 'underline'), fg=font_color, bd=0, bg=background_color)
            label_lost.place(x=300, y=35, anchor=CENTER)
            label_ligne1 = Label(lost, text='______________________________________________________________________________________________________________', font=("Cambria", 20, 'underline'), fg=font_color, bd=0, bg=background_color)
            label_ligne1.place(x=300, y=70, anchor=CENTER)
            label_reponse = Label(lost, text=f'Nombre marqué:  {entry_x.get()}', font=("Cambria", 18, 'italic'), fg=font_color, bd=0, bg=background_color)
            label_reponse.place(x=300, y=125, anchor=CENTER)
            label_nombre = Label(lost, text=f'Nombre donné: {n}', font=("Cambria", 18, 'italic'), fg=font_color, bd=0, bg=background_color)
            label_nombre.place(x=300, y=185, anchor=CENTER)
            label_score_fin = Label(lost, text=f'Score final:   {score}', font=("Cambria", 18, 'italic'), fg=font_color, bd=0, bg=background_color)
            label_ligne2 = Label(lost, text='______________________________________________________________________________________________________________', font=("Cambria", 20, 'underline'), fg=font_color, bd=0, bg=background_color)
            label_ligne2.place(x=300, y=300, anchor=CENTER)
            label_score_fin.place(x=300, y=245, anchor=CENTER)
            bt_retour_au_menu = Button(lost, text='Retour au menu ➢', command=menuretour, borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('Arial', 16), highlightthickness=0, bd=0, relief=FLAT)
            bt_retour_au_menu.place(x=300, y=350, anchor=CENTER)

            if level == 1:

              if player_name != "Guest":
                save_personnal_data(player_name,score)

              bt_save_score = Button(lost, text='Sauvegarder ↻', command=lambda:[change_save(), save_leaderboard_number_memory(player_name,score)], borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('Arial', 12), highlightthickness=0, bd=0, relief=FLAT)
              lost.bind('<s>', lambda event=None:bt_save_score.invoke())
              bt_save_score.place(x=300, y=283, anchor=CENTER)

          nouveau_nombre()
        else:
          label_pres.config(text="Erreur de Saisie!")
  
#_____Jeu_Verifie_Nombre_________fin_______________________________

      #Boutons
      Bt_continue = Button(number_memory, text='Valider ➢', command=valider, fg=font_color, bg=background_color, activeforeground=background_color, activebackground=font_color, highlightthickness=0, bd=0, relief=FLAT)
      Bt_continue.place(x=300, y=240, anchor='center')
      number_memory.bind('<Return>', lambda event=None: Bt_continue.invoke())

  #Jeu_Nombre_Changer_Chrono
    temps = Timer(tps, change)
    temps.start()

#_____Jeu_Nombre_Changer_________fin_______________________________



#_____Menu_Jeu_Regles________début_________________________________

  label_r = Label(num, text='Règles', font=('Cambria', 24, 'underline'), bg=background_color, fg=font_color).place(x=300, y=80, anchor='center')

  label_regles = Label(num, text="Un nombre apparaitra.  Vous aurez un certain nombre\n de secondes en fonction du mode choisit pour le \nmémoriser. À la fin du temps, réecrivez le dans la \ncase blanche qui sera apparût. Bien sûr le nombre \ns'incrémentera d'un chiffre à chaque tour. Ne\ntrichez pas et bonne chance. 😉 ", justify='center', bg=background_color, fg=font_color).place(x=300, y=170, anchor='center')


  Bt_facile = Button(num, text='Facile ➢\n(9s)', command=lambda *args: number_memory(9.0, 180, 90), bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0, justify='center').place(x=200, y=280, anchor=('center'))


  Bt_moyen = Button(num, text='Moyen ➢\n(7s)', command=lambda *args: number_memory(7.0, 140, 70), bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0, justify='center').place(x=300, y=280, anchor=('center'))


  Bt_difficile = Button(num, text='Difficile ➢\n(5s)', command=lambda *args: number_memory(5.0, 100, 50), bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0, justify='center').place(x=400, y=280, anchor=('center'))


  button_home = Button(num, text='⌂', command=home, borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('Arial', 24), highlightthickness=0, bd=0, relief=FLAT).place(x=0, y=0)

#_____Menu_Jeu_Regles_________fin__________________________________



#_____Menu_scores____________début_________________________________

def leaderboard():
  '''
  Affiche un classement avec les meilleurs scores des joueurs pour le mode difficile seulement 
  '''
  lead = Toplevel()
  lead.overrideredirect(True)
  lead.geometry('602x430')
  lead.configure(bg=background_color)

  scores_records = list()
  names_records = list()
  with open("leaderboard_number_memory.txt") as file:
    for line in file:
      scores_records.append(line[0:3])
      names_records.append(line[6::])

  labels = []
  record = list()
  for index in range(len(names_records)):
    record.append(f"{str(scores_records[index])} : {str(names_records[index])}")


  for i in range(len(record)):
    labels.append(Label(lead,text=record[i],background=background_color,width=100,fg=font_color, font=('typewriter', 10)))
    labels[i].place(x=300,y=170+(35*i),anchor=CENTER)

  lb_place = Label(lead, text='1.\n\n2.\n\n3.', font=('typewriter', 9, 'underline'), bg=background_color, fg=font_color, justify=RIGHT)
  lb_place.place(x=200, y=195, anchor=CENTER)


  def retour_m():
    lead.destroy()

  label_Leader = Label(lead, text='Tableau des scores', font=('Calibri', 29, 'underline'), bg=background_color, fg=font_color).place(x=300, y=70, anchor=CENTER)


  bt_retour_menu = Button(lead, text='⌂', command=retour_m, borderwidth=0, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, font=('Arial', 24), highlightthickness=0, bd=0, relief=FLAT).place(x=0, y=0)
  
#------------Easter Egg---------------#

def easter_a(e):
  def easter_w(e):
    def easter_e(e):
      def easter_s(e):
        def easter_o(e):
          def easter_m(e):
            def easter_ee(e):

              def petit():
                global welcome
                welcome.config(fg='yellow')
                master_root.after(200, grand)

              def moyen_plus():
                global welcome
                welcome.config(fg='magenta')
                master_root.after(200, petit)

              def grand():
                global welcome
                welcome.config(fg='cyan')
                master_root.after(200,moyen_plus)
                # reschedule event in 2 seconds

              master_root.after(500,petit)

            master_root.bind('<e>', easter_ee)
          master_root.bind('<m>', easter_m)
        master_root.bind('<o>', easter_o)
      master_root.bind('<s>', easter_s)
    master_root.bind('<e>', easter_e)
  master_root.bind('<w>', easter_w)
master_root.bind('<a>', easter_a)


#_____Menu_Principal___________début_______________________________

welcome = Label(master_root, text="Bienvenue à\nMemory Genuises", font=('Cambria', 29, 'underline'), bg=background_color, fg=font_color)
welcome.place(x=300, y=100, anchor='center')

Bt_nb = Button(master_root, text="Number Memory ➢", command=menu, bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0, font=("typewriter", 14)).place(x=320, y=260, anchor=('center'))

Bt_leaderboard = Button(master_root, text='⭐', command = leaderboard, font=('typewriter', 14), bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0).place(x=190, y=260, anchor=CENTER)

#_____Menu_Principal___________fin________________________________



#_____Menu_Login______________début____________________________________________________

Bt_login = Button(master_root, text='Se connecter\nCréer un compte', command=login, font=('typewriter', 10), bg=background_color, fg=font_color, activeforeground=background_color, activebackground=font_color, relief=FLAT, highlightthickness=0, bd=0)
Bt_login.place(x=600, y=0, anchor=NE)

#______Menu_Login____________fin_______________________
mainloop()