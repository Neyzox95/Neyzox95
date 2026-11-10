# -*- coding: utf-8 -*-
import customtkinter as ctk
import subprocess
import time
import pyautogui
import pyperclip
import os
import webbrowser
import threading
import sys
import tkinter as tk

SCRIPT_LUA = 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Aysoo9z/Monmenu/refs/heads/main/menu.lua"))()'

CHEMIN_XENO = r"C:\Users\alvin\Desktop\Mazz\dist\Xeno-v1.3.65\Xeno.exe"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def lancer_animation_bagdad():
    splash = ctk.CTkToplevel(app)
    splash.overrideredirect(True)
    splash.attributes("-topmost", True)
    
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    splash.geometry(f"{screen_w}x{screen_h}+0+0")
    
    splash.configure(fg_color="#000000")
    splash.attributes("-transparentcolor", "#000000")
    
    lbl = ctk.CTkLabel(splash, text="! Bagdad", font=("Impact", 120, "italic"), text_color="#0F2D5A")
    lbl.place(relx=0.5, rely=0.5, anchor="center")
    
    def animation_complete():
        alpha = 0.0
        splash.attributes("-alpha", alpha)
        while alpha < 1.0:
            alpha += 0.1
            try: splash.attributes("-alpha", alpha)
            except: break
            time.sleep(0.02)
            
        time.sleep(2.5) 
        
        while alpha > 0.0:
            alpha -= 0.1
            try: splash.attributes("-alpha", alpha)
            except: break
            time.sleep(0.02)
            
        splash.destroy()
        try:
            app.deiconify()
            animer_fenetre()
        except: pass

    app.after(100, lambda: threading.Thread(target=animation_complete, daemon=True).start())

def animer_fenetre():
    app.attributes("-alpha", 0.0)
    position_finale = (app.winfo_x(), app.winfo_y())
    app.geometry(f"+{position_finale[0]}+{position_finale[1] + 30}")
    def etape(i):
        if i > 40:
            app.geometry(f"+{position_finale[0]}+{position_finale[1]}")
            return
        alpha = i / 40
        decalage = int(30 * (1 - alpha))
        app.attributes("-alpha", alpha)
        app.geometry(f"+{position_finale[0]}+{position_finale[1] + decalage}")
        app.after(15, lambda: etape(i + 1))
    etape(0)

def pulsation_titre():
    couleurs = [(15, 45, 90), (30, 80, 160), (15, 45, 90), (10, 30, 60)]
    index = [0]
    def step():
        r, g, b = couleurs[index[0] % len(couleurs)]
        lbl_titre.configure(text_color=f"#{r:02x}{g:02x}{b:02x}")
        index[0] += 1
        app.after(400, step)
    step()

def animer_bouton_survol(event):
    etat = {"couleur": [255, 0, 60]}
    def step(i):
        if i > 10: return
        c = etat["couleur"]
        c[1] = min(255, c[1] + 6)
        c[2] = min(255, c[2] + 8)
        btn_lancer.configure(fg_color=f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}")
        app.after(15, lambda: step(i + 1))
    step(0)

def animer_bouton_sortie(event): btn_lancer.configure(fg_color="#FF003C")

def animer_progression(demarrer=True):
    if demarrer:
        barre_progression.pack(pady=(0, 10), padx=40, fill="x")
        barre_progression.start()
    else:
        barre_progression.stop()
        barre_progression.pack_forget()

def clignoter_bouton_erreur():
    etat = [True]
    def step(n):
        if n > 6:
            btn_lancer.configure(fg_color="#FF003C")
            return
        btn_lancer.configure(fg_color="#FF003C" if etat[0] else "#550000")
        etat[0] = not etat[0]
        app.after(200, lambda: step(n + 1))
    step(0)

def coller_script(texte, log_func, label):
    log_func("[*] Préparation : " + label)
    pyperclip.copy(texte)
    time.sleep(1)
    try:
        xeno_fenetre = pyautogui.getWindowsWithTitle("Xeno")[0]
        xeno_fenetre.activate()
    except Exception:
        log_func("[!] Clique sur la fenêtre Xeno (5 sec)...")
        time.sleep(5)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    log_func("[+] " + label + " collé.")

def ecrire_log_direct(texte):
    log.insert("end", texte + "\n")
    log.see("end")

def lancer_cheat():
    btn_lancer.configure(state="disabled", text="LANCEMENT EN COURS...", fg_color="#555555")
    animer_progression(True)
    log.configure(state="normal")
    log.delete("0.0", "end")

    def update_log(msg):
        ecrire_log_direct(msg)
        app.update()

    update_log("[*] Ouverture de Roblox...")
    webbrowser.open("roblox://experiences/start")
    time.sleep(15)

    update_log("[*] Lancement de Xeno...")
    if os.path.exists(CHEMIN_XENO):
        subprocess.Popen([CHEMIN_XENO], shell=True)
    else:
        update_log("[!] ERREUR : Xeno.exe introuvable.")
        animer_progression(False)
        clignoter_bouton_erreur()
        btn_lancer.configure(state="normal", text="RÉESSAYER")
        return

    time.sleep(8)
    
    update_log("[*] Injection du script MAZZ...")
    coller_script(SCRIPT_LUA, update_log, "Menu MAZZ (loadstring)")

    update_log("\n[+] TERMINÉ ! Clique sur Attach et Execute dans Xeno.")
    animer_progression(False)
    btn_lancer.configure(state="normal", text="RELANCER LE CHEAT", fg_color="#28a745")

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("450x480")
app.title("MAZZ LOADER")
app.configure(fg_color="#0d0d0d")
app.resizable(False, False)
app.withdraw()

try:
    icon_png = resource_path("mazz.png")
    icon_ico = resource_path("mazz.ico")
    if os.path.exists(icon_png):
        img = tk.PhotoImage(file=icon_png)
        app.iconphoto(True, img)
    elif os.path.exists(icon_ico):
        app.iconbitmap(icon_ico)
except Exception:
    pass

lbl_titre = ctk.CTkLabel(app, text="! Bagdad", font=("Consolas", 45, "bold", "italic"), text_color="#0F2D5A")
lbl_sous_titre = ctk.CTkLabel(app, text="EXTERNAL LOADER V2.6", font=("Consolas", 12), text_color="#555555")

btn_lancer = ctk.CTkButton(app, text="LANCER LE CHEAT", font=("Consolas", 16, "bold"),
                           fg_color="#FF003C", hover_color="#cc002f", text_color="#ffffff",
                           height=50, corner_radius=8,
                           command=lambda: threading.Thread(target=lancer_cheat, daemon=True).start())
btn_lancer.bind("<Enter>", animer_bouton_survol)
btn_lancer.bind("<Leave>", animer_bouton_sortie)

barre_progression = ctk.CTkProgressBar(app, height=6, corner_radius=3,
                                       fg_color="#222222", progress_color="#FF003C",
                                       mode="indeterminate")

log = ctk.CTkTextbox(app, font=("Consolas", 11), fg_color="#000000", text_color="#00FF00", corner_radius=8)
log.insert("end", "En attente du lancement...\n")
log.configure(state="disabled")

lbl_titre.pack(pady=(15, 0))
lbl_sous_titre.pack(pady=(0, 20))
btn_lancer.pack(pady=10, padx=40, fill="x")
log.pack(pady=10, padx=40, fill="both", expand=True)

app.after(100, lancer_animation_bagdad)
app.after(3500, pulsation_titre) 

app.mainloop()
