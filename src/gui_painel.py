import customtkinter as ctk
import json
import os
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
		return ["0 - Câmera 0", "1 - Câmera 1", "2 - Câmera 2"]

class PainelReconhecimento(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Sistema de Chamada Facial")
		self.geometry("1000x600")

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=3)
		self.grid_rowconfigure(0, weight=1)

		self.frame_menu = ctk.CTkFrame(self, corner_radius=0)
		self.frame_menu.grid(row=0, column=0, sticky="nsew")
		
		self.rotulo_turma = ctk.CTkLabel(self.frame_menu, text="Selecione a Turma:", font=("Roboto", 16, "bold"))
		self.rotulo_turma.pack(pady=(20, 5), padx=20)
		
		self.seletor_turma = ctk.CTkComboBox(self.frame_menu, width=250, values=[
			"1º Ano - A", "1º Ano - B", "2º Ano - A", "2º Ano - B", 
			"3º Ano - A", "3º Ano - B", "4º Ano - A", "4º Ano - B",
			"5º Ano - A", "5º Ano - B", "6º Ano - A", "6º Ano - B",
			"7º Ano - U", "8º Ano - A", "8º Ano - B", "9º Ano - U"
		])
		self.seletor_turma.pack(pady=5, padx=20)
		
		self.rotulo_camera = ctk.CTkLabel(self.frame_menu, text="Selecione a Câmera:", font=("Roboto", 16, "bold"))
		self.rotulo_camera.pack(pady=(20, 5), padx=20)
		
		lista_cameras = listar_cameras()
		self.seletor_camera = ctk.CTkComboBox(self.frame_menu, width=250, values=lista_cameras)
		self.seletor_camera.pack(pady=5, padx=20)
		
		self.botao_iniciar = ctk.CTkButton(self.frame_menu, text="Iniciar Chamada", width=250, fg_color="#27ae60", hover_color="#2ecc71")
		self.botao_iniciar.pack(pady=(40, 10), padx=20)
		
		self.botao_encerrar = ctk.CTkButton(self.frame_menu, text="Encerrar Chamada", width=250, fg_color="#c0392b", hover_color="#e74c3c")
		self.botao_encerrar.pack(pady=10, padx=20)
		
		self.botao_presencas = ctk.CTkButton(self.frame_menu, text="Ver Presenças Consolidadas", width=250, fg_color="#2980b9", hover_color="#3498db", command=self.carregar_presencas)
		self.botao_presencas.pack(pady=10, padx=20)

		self.frame_dados = ctk.CTkFrame(self)
		self.frame_dados.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
		self.frame_dados.grid_rowconfigure(1, weight=1)
		self.frame_dados.grid_columnconfigure(0, weight=1)

		self.rotulo_painel = ctk.CTkLabel(self.frame_dados, text="Console de Execução", font=("Roboto", 18, "bold"))
		self.rotulo_painel.grid(row=0, column=0, pady=(10, 0), sticky="w", padx=10)

		self.caixa_texto_log = ctk.CTkTextbox(self.frame_dados, font=("Consolas", 13))
		self.caixa_texto_log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

		self.tabela_presencas = ctk.CTkScrollableFrame(self.frame_dados)
		
	def alternar_visualizacao(self, mostrar_tabela):
		if mostrar_tabela:
			self.caixa_texto_log.grid_remove()
			self.rotulo_painel.configure(text="Relatório de Presenças")
			self.tabela_presencas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
		else:
			self.tabela_presencas.grid_remove()
			self.rotulo_painel.configure(text="Console de Execução")
			self.caixa_texto_log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

	def log_sistema(self, mensagem):
		self.alternar_visualizacao(mostrar_tabela=False)
		self.caixa_texto_log.insert("end", mensagem + "\n")
		self.caixa_texto_log.see("end")

	def carregar_presencas(self):
		self.alternar_visualizacao(mostrar_tabela=True)
		caminho_db = "db/presencas.json"
		
		for widget in self.tabela_presencas.winfo_children():
			widget.destroy()

		cabecalhos = ["Data", "Hora", "Matrícula", "Nome do Aluno", "Turma"]
		for col, texto in enumerate(cabecalhos):
			lbl = ctk.CTkLabel(self.tabela_presencas, text=texto, font=("Roboto", 14, "bold"))
			lbl.grid(row=0, column=col, padx=10, pady=10, sticky="w")

		if not os.path.exists(caminho_db):
			lbl_erro = ctk.CTkLabel(self.tabela_presencas, text="Nenhum registro de presença encontrado no disco.", text_color="#e74c3c")
			lbl_erro.grid(row=1, column=0, columnspan=5, pady=20)
			return

		try:
			with open(caminho_db, "r", encoding="utf-8") as arquivo_json:
				dados = json.load(arquivo_json)
			
			for linha_idx, registro in enumerate(dados, start=1):
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("data", "")).grid(row=linha_idx, column=0, padx=10, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("hora", "")).grid(row=linha_idx, column=1, padx=10, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("matricula", "")).grid(row=linha_idx, column=2, padx=10, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("nome", "")).grid(row=linha_idx, column=3, padx=10, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("turma", "")).grid(row=linha_idx, column=4, padx=10, pady=2, sticky="w")
				
		except json.JSONDecodeError:
			lbl_erro = ctk.CTkLabel(self.tabela_presencas, text="Falha de desserialização: o arquivo JSON está vazio ou corrompido.", text_color="#f39c12")
			lbl_erro.grid(row=1, column=0, columnspan=5, pady=20)