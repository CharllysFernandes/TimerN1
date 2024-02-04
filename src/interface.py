import tkinter as tk
from datetime import datetime, timedelta, time
from threading import Thread

class Interface:
    def __init__(self, root):
        self.root = root

        self.tempo_pausa_10 = 10
        self.tempo_pausa_20 = 20

        self.atualizando = False

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

        self.pausa_10_btn = tk.Button(pausas_frame, text="Pausa 10")
        self.pausa_10_btn.grid(row=0, column=0, padx=5)

        self.pausa_20_btn = tk.Button(pausas_frame, text="Pausa 20")
        self.pausa_20_btn.grid(row=0, column=1, padx=5)

        self.pausa_10_2_btn = tk.Button(pausas_frame, text="Pausa 10")
        self.pausa_10_2_btn.grid(row=0, column=2, padx=5)

        self.pausa_10_he_btn = tk.Button(pausas_frame, text="Pausa 10 HE", command=lambda: self.iniciar_contagem_pausa(self.pausa_10_he_btn))
        self.pausa_10_he_btn.grid(row=0, column=3, padx=5)

        self.tempo_inicial = None
        self.atualizando = False
        self.thread_cronometro = None

    def iniciar_cronometro(self):
        if not self.atualizando:
            agora = datetime.now()
            if self.tempo_inicial is not None and agora.date() == self.tempo_inicial.date():
                # Continua de onde parou no mesmo dia
                tempo_passado = agora - self.tempo_inicial
            else:
                # Começa do zero em outro dia
                tempo_passado = timedelta(seconds=0)
                self.tempo_inicial = agora
            self.tempo_inicial -= tempo_passado  # Ajusta o tempo inicial
            self.iniciar_cronometro_thread()
            self.criar_log("\n"+ "________________" + "\n" + "Início de trabalho: {}".format(self.tempo_inicial.strftime("%Y-%m-%d %H:%M")))

    def encerrar_cronometro(self):
        self.atualizando = False
        hora_encerramento = datetime.now()
        tempo_trabalhado = hora_encerramento - self.tempo_inicial
        tempo_formatado = "{:02}:{:02}:{:02}".format(
            tempo_trabalhado.seconds // 3600, (tempo_trabalhado.seconds // 60) % 60, tempo_trabalhado.seconds % 60
        )
        mensagem = "Encerramento de trabalho: {}\nTotal de horas trabalhadas: {}".format(
            hora_encerramento.strftime("%Y-%m-%d %H:%M"), tempo_formatado
        )
        self.criar_log(mensagem)
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

    def criar_log(self, mensagem):
        with open("Log.txt", "a") as arquivo_log:
            arquivo_log.write(mensagem + "\n")


    def iniciar_contagem_pausa(self, botao):
        if not self.atualizando:
            self.atualizando = True
            self.atualizar_contagem_regressiva(botao)
        else:
            self.atualizando = False
            botao.config(text="Pausa 10 HE")
            botao.config(state="disabled")

    def atualizar_contagem_regressiva(self, botao):
        if self.atualizando:
            minutos, segundos = divmod(abs(self.tempo_pausa_10), 60)
            sinal = "+" if self.tempo_pausa_10 < 0 else "-"
            tempo_formatado = "{}{:02}:{:02}".format(sinal, minutos, segundos)
            botao.config(text="Encerrar ({})".format(tempo_formatado))
            self.tempo_pausa_10 -= 1 if self.tempo_pausa_10 >= 0 else +1
            self.root.after(1000, lambda: self.atualizar_contagem_regressiva(botao))
