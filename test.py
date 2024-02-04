import tkinter as tk

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Contagem Regressiva")

        self.label_tempo = tk.Label(root, text="00:00", font=("Helvetica", 24))
        self.label_tempo.pack(pady=20)

        self.botao_contagem = tk.Button(root, text="Iniciar (1:00)", command=self.iniciar_contagem)
        self.botao_contagem.pack(pady=10)

        self.tempo_restante = 60
        self.atualizando = False

    def iniciar_contagem(self):
        if not self.atualizando:
            self.atualizando = True
            self.atualizar_contagem_regressiva()

    def atualizar_contagem_regressiva(self):
        if self.atualizando and self.tempo_restante > 0:
            minutos, segundos = divmod(self.tempo_restante, 60)
            tempo_formatado = "{:02}:{:02}".format(minutos, segundos)
            self.botao_contagem.config(text="Encerrar ({})".format(tempo_formatado))
            self.tempo_restante -= 1
            self.root.after(1000, self.atualizar_contagem_regressiva)
        elif self.tempo_restante == 0:
            self.atualizando = False
            self.botao_contagem.config(text="Iniciar (1:00)")
            self.tempo_restante = 60

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
