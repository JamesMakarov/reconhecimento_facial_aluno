import customtkinter as ctk
import json
import os
import cv2
from pygrabber.dshow_graph import FilterGraph

def listar_cameras():
	try:
		graph = FilterGraph()
		dispositivos = graph.get_input_devices()
		lista_formatada = []
		for indice, nome in enumerate(dispositivos):
			lista_formatada.append(f"{indice} - {nome}")
		
		if not lista_formatada:
			return ["0 - Câmera Padrão"]
		return lista_formatada
	except Exception:
		return ["0 - Câmera 0", "1 - Câmera 1", "2 - Câmera 2", "3 - Câmera 3"]

class PainelReconhecimento(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Controle de Chamada - Visão Computacional")
		self.geometry("700x650")
		
		self.rotulo_turma = ctk.CTkLabel(self, text="Selecione a Turma:", font=("Roboto", 16))
		self.rotulo_turma.pack(pady=(20, 5))
		
		self.seletor_turma = ctk.CTkComboBox(self, width=250, values=[
			"1º Ano - A", "1º Ano - B", "2º Ano - A", "2º Ano - B", 
			"3º Ano - A", "3º Ano - B", "4º Ano - A", "4º Ano - B",
			"5º Ano - A", "5º Ano - B", "6º Ano - A", "6º Ano - B",
			"7º Ano - U", "8º Ano - A", "8º Ano - B", "9º Ano - U"
		])
		self.seletor_turma.pack(pady=5)
		
		self.rotulo_camera = ctk.CTkLabel(self, text="Selecione a Câmera:", font=("Roboto", 16))
		self.rotulo_camera.pack(pady=(10, 5))
		
		lista_cameras = listar_cameras()
		self.seletor_camera = ctk.CTkComboBox(self, width=250, values=lista_cameras)
		self.seletor_camera.pack(pady=5)
		
		self.botao_iniciar = ctk.CTkButton(self, text="Iniciar Chamada", width=250, fg_color="green", hover_color="darkgreen")
		self.botao_iniciar.pack(pady=15)
		
		self.botao_encerrar = ctk.CTkButton(self, text="Encerrar Chamada", width=250, fg_color="red", hover_color="darkred")
		self.botao_encerrar.pack(pady=5)
		
		self.botao_presencas = ctk.CTkButton(self, text="Ver Presenças (JSON)", width=250, command=self.carregar_presencas)
		self.botao_presencas.pack(pady=15)
		
		self.caixa_texto_log = ctk.CTkTextbox(self, width=600, height=200, font=("Consolas", 12))
		self.caixa_texto_log.pack(pady=10)

	def carregar_presencas(self):
		caminho_db = "db/presencas.json"
		self.caixa_texto_log.insert("end", f"\n[SISTEMA] Lendo dados de: {caminho_db}\n")
		
		if os.path.exists(caminho_db):
			try:
				with open(caminho_db, "r", encoding="utf-8") as arquivo_json:
					dados = json.load(arquivo_json)
					texto_formatado = json.dumps(dados, indent=4, ensure_ascii=False)
					self.caixa_texto_log.insert("end", f"{texto_formatado}\n")
			except json.JSONDecodeError:
				self.caixa_texto_log.insert("end", "[AVISO] Arquivo presencas.json existe, mas está vazio ou mal formatado.\n")
		else:
			self.caixa_texto_log.insert("end", "[ERRO] Arquivo presencas.json ainda não existe.\n")

if __name__ == "__main__":
	ctk.set_appearance_mode("dark")
	app = PainelReconhecimento()
	app.mainloop()