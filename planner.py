import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
import json

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas relativas
CHAR_PATH = os.path.join(BASE_DIR, "_Assets", "Engage characters")
EMBLEM_PATH = os.path.join(BASE_DIR, "_Assets", "Emblems")
ENGRAVE_PATH = os.path.join(BASE_DIR, "_Assets", "Engraves")

# ================= Constantes =================
CHARACTERS = ["alear", "alcryst", "alfred", "amber", "anna", "boucheron", "celine", "chloe", "citrinne",
              "clanne", "diamant", "etie", "fogado", "framme", "goldmary", "gregory", "hortensia",
              "ivy", "jade", "jean", "kagetsu", "lapis","louis", "lindon", "madeline", "mauvier",
              "merrin", "nel", "pandreo", "pannette", "rafal", "rosado", "saphir", "seadall",
              "timerra", "veyle", "yunaka", "zelestia", "zelkov"]

EMBLEMS = ["Marth", "Celica", "Sigurd", "Leif", "Roy", "Lyn", "Eirika", "Ike",
           "Micaiah", "Lucina", "Corrin", "Byleth", "Tiki", "Edelgard", "Camilla",
           "Soren", "Hector", "Chrom", "Veronica"]

ENGRAVES = EMBLEMS + ["Alear"]

def check_images(folder, names):
    print(f"\n🔍 Revisando carpeta: {folder}")
    found = set(os.listdir(folder))
    found_lower = {f.lower() for f in found}

    for name in names:
        expected = f"{name}.png"
        if expected.lower() in found_lower:
            print(f"✅ {expected} encontrado")
        else:
            matches = [f for f in found if f.lower().startswith(name.lower())]
            if matches:
                print(f"⚠️ {expected} no coincide exactamente, pero encontré: {matches}")
            else:
                print(f"❌ Falta: {expected}")

check_images(EMBLEM_PATH, EMBLEMS)
check_images(ENGRAVE_PATH, ENGRAVES)


BG_COLOR = "#081422"
TEXT_COLOR = "#f0f0f0"

