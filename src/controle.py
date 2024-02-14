import time
from threading import Thread
from datetime import timedelta, datetime
from src.manipulacao_dados import ManipuladorDados

class Controle:
    def __init__(self, interface):
        self.interface = interface
        self.atualizando = False
        self.atualizando_pausa = False
        self.tempo_inicial = None
        self.thread_cronometro = None
        self.manipulador_dados = ManipuladorDados()

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
            mensagem = "Início de trabalho: {}".format(self.tempo_inicial.strftime("%Y-%m-%d %H:%M"))
            self.manipulador_dados.criar_log(mensagem)

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
        self.manipulador_dados.criar_log(mensagem)
        if self.thread_cronometro is not None:
            self.thread_cronometro.join()  # Aguarda a finalização da thread

    def iniciar_cronometro_thread(self):
        self.atualizando = True
        self.thread_cronometro = Thread(target=self.atualizar_cronometro)
        self.thread_cronometro.daemon = True  # Define a thread como "daemon"
        self.thread_cronometro.start()

    def atualizar_cronometro(self):
        while self.atualizando:
            tempo_atual = datetime.now() - self.tempo_inicial if self.tempo_inicial else timedelta(seconds=0)
            tempo_formatado = "{:02}:{:02}:{:02}".format(
                tempo_atual.seconds // 3600, (tempo_atual.seconds // 60) % 60, tempo_atual.seconds % 60
            )
            self.interface.label_tempo.config(text=tempo_formatado)
            # Atualizar a cada segundo
            time.sleep(1)

    def atualizar_contagem_regressiva(self, botao, tempo_em_segundos_pausa):
        if self.atualizando_pausa:
            minutos, segundos = divmod(abs(tempo_em_segundos_pausa), 60)
            sinal = "+" if tempo_em_segundos_pausa < 0 else "-"
            tempo_formatado = "{}{:02}:{:02}".format(sinal, minutos, segundos)

            # Mudar a cor do texto com base na condição
            cor_texto = "blue" if tempo_em_segundos_pausa >= 0 else "red"

            botao.config(text="Encerrar ({})".format(tempo_formatado), fg=cor_texto)
            tempo_em_segundos_pausa -= 1 if tempo_em_segundos_pausa >= 0 else +1 
            self.interface.after(1000, lambda: self.atualizar_contagem_regressiva(botao, tempo_em_segundos_pausa))

    # def iniciar_contagem_pausa(self, tempo_pausa):
    #     agora = datetime.now()
    #     self.manipulador_dados.registrar_pausa(agora, tempo_pausa)

    def iniciar_contagem_pausa(self, botao, tempo):
        agora = datetime.now()
        if not self.atualizando_pausa:
            self.atualizando_pausa = True
            self.atualizar_contagem_regressiva(botao, tempo)
            # self.manipulador_dados.registrar_pausa(botao, agora)
            mensagem = "{} de Pausa {}: {}".format(botao["text"], tempo // 60, agora.strftime("%Y-%m-%d %H:%M"))
            self.manipulador_dados.criar_log(mensagem)

            
        else:
            self.atualizando_pausa = False
            # botao.config(text="Pausa 10 HE")
            botao.config(state="disabled")
            # self.manipulador_dados.registrar_pausa(botao, agora)
            
