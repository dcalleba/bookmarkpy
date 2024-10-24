import tkinter as tk
from PIL import Image, ImageTk
import ephem
import datetime

def get_moon_phase_and_times():
    """
    Cette fff git log
    fonction retourne la phase de la lune, l'heure de lever, l'heure de coucher et l'âge de la lune.
    """
    observer = ephem.Observer()
    observer.lat = '48.8566'  # Latitude de Paris
    observer.lon = '2.3522'    # Longitude de Paris
    observer.elevation = 35     # Élévation en mètres

    moon = ephem.Moon(observer)
    
    moonrise = observer.next_rising(moon)
    moonset = observer.next_setting(moon)
    
    # Formatage des heures en heure locale (Paris)
    moonrise_time = ephem.localtime(moonrise).strftime('%H:%M')
    moonset_time = ephem.localtime(moonset).strftime('%H:%M')
    
    # Calcul de la phase et de l'âge de la lune
    phase = moon.moon_phase
    new_moon_date = ephem.previous_new_moon(observer.date)
    
    # Calculer l'âge de la lune en jours
    age_of_moon = (observer.date - new_moon_date) % 29.53  # Âge en jours dans le cycle lunaire
    
    return phase, moonrise_time, moonset_time, age_of_moon

def changer_image(phase):
    """
    Change l'image affichée en fonction de la phase de la lune sélectionnée.
    
    :param phase: Le nom de la phase de la lune.
    """
    image_path = f"{phase}.png"  # Assurez-vous que les images sont nommées correctement
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    
    label_image.config(image=photo)
    label_image.image = photo  # Garder une référence à l'image

def update_info():
    """
    Met à jour le label avec la phase actuelle, les heures de lever et coucher, et l'âge.
    """
    phase, moonrise_time, moonset_time, age_of_moon = get_moon_phase_and_times()
    
    # Interprétation de la phase
    if phase < 0.03 or phase > 0.97:
        phase_description = "Nouvelle Lune"
        changer_image("nouvelle_lune")
    elif phase < 0.25:
        phase_description = "Premier Croissant"
        changer_image("premier_croissant")
    elif phase < 0.5:
        phase_description = "Premier Quartier"
        changer_image("premier_quartier")
    elif phase < 0.75:
        phase_description = "Gibbeuse Croissante"
        changer_image("gibbeuse_croissante")
    else:
        phase_description = "Pleine Lune"
        changer_image("pleine_lune")
    
    # Mise à jour du label avec les informations
    label_info.config(text=f"Phase: {phase_description}\nLever: {moonrise_time}\nCoucher: {moonset_time}\nÂge: {age_of_moon:.2f} jours")

# Création de l'interface graphique
fenetre = tk.Tk()
fenetre.title("Phases de la Lune")

# Création d'un label pour afficher l'image
label_image = tk.Label(fenetre)
label_image.pack(pady=20)

# Label pour afficher les informations sur la lune
label_info = tk.Label(fenetre, text="")
label_info.pack(pady=10)

# Bouton pour mettre à jour l'affichage
button_update = tk.Button(fenetre, text="Afficher Info Lune", command=update_info)
button_update.pack(pady=10)

# Lancement de l'application
fenetre.mainloop()