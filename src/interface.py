import tkinter as tk
from datetime import timedelta
from registro import RegistroHoras

class Interface:
    def __init__(self, root, registro_horas):
        self.root = root
        self.registro_horas = registro_horas

        self.root.title("Registro de Horas")

        # Adiciona o texto "Horas trabalhadas" acima do display
        self.texto_label = tk.Label(root, text="Horas Trabalhadas", font=("Helvetica", 14))
        self.texto_label.pack(pady=5)

        self.total_horas_label = tk.Label(root, text="00:00:00", font=("Helvetica", 16), fg="green", bg="black")
        self.total_horas_label.pack(pady=10)

        self.iniciar_button = tk.Button(root, text="Iniciar Trabalho", command=self.iniciar_trabalho)
        self.iniciar_button.pack(pady=5)

        self.encerrar_button = tk.Button(root, text="Encerrar Trabalho", command=self.encerrar_trabalho, state=tk.DISABLED)
        self.encerrar_button.pack(pady=5)

        self.pausa_10_button = tk.Button(root, text="Pausa 10 Min", command=lambda: self.registrar_pausa(10))
        self.pausa_10_button.pack(side=tk.LEFT, padx=5)

        self.pausa_20_button = tk.Button(root, text="Pausa 20 Min", command=lambda: self.registrar_pausa(20))
        self.pausa_20_button.pack(side=tk.LEFT, padx=5)

        self.pausa_30_button = tk.Button(root, text="Pausa 30 Min", command=lambda: self.registrar_pausa(30))
        self.pausa_30_button.pack(side=tk.LEFT, padx=5)

        self.atualizar_display()

    def iniciar_trabalho(self):
        self.registro_horas.iniciar_trabalho()
        self.atualizar_display()

    def encerrar_trabalho(self):
        self.registro_horas.encerrar_trabalho()
        self.atualizar_display()

    def registrar_pausa(self, minutos):
        self.registro_horas.registrar_pausa(minutos)
        self.atualizar_display()

    def atualizar_display(self):
        tempo_formatado = self.registro_horas.obter_tempo_formatado()
        self.total_horas_label.config(text=f"Total de Horas: {tempo_formatado}")
