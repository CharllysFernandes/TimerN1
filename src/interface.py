import tkinter as tk
from src.controle import Controle

class Interface:
    def __init__(self, root):
        self.root = root
        self.controle = Controle(self)

        self.root.title("Controles de Jornada e Pausas N1")

        self.label_tempo = tk.Label(root, text="00:00:00", font=("Helvetica", 24))
        self.label_tempo.pack(pady=20)

        botoes_frame = tk.Frame(root)
        botoes_frame.pack(pady=10)

        self.iniciar_btn = tk.Button(botoes_frame, text="Iniciar", command=self.controle.iniciar_cronometro)
        self.iniciar_btn.grid(row=0, column=0, padx=5)

        self.encerrar_btn = tk.Button(botoes_frame, text="Encerrar", command=self.controle.encerrar_cronometro)
        self.encerrar_btn.grid(row=0, column=1, padx=5)

        pausas_frame = tk.Frame(root)
        pausas_frame.pack(pady=10)

        self.pausa_10_btn = tk.Button(pausas_frame, text="Pausa 10", command=lambda: self.controle.iniciar_contagem_pausa(self.pausa_10_btn, 10*60))
        self.pausa_10_btn.grid(row=0, column=0, padx=5)

        self.pausa_20_btn = tk.Button(pausas_frame, text="Pausa 20", command=lambda: self.controle.iniciar_contagem_pausa(self.pausa_20_btn, 20*60))
        self.pausa_20_btn.grid(row=0, column=1, padx=5)

        self.pausa_10_2_btn = tk.Button(pausas_frame, text="Pausa 10", command=lambda: self.controle.iniciar_contagem_pausa(self.pausa_10_2_btn, 10*60))
        self.pausa_10_2_btn.grid(row=0, column=2, padx=5)
        
        self.pausa_10_HE_btn = tk.Button(pausas_frame, text="Pausa 10 HE", command=lambda: self.controle.iniciar_contagem_pausa(self.pausa_10_HE_btn, 10*60))
        self.pausa_10_HE_btn.grid(row=0, column=3, padx=5)