class CharacterSlot:
    def __init__(self, parent, row, portrait_path, emblem_path, engrave_path,
                 characters, emblems, engraves, used_engravings, force_alear=False):
        self.used_engravings = used_engravings
        self.current_engrave = None
        self.char_path = portrait_path
        self.emblem_path = emblem_path
        self.engrave_path = engrave_path

        outer = tk.Frame(parent, bg='#081422')
        outer.grid(row=row, column=0, padx=20, pady=10, sticky='ew')
        for col in range(4):
            outer.columnconfigure(col, weight=1)

        self.selected_char = tk.StringVar()
        self.char_dropdown = ttk.Combobox(
            outer, textvariable=self.selected_char,
            values=characters, state='readonly', width=18
        )
        self.char_dropdown.grid(row=0, column=0, padx=6, pady=4)

        # Emblem
        self.selected_emblem = tk.StringVar()
        self.emblem_dropdown = ttk.Combobox(
            outer, textvariable=self.selected_emblem,
            values=emblems, state='readonly', width=18
        )
        self.emblem_dropdown.grid(row=0, column=1, padx=6, pady=4)

        # Engrave
        self.engrave_options = engraves
        self.selected_engrave = tk.StringVar()
        self.engrave_dropdown = ttk.Combobox(
            outer, textvariable=self.selected_engrave,
            values=self.engrave_options, state='readonly', width=18
        )
        self.engrave_dropdown.grid(row=0, column=2, padx=6, pady=4)
        self.engrave_dropdown.set('Select Engrave')
        self.engrave_dropdown.bind('<<ComboboxSelected>>', self.validate_engrave)

        # Weapon label
        weapon_label = tk.Label(outer, text='Weapon:', bg='#081422', fg=TEXT_COLOR)
        weapon_label.grid(row=0, column=3, sticky='w', padx=6, pady=4)

        class_label = tk.Label(outer, text='Class:', bg='#081422', fg=TEXT_COLOR)
        class_label.grid(row=0, column=4, sticky='w', padx=6, pady=4)

        ability1_label = tk.Label(outer, text='Ability 1:', bg='#081422', fg=TEXT_COLOR)
        ability1_label.grid(row=0, column=5, sticky='w', padx=6, pady=4)

        ability2_label = tk.Label(outer, text='Ability 2:', bg='#081422', fg=TEXT_COLOR)
        ability2_label.grid(row=0, column=6, sticky='w', padx=6, pady=4)

        self.char_portrait_label = tk.Label(outer, bg='#081422')
        self.char_portrait_label.grid(row=1, column=0, padx=6, pady=6)

        self.emblem_portrait_label = tk.Label(outer, bg='#081422')
        self.emblem_portrait_label.grid(row=1, column=1, padx=6, pady=6)

        self.engrave_portrait_label = tk.Label(outer, bg='#081422')
        self.engrave_portrait_label.grid(row=1, column=2, padx=6, pady=6)

        self.weapon_entry = ttk.Entry(outer, width=15)
        self.weapon_entry.grid(row=1, column=3, padx=6, pady=6)

        self.class_entry = ttk.Entry(outer, width=15)
        self.class_entry.grid(row=1, column=4, padx=6, pady=6)

        self.ability1_entry = ttk.Entry(outer, width=15)
        self.ability1_entry.grid(row=1, column=5, padx=6, pady=6)

        self.ability2_entry = ttk.Entry(outer, width=15)
        self.ability2_entry.grid(row=1, column=6, padx=6, pady=6)


        self.error_label = tk.Label(outer, text='', fg='#ff6b6b', bg='#081422')
        self.error_label.grid(row=2, column=0, columnspan=4, sticky='w', padx=8, pady=2)

        self.char_dropdown.bind('<<ComboboxSelected>>', self.update_char_portrait)
        self.emblem_dropdown.bind('<<ComboboxSelected>>', self.update_emblem_portrait)

        if force_alear:
            self.selected_char.set('alear')
            self.update_char_portrait()  # carga imagen
            self.char_dropdown.config(state='disabled')
        else:
            self.char_dropdown.set('Select Character')
        self.emblem_dropdown.set('Select Emblem')

    def validate_engrave(self, event=None):
        choice = self.selected_engrave.get()
        if choice in self.used_engravings:
            self.error_label.config(text=f"Engrave '{choice}' is already used!")
            self.selected_engrave.set('Select Engrave')
        else:
            if self.current_engrave:
                self.used_engravings.remove(self.current_engrave)
            self.used_engravings.add(choice)
            self.current_engrave = choice
            self.error_label.config(text='')
            self.update_engrave_portrait(choice)

    def update_char_portrait(self, event=None):
        char_name = self.selected_char.get()
        if char_name and char_name != "Select Character":
            img_path = None
            for ext in [".png", ".jpg", ".jpeg"]:
                test_path = os.path.join(self.char_path, f"{char_name}{ext}")
                if os.path.exists(test_path):
                    img_path = test_path
                    break

            print(f"[DEBUG] Buscando imagen en: {img_path}")
            print(f"[DEBUG] Existe? {os.path.exists(img_path) if img_path else False}")

            if img_path:
                try:
                    img = Image.open(img_path).resize((100, 100), Image.Resampling.LANCZOS)
                    self.char_img = ImageTk.PhotoImage(img)
                    self.char_portrait_label.config(image=self.char_img, text='')
                except Exception as e:
                    print(f"[ERROR] Falló al abrir imagen: {e}")
                    self.char_portrait_label.config(image='', text='[Error]', fg='red', bg='#081422')
            else:
                self.char_portrait_label.config(image='', text='[No Image]', fg='red', bg='#081422')
        else:
            self.char_portrait_label.config(image='', text='')


    def update_emblem_portrait(self, event=None):
        emblem_name = self.selected_emblem.get()
        if emblem_name and emblem_name != "Select Emblem":
            img_path = None
            for ext in [".png", ".jpg", ".jpeg"]:
                test_path = os.path.join(self.emblem_path, f"{emblem_name}{ext}")
                if os.path.exists(test_path):
                    img_path = test_path
                    break
            if img_path:
                try:
                    img = Image.open(img_path).resize((100, 100), Image.Resampling.LANCZOS)
                    self.emblem_img = ImageTk.PhotoImage(img)  # referencia viva
                    self.emblem_portrait_label.config(image=self.emblem_img, text='')
                except Exception as e:
                    print(f"[ERROR] Falló al abrir imagen: {e}")
                    self.emblem_portrait_label.config(image='', text='[Error]', fg='red', bg='#081422')
            else:
                self.emblem_portrait_label.config(image='', text='[No Image]', fg='red', bg='#081422')
        else:
            self.emblem_portrait_label.config(image='', text='')
        
    def update_engrave_portrait(self, engrave_name=None):
        name = engrave_name if engrave_name else self.selected_engrave.get()
        if name and name != "Select Engrave":
            img_path = None
            for ext in [".png", ".jpg", ".jpeg"]:
                test_path = os.path.join(self.engrave_path, f"{name}{ext}")
                if os.path.exists(test_path):
                    img_path = test_path
                    break

            if img_path:
                try:
                    img = Image.open(img_path).resize((100, 100), Image.Resampling.LANCZOS)
                    self.engrave_img = ImageTk.PhotoImage(img)
                    self.engrave_portrait_label.config(image=self.engrave_img, text='')
                except Exception as e:
                    print(f"[ERROR] Falló al abrir imagen: {e}")
                    self.engrave_portrait_label.config(image='', text='[Error]', fg='red', bg='#081422')
            else:
                self.engrave_portrait_label.config(image='', text='[No Image]', fg='red', bg='#081422')
        else:
            self.engrave_portrait_label.config(image='', text='')

