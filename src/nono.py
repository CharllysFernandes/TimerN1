# interface.py
import tkinter as tk
from datetime import datetime, timedelta, time
from threading import Thread

class Interface:
    def __init__(self, root):
        self.root = root
        self.atualizando = False
        self.atualizando_pausa = False

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

        self.pausa_10_btn = tk.Button(pausas_frame, text="Pausa 10", command=lambda: self.iniciar_contagem_pausa(self.pausa_10_btn, 10*60))
        self.pausa_10_btn.grid(row=0, column=0, padx=5)

        self.pausa_20_btn = tk.Button(pausas_frame, text="Pausa 20", command=lambda: self.iniciar_contagem_pausa(self.pausa_20_btn, 20*60))
        self.pausa_20_btn.grid(row=0, column=1, padx=5)

        self.pausa_10_2_btn = tk.Button(pausas_frame, text="Pausa 10", command= lambda: self.iniciar_contagem_pausa(self.pausa_10_2_btn, 10*60))
        self.pausa_10_2_btn.grid(row=0, column=2, padx=5)

        self.pausa_10_he_btn = tk.Button(pausas_frame, text="Pausa 10 HE", command=lambda: self.iniciar_contagem_pausa(self.pausa_10_he_btn, 10*60)) #Pausa 10
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


    def iniciar_contagem_pausa(self, botao, tempo):
        if not self.atualizando_pausa:
            self.atualizando_pausa = True
            self.atualizar_contagem_regressiva(botao, tempo)
            self.registrar_pausa(botao, tempo)
        else:
            self.atualizando_pausa = False
            botao.config(text="Pausa 10 HE")
            botao.config(state="disabled")
            self.registrar_pausa(botao, tempo)

    def atualizar_contagem_regressiva(self, botao, tempo_em_segundos_pausa):
        if self.atualizando_pausa:
            minutos, segundos = divmod(abs(tempo_em_segundos_pausa), 60)
            sinal = "+" if tempo_em_segundos_pausa < 0 else "-"
            tempo_formatado = "{}{:02}:{:02}".format(sinal, minutos, segundos)

            # Mudar a cor do texto com base na condição
            cor_texto = "blue" if tempo_em_segundos_pausa >= 0 else "red"

            botao.config(text="Encerrar ({})".format(tempo_formatado), fg=cor_texto)
            tempo_em_segundos_pausa -= 1 if tempo_em_segundos_pausa >= 0 else +1 
            self.root.after(1000, lambda: self.atualizar_contagem_regressiva(botao, tempo_em_segundos_pausa))

    def registrar_pausa(self, botao, tempo_pausa):
        if not self.atualizando_pausa:
            agora = datetime.now()
            self.criar_log("<<-- Retorno de Pausa {}: {}".format(int(tempo_pausa/60), agora.strftime("%Y-%m-%d %H:%M")))
            self.atualizando_pausa = False
            self.atualizar_contagem_regressiva(botao, tempo_pausa)
        else:
            self.atualizando_pausa = True
            agora = datetime.now()
            self.criar_log("-->> Inicio de Pausa {}: {}".format(int(tempo_pausa/60), agora.strftime("%Y-%m-%d %H:%M")))