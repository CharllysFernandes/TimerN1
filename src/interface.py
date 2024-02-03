import tkinter as tk
from datetime import datetime, timedelta
from threading import Thread

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Controles de Jornada e Pausas N1")

        self.label_tempo = tk.Label(root, text="00:00:00", font=("Helvetica", 24))
        self.label_tempo.pack(pady=20)

        botoes_frame = tk.Frame(root)
        botoes_frame.pack(pady=10)

        self.iniciar_btn = tk.Button(botoes_frame, text="Iniciar", command=self.iniciar_cronometro)
        self.iniciar_btn.grid(row=0, column=0, padx=5)

        self.encerrar_btn = tk.Button(botoes_frame, text="Encerrar", command=self.encerrar_cronometro, state=tk.DISABLED)
        self.encerrar_btn.grid(row=0, column=1, padx=5)

        pausas_frame = tk.Frame(root)
        pausas_frame.pack(pady=10)

        self.pausa_10_btn = tk.Button(pausas_frame, text="Pausa 10", command=self.registrar_pausa_10)
        self.pausa_10_btn.grid(row=0, column=0, padx=5)

        self.pausa_20_btn = tk.Button(pausas_frame, text="Pausa 20", command=self.registrar_pausa_20)
        self.pausa_20_btn.grid(row=0, column=1, padx=5)

        self.pausa_10_2_btn = tk.Button(pausas_frame, text="Pausa 10", command=self.registrar_pausa_10_2)
        self.pausa_10_2_btn.grid(row=0, column=2, padx=5)

        self.pausa_10_he_btn = tk.Button(pausas_frame, text="Pausa 10 HE", command=self.registrar_pausa_10_he)
        self.pausa_10_he_btn.grid(row=0, column=3, padx=5)

        self.tempo_inicial = None
        self.atualizando = False
        self.thread_cronometro = None

    def iniciar_cronometro(self):
        if not self.atualizando:
            self.tempo_inicial = datetime.now()
            self.iniciar_cronometro_thread()

    def encerrar_cronometro(self):
        self.atualizando = False
        if self.thread_cronometro is not None:
            self.thread_cronometro.join()  # Aguarda a finalização da thread
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

    def iniciar_cronometro_thread(self):
        self.atualizando = True
        self.iniciar_btn["state"] = tk.DISABLED
        self.encerrar_btn["state"] = tk.NORMAL
        self.thread_cronometro = Thread(target=self.atualizar_cronometro)
        self.thread_cronometro.daemon = True  # Define a thread como "daemon"
        self.thread_cronometro.start()

    def registrar_pausa_10(self):
        # Lógica para registrar pausa de 10 minutos
        pass

    def registrar_pausa_10_2(self):
        # Lógica para registrar pausa de 10 minutos
        pass

    def registrar_pausa_20(self):
        # Lógica para registrar pausa de 20 minutos
        pass

    def registrar_pausa_10_he(self):
        # Lógica para registrar pausa de 10 minutos (HE)
        pass
