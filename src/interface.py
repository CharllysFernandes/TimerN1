import tkinter as tk
from datetime import timedelta
from registro import RegistroHoras

class Interface:
    def __init__(self, root, registro_horas):
        self.root = root
        self.registro_horas = registro_horas
        self.is_trabalho_iniciado = False

        self.root.title("Folha de Ponto")

        # Adiciona o texto "Folha de Ponto" acima do display
        self.texto_label = tk.Label(root, text="Folha de Ponto", font=("Helvetica", 16))
        self.texto_label.grid(row=0, column=0, pady=10, columnspan=4)  # columnspan para estender sobre as 4 colunas

        self.iniciar_button = tk.Button(root, text="Iniciar", command=self.toggle_trabalho)
        self.iniciar_button.grid(row=1, column=0, pady=5, padx=5, columnspan=4)

        self.pausa_10_button = tk.Button(root, text="Iniciar Pausa 10", command=lambda: self.registrar_pausa(10))
        self.pausa_10_button.grid(row=2, column=0, padx=5, pady=10)

        self.pausa_20_button = tk.Button(root, text="Iniciar Pausa 20", command=lambda: self.registrar_pausa(20))
        self.pausa_20_button.grid(row=2, column=1, padx=5, pady=10)

        self.pausa_30_button = tk.Button(root, text="Iniciar Pausa 30", command=lambda: self.registrar_pausa(30))
        self.pausa_30_button.grid(row=2, column=2, padx=5, pady=10)

        self.pausa_10_he_button = tk.Button(root, text="Iniciar Pausa 10 HE", command=lambda: self.registrar_pausa_he(10))
        self.pausa_10_he_button.grid(row=2, column=3, padx=5, pady=10)

        self.atualizar_display()

    def iniciar_trabalho(self):
        self.registro_horas.iniciar_trabalho()
        self.atualizar_display()

    def registrar_pausa(self, minutos):
        self.registro_horas.registrar_pausa(minutos)
        self.atualizar_display()

    def registrar_pausa_he(self, minutos):
        self.registro_horas.registrar_pausa_he(minutos)
        self.atualizar_display()

    def atualizar_display(self):
        tempo_formatado = self.registro_horas.obter_tempo_formatado()
        self.texto_label.config(text=f"Folha de Ponto - {tempo_formatado}")

    def toggle_trabalho(self):
        if not self.is_trabalho_iniciado:
            self.registro_horas.iniciar_trabalho()
            self.is_trabalho_iniciado = True
            self.iniciar_button.config(text="Encerrar")
        else:
            self.registro_horas.encerrar_trabalho()
            self.is_trabalho_iniciado = False
            self.iniciar_button.config(text="Iniciar")

        self.atualizar_display()