import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import ttk
import serial as serial
from playsound import playsound

# Programme de gestion du MBot en bluetooth.

# Configuration :
port = '/dev/ttyACM0'
precision = 1

MBot = serial.Serial(port=port, baudrate=115200, timeout=.1)

# Fonction servent à ajouter des zéros.


def complete_with_zeros(num, n):
    num_str = str(num)
    if len(num_str) >= n:
        return num_str
    else:
        return '0' * (n - len(num_str)) + num_str

# Fonction envoyant un message en UART au MBot.


def send_message(message):
    message += '\n'
    MBot.write(bytes(message, 'utf-8'))
    print('Message envoyé au MBot : ' + message)

# Effectue un déplacement du MBot pour un temps donnée (de 0 à 9 secondes).


def move_MBot_timer(event, move, time):
    send_message('0' + str(move) + str(time))

# Débute le déplacement du MBot.


def move_MBot(event, move):
    send_message('1' + str(move))

# Définit le mode du MBot.


def set_mode(*args):
    selected_value = current_mode.get()
    send_message('2' + selected_value)

# Définit la vitesse du MBot.


def set_speed(event):
    speed = complete_with_zeros(int(current_speed.get()), 3)
    send_message('31' + speed)

# Définit la vitesse de rotation du MBot.


def set_rotation_speed(event):
    speed = complete_with_zeros(int(current_rotation_speed.get()), 3)
    send_message('32' + speed)

# Définit la couleur des DEL.


def change_color():
    color = askcolor(title='Choix de la couleur des DEL embarquées')
    if color[1]:
        r = int(color[0][0])
        g = int(color[0][1])
        b = int(color[0][2])
        send_message('4' + complete_with_zeros(r, 3) +
                     complete_with_zeros(g, 3) + complete_with_zeros(b, 3))


def serial_loop():
    if MBot.in_waiting > 0:
        message = MBot.readline().decode().strip()
        print('Message reçu du MBot : ' + message)
        match message[0]:
            case '0':
                lenght = int(message[2]) + int(message[1]) * 10
                distance_bar['value'] = lenght
            case '1':
                playsound('./assets/fart.mp3', False)

    root.after(10, serial_loop)


# Initialisation de la fenêtre.
root = tk.Tk()
root.title('Contrôleur MBot 3000 - Édition "PAUL MET LES GAZ"')
root.geometry('1150x450+50+50')
root.resizable(False, False)

# Ajout du titre.
title = ttk.Label(root, text='Contrôleur MBot 3000', font=('Calibri', 17))
title.pack()

# Mise en place du contrôle du MBot par les touches du clavier.
root.bind('<KeyPress-Up>', lambda event: move_MBot_timer(event, 1, precision))
root.bind('<KeyPress-Down>',
          lambda event: move_MBot_timer(event, 2, precision), add='+')
root.bind('<KeyPress-Left>',
          lambda event: move_MBot_timer(event, 3, precision), add='+')
root.bind('<KeyPress-Right>',
          lambda event: move_MBot_timer(event, 4, precision), add='+')

# Mise en place des boutons de contrôle du MBot.
ttk.Label(root, text='Contrôle du MBot', font=(
    'Calibri', 10)).place(x=165, y=60)
up_button = ttk.Button(root, text='↑')
up_button.bind('<ButtonPress-1>', lambda event: move_MBot(event, 1))
up_button.bind('<ButtonRelease-1>', lambda event: move_MBot(event, 0))
up_button.place(x=175, y=110)
down_button = ttk.Button(root, text='↓')
down_button.bind('<ButtonPress-1>', lambda event: move_MBot(event, 2))
down_button.bind('<ButtonRelease-1>', lambda event: move_MBot(event, 0))
down_button.place(x=175, y=190)
left_button = ttk.Button(root, text='←')
left_button.bind('<ButtonPress-1>', lambda event: move_MBot(event, 3))
left_button.bind('<ButtonRelease-1>', lambda event: move_MBot(event, 0))
left_button.place(x=100, y=150)
right_button = ttk.Button(root, text='→')
right_button.bind('<ButtonPress-1>', lambda event: move_MBot(event, 4))
right_button.bind('<ButtonRelease-1>', lambda event: move_MBot(event, 0))
right_button.place(x=250, y=150)

# Sélecteur de modes.
ttk.Label(root, text='Mode', font=('Calibri', 10)).place(x=550, y=60)
current_mode = tk.StringVar(value='1')
current_mode.trace_add('write', set_mode)
modes = (('Manuel', '1'),
         ('Autonome', '2'),
         ('Suiveur de ligne', '3'),
         ('Combat', '4'))
i = 0
for mode in modes:
    r = ttk.Radiobutton(
        root,
        text=mode[0],
        value=mode[1],
        variable=current_mode
    )
    r.place(x=500, y=110 + 30 * i)
    i = i + 1

ttk.Label(root, text='Vitesses', font=('Calibri', 10)).place(x=900, y=60)

# Sélecteur de la vitesse.
ttk.Label(root, text='- Vitesse ligne droite +',
          font=('Calibri', 10)).place(x=840, y=110)
current_speed = tk.DoubleVar(value=100)
speed_slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    length=300,
    orient='horizontal',
    variable=current_speed
)
speed_slider.bind('<ButtonRelease-1>', set_speed)
speed_slider.place(x=775, y=150)

# Sélecteur de la vitesse de rotation.
ttk.Label(root, text='- Vitesse de rotation +',
          font=('Calibri', 10)).place(x=840, y=180)
current_rotation_speed = tk.DoubleVar(value=100)
rotation_speed_slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    length=300,
    orient='horizontal',
    variable=current_rotation_speed
)
rotation_speed_slider.bind('<ButtonRelease-1>', set_rotation_speed)
rotation_speed_slider.place(x=775, y=210)

# Boutons de modes spéciaux.
ttk.Label(root, text='Commandes spéciales', font=(
    'Calibri', 10)).place(x=140, y=260)
ttk.Button(
    root,
    text='Fréquences',
    command=lambda: send_message('51')).place(x=170, y=300)
ttk.Button(
    root,
    text='Police',
    command=lambda: send_message('52')).place(x=170, y=350)

# Affichage de la distance avec l'objet le plus proche.
ttk.Label(root, text='Capteur à ultrasons', font=(
    'Calibri', 10)).place(x=480, y=260)
distance_bar = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
    length=200
)
distance_bar.place(x=470, y=300)

# Sélecteur de couleur des DEL
ttk.Label(root, text='Choix de la couleur des DEL',
          font=('Calibri', 10)).place(x=820, y=260)
color_button = ttk.Button(
    root,
    text='Couleur des DEL',
    command=change_color).place(x=850, y=300)

serial_loop()

root.mainloop()