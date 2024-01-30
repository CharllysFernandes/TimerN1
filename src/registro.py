from datetime import datetime, timedelta

class RegistroHoras:
    def __init__(self):
        self.horas_trabalhadas = timedelta()
        self.hora_inicio = None

    def iniciar_trabalho(self):
        self.hora_inicio = datetime.now()

    def encerrar_trabalho(self):
        if self.hora_inicio:
            self.horas_trabalhadas += datetime.now() - self.hora_inicio
            self.hora_inicio = None

    def registrar_pausa(self, minutos):
        if self.hora_inicio:
            self.hora_inicio += timedelta(minutes=minutos)

    def obter_tempo_formatado(self):
        horas, resto = divmod(self.horas_trabalhadas.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        return "{:02}:{:02}:{:02}".format(horas, minutos, segundos)
    