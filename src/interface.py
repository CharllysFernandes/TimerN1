import tkinter as tk
from datetime import datetime, timedelta
from threading import Thread

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Controles de Jornada e Pausas N1")

        self.label_tempo = tk.Label(root, text="00:00:00", font=("Helvetica", 24))
        self.label_tempo.pack(pady=20)

        self.iniciar_btn = tk.Button(root, text="Iniciar", command=self.iniciar_cronometro)
        self.iniciar_btn.pack(pady=10)

        self.encerrar_btn = tk.Button(root, text="Encerrar", command=self.encerrar_cronometro, state=tk.DISABLED)
        self.encerrar_btn.pack(pady=10)

        self.tempo_inicial = None
        self.atualizando = False

    def iniciar_cronometro(self):
        if not self.atualizando:
            self.tempo_inicial = datetime.now()
            self.iniciar_cronometro_thread()

    def encerrar_cronometro(self):
        self.atualizando = False
        self.iniciar_btn["state"] = tk.NORMAL
        self.encerrar_btn["state"] = tk.DISABLED

    def atualizar_cronometro(self):
        if self.atualizando:
            tempo_atual = datetime.now() - self.tempo_inicial if self.tempo_inicial else timedelta(seconds=0)
            tempo_formatado = "{:02}:{:02}:{:02}".format(
                tempo_atual.seconds // 3600, (tempo_atual.seconds // 60) % 60, tempo_atual.seconds % 60
            )
            self.label_tempo.config(text=tempo_formatado)
            self.root.after(1000, self.atualizar_cronometro)

    def iniciar_cronometro_thread(self):  # Renomeado corretamente para iniciar_cronometro_thread
        self.atualizando = True
        self.iniciar_btn["state"] = tk.DISABLED
        self.encerrar_btn["state"] = tk.NORMAL
        self.iniciar_cronometro_thread = Thread(target=self.atualizar_cronometro)
        self.iniciar_cronometro_thread.start()

