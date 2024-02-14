class ManipuladorDados:
    def __init__(self):
        pass

    def criar_log(self, mensagem):
        with open("Log.txt", "a") as arquivo_log:
            arquivo_log.write(mensagem + "\n")

    def atualizar_interface(self, tempo_formatado):
        # Aqui você poderia adicionar a lógica para atualizar a interface com o tempo decorrido
        pass

    # def registrar_pausa(self, timestamp, tempo_pausa):
    #     if tempo_pausa > 0:
    #         mensagem = "Início de Pausa: {}".format(timestamp.strftime("%Y-%m-%d %H:%M"))
    #     else:
    #         mensagem = "Fim de Pausa: {}".format(timestamp.strftime("%Y-%m-%d %H:%M"))
    #     self.criar_log(mensagem)
