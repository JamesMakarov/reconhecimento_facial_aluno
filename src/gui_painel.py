import customtkinter as ctk
import json
import os

class PainelReconhecimento(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Controle de Chamada - Visão Computacional")
		self.geometry("700x550")
		
		self.rotulo_turma = ctk.CTkLabel(self, text="Selecione a Turma:", font=("Roboto", 16))
		self.rotulo_turma.pack(pady=(20, 5))
		
		self.seletor_turma = ctk.CTkComboBox(self, width=250, values=[
			"1º Ano - A", "1º Ano - B", "2º Ano - A", "2º Ano - B", 
			"3º Ano - A", "3º Ano - B", "4º Ano - A", "4º Ano - B",
			"5º Ano - A", "5º Ano - B", "6º Ano - A", "6º Ano - B",
			"7º Ano - U", "8º Ano - A", "8º Ano - B", "9º Ano - U"
		])
		self.seletor_turma.pack(pady=5)
		
		self.botao_iniciar = ctk.CTkButton(self, text="Iniciar Chamada", width=250, fg_color="green", hover_color="darkgreen", command=self.iniciar_processo_chamada)
		self.botao_iniciar.pack(pady=15)
		
		self.botao_encerrar = ctk.CTkButton(self, text="Encerrar Chamada", width=250, fg_color="red", hover_color="darkred", command=self.encerrar_processo_chamada)
		self.botao_encerrar.pack(pady=5)
		
		self.botao_presencas = ctk.CTkButton(self, text="Ver Presenças (JSON)", width=250, command=self.carregar_presencas)
		self.botao_presencas.pack(pady=15)
		
		self.caixa_texto_log = ctk.CTkTextbox(self, width=600, height=200, font=("Consolas", 12))
		self.caixa_texto_log.pack(pady=10)

	def iniciar_processo_chamada(self):
		turma_selecionada = self.seletor_turma.get()
		self.caixa_texto_log.insert("end", f"[SISTEMA] Iniciando reconhecimento para: {turma_selecionada}\n")

	def encerrar_processo_chamada(self):
		self.caixa_texto_log.insert("end", "[SISTEMA] Processo de visão encerrado. Dados consolidados.\n")

	def carregar_presencas(self):
		caminho_db = "../db/presencas.json"
		self.caixa_texto_log.insert("end", f"\n[SISTEMA] Lendo dados de: {caminho_db}\n")
		
		if os.path.exists(caminho_db):
			with open(caminho_db, "r", encoding="utf-8") as arquivo_json:
				dados = json.load(arquivo_json)
				texto_formatado = json.dumps(dados, indent=4, ensure_ascii=False)
				self.caixa_texto_log.insert("end", f"{texto_formatado}\n")
		else:
			self.caixa_texto_log.insert("end", "[ERRO] Arquivo presencas.json não localizado no diretório db.\n")

if __name__ == "__main__":
	ctk.set_appearance_mode("dark")
	app = PainelReconhecimento()
	app.mainloop()