class ControleBotoes:
    def __init__(self, registro_horas, interface):
        self.registro_horas = registro_horas
        self.interface = interface
        self.is_trabalho_iniciado = False

    def iniciar_trabalho(self):
        self.registro_horas.iniciar_trabalho()
        self.interface.atualizar_display()

    def encerrar_trabalho(self):
        self.registro_horas.encerrar_trabalho()
        self.interface.atualizar_display()

    def registrar_pausa(self, minutos):
        self.registro_horas.registrar_pausa(minutos)
        self.interface.atualizar_display()

    def registrar_pausa_he(self, minutos):
        self.registro_horas.registrar_pausa_he(minutos)
        self.interface.atualizar_display()

    def toggle_trabalho(self):
        if not self.is_trabalho_iniciado:
            self.iniciar_trabalho()
            self.is_trabalho_iniciado = True
            self.interface.iniciar_button.config(text="Encerrar")
        else:
            self.encerrar_trabalho()
            self.is_trabalho_iniciado = False
            self.interface.iniciar_button.config(text="Iniciar")
