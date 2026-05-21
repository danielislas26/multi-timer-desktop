import customtkinter 
import os
import tkinter.font
import time



directorio_actual = os.path.dirname(os.path.abspath(__file__))

ruta_regular = os.path.join(directorio_actual, "..", "assets", "fonts", "ShareTechMono-Regular.ttf")
ruta_semibold = os.path.join(directorio_actual, "..", "assets", "fonts", "Orbitron-SemiBold.ttf")

ruta_digit = os.path.join(directorio_actual, "..", "assets", "fonts", "DS-DIGI.TTF")
ruta_digitbold = os.path.join(directorio_actual, "..", "assets", "fonts", "DS-DIGIB.TTF")

customtkinter.FontManager.load_font(ruta_regular)
customtkinter.FontManager.load_font(ruta_semibold)
customtkinter.FontManager.load_font(ruta_digit)
customtkinter.FontManager.load_font(ruta_digitbold)

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.digitos = ""
        self.configure(fg_color="#222831")
        self.geometry("250x250")
        self.title("Cronometro")

        mi_fuente_digital = customtkinter.CTkFont(family="Share Tech Mono", size=17)
        mi_fuente_numeral = customtkinter.CTkFont(family="DS-Digital", size=20, weight="bold")
        print([f for f in tkinter.font.families() if "Share" in f])

        self.entry_1 = customtkinter.CTkEntry(
            self, border_width=0, fg_color="transparent",
            justify="center", font=mi_fuente_digital, placeholder_text="coding"
        )
        self.entry_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.entry_1.bind("<KeyRelease>", self.on_key_release)
 
        self.time_1entry = customtkinter.CTkEntry(
            self, border_width=0, fg_color="transparent",
            justify="center", font=mi_fuente_numeral, placeholder_text="00:00:00"
        )
       
        
        self.time_1entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.time_1entry.bind("<KeyRelease>", self.formatear_tiempo)
        self.time_1entry.bind("<Key>", self.formatear_tiempo)

        self.button = customtkinter.CTkButton(
            self, text="play", command=self.button_click,
            fg_color=("#285A48", "#285A48"), hover_color="#1e4437",
            border_color="#B0E4CC", border_width=2, text_color="#E2DFD0",
            font=("Ubuntu", 17, "bold"), height=35, state="disabled"
        )
        self.button.grid(row=2, column=0, padx=20, pady=10) 

        self.timer = customtkinter.CTkLabel(self, font=mi_fuente_numeral, text="00:00")
        self.timer.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.toplevel_window = None
        self.tiempo_restante = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Para centrar verticalmente
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def get_time(self):

        time_text = self.time_1entry.get()

        try:
            horas, minutos, segundos = map(int, time_text.split(":"))

            self.tiempo_restante = (
                horas * 3600 +
                minutos * 60 +
                segundos
            )

            self.actualizar_timer()

        except:
            print("Formato inválido")
        
    def formatear_tiempo(self, event):

        tecla = event.keysym

        # Backspace
        if tecla == "BackSpace":
            self.digitos = self.digitos[:-1]

        # Solo números
        elif event.char.isdigit():

            # Máximo 6 dígitos
            if len(self.digitos) < 6:
                self.digitos += event.char

        else:
            return

        # Rellenar con ceros
        texto = self.digitos.zfill(6)

        horas = texto[:2]
        minutos = texto[2:4]
        segundos = texto[4:6]

        resultado = f"{horas}:{minutos}:{segundos}"

        self.time_1entry.delete(0, "end")
        self.time_1entry.insert(0, resultado)

        self.time_1entry.icursor("end")

        self.check_entry()
        return "break"

    def actualizar_timer(self):
        if self.tiempo_restante > 0:
            horas = self.tiempo_restante // 3600
            minutos = (self.tiempo_restante % 3600) // 60
            segundos = self.tiempo_restante % 60

            texto_timer = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            self.timer.configure(text=texto_timer)
            self.tiempo_restante -= 1
            self.after(1000, self.actualizar_timer)
        else:
            self.timer.configure(text="¡Tiempo completado!")
            self.button.configure(state="normal")

    def abrir_popup(self):
        ventana_emergente = customtkinter.CTkToplevel(self)
        ventana_emergente.title("Mi Popup")
        ventana_emergente.geometry("400x300")

    def on_key_release(self, event):
        self.check_entry()

    

    def check_entry(self):
        title_text = self.entry_1.get()
        time_text = self.time_1entry.get()
        print(f"title: '{title_text}'")
        print(f"time: '{time_text}'")
        
        if len(title_text) == 0 or len(time_text) == 0:
            self.button.configure(state="disabled")
            print("Uno o más campos vacíos")
        elif title_text.strip() == "" or time_text.strip() == "":
            self.button.configure(state="disabled")
            print("Solo espacios")
        else:
            numeros = time_text.replace(":", "")
            if not numeros.isdigit() or int(numeros) == 0:
                print("no es digito")
                self.button.configure(state="disabled")
            else:
                self.button.configure(state="normal")
                print("Ambos campos tienen texto válido")

    def button_click(self):

        self.button.configure(state="disabled")

        self.get_time()

        data = {
            "task_1": self.entry_1.get(),
        }

app = App()
app.mainloop()