root = tk.Tk()
root.title("Character Selector")
root.geometry("950x700")
root.configure(bg=BG_COLOR)

# ==== Canvas con scrollbar ====
canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ==== Slots ====
used_engravings = set()
slots = []

for i in range(14):
    force_alear = (i == 0)
    slot = CharacterSlot(
    scrollable_frame, i,
    CHAR_PATH, EMBLEM_PATH, ENGRAVE_PATH,
    CHARACTERS, EMBLEMS, ENGRAVES,
    used_engravings,
    force_alear=force_alear
)
    slots.append(slot)

SAVE_FILE = os.path.join(BASE_DIR, "save.json")

def save_progress():
    data = []
    for slot in slots:
        data.append({
            "character": slot.selected_char.get(),
            "emblem": slot.selected_emblem.get(),
            "engrave": slot.selected_engrave.get(),
            "weapon": slot.weapon_entry.get(),
            "class": slot.class_entry.get(),
            "ability1": slot.ability1_entry.get(),
            "ability2": slot.ability2_entry.get()
        })
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("✅ Progreso guardado en", SAVE_FILE)

def load_progress():
    if not os.path.exists(SAVE_FILE):
        print("⚠️ No hay archivo de guardado")
        return
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for slot, saved in zip(slots, data):
        if saved["character"] in CHARACTERS:
            slot.selected_char.set(saved["character"])
            slot.update_char_portrait()
        if saved["emblem"] in EMBLEMS:
            slot.selected_emblem.set(saved["emblem"])
            slot.update_emblem_portrait()
        if saved["engrave"] in ENGRAVES:
            slot.selected_engrave.set(saved["engrave"])
            slot.update_engrave_portrait()
        # Weapon
        slot.weapon_entry.delete(0, tk.END)
        slot.weapon_entry.insert(0, saved.get("weapon", ""))

        # Class
        slot.class_entry.delete(0, tk.END)
        slot.class_entry.insert(0, saved.get("class", ""))

        # Ability 1
        slot.ability1_entry.delete(0, tk.END)
        slot.ability1_entry.insert(0, saved.get("ability1", ""))

        # Ability 2
        slot.ability2_entry.delete(0, tk.END)
        slot.ability2_entry.insert(0, saved.get("ability2", ""))

# ==== Botones Guardar / Cargar ====
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

save_btn = ttk.Button(btn_frame, text="Guardar Progreso", command=save_progress)
save_btn.pack(side="left", padx=10)

load_btn = ttk.Button(btn_frame, text="Cargar Progreso", command=load_progress)
load_btn.pack(side="left", padx=10)


root.mainloop()


