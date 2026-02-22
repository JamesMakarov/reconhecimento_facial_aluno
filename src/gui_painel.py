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
		self.geometry("950x650")

		self.dados_presencas = []

		self.sistema_abas = ctk.CTkTabview(self)
		self.sistema_abas.pack(fill="both", expand=True, padx=10, pady=10)

		self.aba_operacao = self.sistema_abas.add("Operação")
		self.aba_relatorios = self.sistema_abas.add("Relatórios")

		self.configurar_aba_operacao()
		self.configurar_aba_relatorios()

	def configurar_aba_operacao(self):
		self.aba_operacao.grid_columnconfigure(0, weight=1)
		self.aba_operacao.grid_columnconfigure(1, weight=2)
		self.aba_operacao.grid_rowconfigure(0, weight=1)

		frame_controles = ctk.CTkFrame(self.aba_operacao)
		frame_controles.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

		ctk.CTkLabel(frame_controles, text="Selecione a Turma:", font=("Roboto", 16, "bold")).pack(pady=(20, 5), padx=20)
		
		self.seletor_turma = ctk.CTkComboBox(frame_controles, width=250, values=[
			"1º Ano - A", "1º Ano - B", "2º Ano - A", "2º Ano - B", 
			"3º Ano - A", "3º Ano - B", "4º Ano - A", "4º Ano - B",
			"5º Ano - A", "5º Ano - B", "6º Ano - A", "6º Ano - B",
			"7º Ano - U", "8º Ano - A", "8º Ano - B", "9º Ano - U"
		])
		self.seletor_turma.pack(pady=5, padx=20)

		ctk.CTkLabel(frame_controles, text="Selecione a Câmera:", font=("Roboto", 16, "bold")).pack(pady=(20, 5), padx=20)
		
		self.seletor_camera = ctk.CTkComboBox(frame_controles, width=250, values=listar_cameras())
		self.seletor_camera.pack(pady=5, padx=20)

		self.botao_iniciar = ctk.CTkButton(frame_controles, text="Iniciar Chamada", width=250, fg_color="#27ae60", hover_color="#2ecc71")
		self.botao_iniciar.pack(pady=(40, 10), padx=20)

		self.botao_encerrar = ctk.CTkButton(frame_controles, text="Encerrar Chamada", width=250, fg_color="#c0392b", hover_color="#e74c3c")
		self.botao_encerrar.pack(pady=10, padx=20)

		frame_console = ctk.CTkFrame(self.aba_operacao)
		frame_console.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
		frame_console.grid_rowconfigure(1, weight=1)
		frame_console.grid_columnconfigure(0, weight=1)

		ctk.CTkLabel(frame_console, text="Console de Execução", font=("Roboto", 18, "bold")).grid(row=0, column=0, pady=(10, 0), sticky="w", padx=10)
		self.caixa_texto_log = ctk.CTkTextbox(frame_console, font=("Consolas", 13))
		self.caixa_texto_log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

	def configurar_aba_relatorios(self):
		self.aba_relatorios.grid_rowconfigure(1, weight=1)
		self.aba_relatorios.grid_columnconfigure(0, weight=1)

		frame_topo = ctk.CTkFrame(self.aba_relatorios, fg_color="transparent")
		frame_topo.grid(row=0, column=0, sticky="ew", pady=(0, 10))

		ctk.CTkLabel(frame_topo, text="Turma:", font=("Roboto", 14, "bold")).pack(side="left", padx=(10, 5))
		self.filtro_turma = ctk.CTkComboBox(frame_topo, width=150, values=["Nenhuma"], command=self.ao_selecionar_turma)
		self.filtro_turma.pack(side="left", padx=5)

		ctk.CTkLabel(frame_topo, text="Data da Aula:", font=("Roboto", 14, "bold")).pack(side="left", padx=(20, 5))
		self.filtro_data = ctk.CTkComboBox(frame_topo, width=150, values=["-"], command=self.exibir_tabela_filtrada)
		self.filtro_data.pack(side="left", padx=5)

		botao_atualizar = ctk.CTkButton(frame_topo, text="Sincronizar Arquivo", fg_color="#2980b9", hover_color="#3498db", command=self.carregar_banco_presencas)
		botao_atualizar.pack(side="right", padx=10)

		self.tabela_presencas = ctk.CTkScrollableFrame(self.aba_relatorios)
		self.tabela_presencas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
		
		self.carregar_banco_presencas()

	def log_sistema(self, mensagem):
		self.caixa_texto_log.insert("end", mensagem + "\n")
		self.caixa_texto_log.see("end")

	def carregar_banco_presencas(self):
		caminho_db = "db/presencas.json"
		if os.path.exists(caminho_db):
			try:
				with open(caminho_db, "r", encoding="utf-8") as arquivo_json:
					self.dados_presencas = json.load(arquivo_json)
			except json.JSONDecodeError:
				self.dados_presencas = []
		else:
			self.dados_presencas = []

		turmas_disponiveis = sorted(list(set(registro.get("turma") for registro in self.dados_presencas)))
		
		if not turmas_disponiveis:
			self.filtro_turma.configure(values=["Nenhuma"])
			self.filtro_turma.set("Nenhuma")
			self.filtro_data.configure(values=["-"])
			self.filtro_data.set("-")
			self.limpar_tabela()
			return

		self.filtro_turma.configure(values=turmas_disponiveis)
		self.filtro_turma.set(turmas_disponiveis[0])
		self.ao_selecionar_turma(turmas_disponiveis[0])

	def ao_selecionar_turma(self, turma_selecionada):
		datas = sorted(list(set(registro.get("data") for registro in self.dados_presencas if registro.get("turma") == turma_selecionada)), reverse=True)
		
		if not datas:
			self.filtro_data.configure(values=["Nenhuma"])
			self.filtro_data.set("Nenhuma")
		else:
			self.filtro_data.configure(values=datas)
			self.filtro_data.set(datas[0])
			
		self.exibir_tabela_filtrada()

	def limpar_tabela(self):
		for widget in self.tabela_presencas.winfo_children():
			widget.destroy()

		cabecalhos = ["Data", "Hora", "Matrícula", "Nome do Aluno", "Turma"]
		for col, texto in enumerate(cabecalhos):
			lbl = ctk.CTkLabel(self.tabela_presencas, text=texto, font=("Roboto", 14, "bold"))
			lbl.grid(row=0, column=col, padx=15, pady=10, sticky="w")

	def exibir_tabela_filtrada(self, evento_ignorado=None):
		self.limpar_tabela()
		
		turma_selecionada = self.filtro_turma.get()
		data_selecionada = self.filtro_data.get()

		if turma_selecionada == "Nenhuma" or data_selecionada == "Nenhuma" or data_selecionada == "-":
			return

		registros_filtrados = [r for r in self.dados_presencas if r.get("turma") == turma_selecionada and r.get("data") == data_selecionada]
		registros_ordenados = sorted(registros_filtrados, key=lambda x: x.get("nome", ""))

		for linha_idx, registro in enumerate(registros_ordenados, start=1):
			ctk.CTkLabel(self.tabela_presencas, text=registro.get("data", "")).grid(row=linha_idx, column=0, padx=15, pady=2, sticky="w")
			ctk.CTkLabel(self.tabela_presencas, text=registro.get("hora", "")).grid(row=linha_idx, column=1, padx=15, pady=2, sticky="w")
			ctk.CTkLabel(self.tabela_presencas, text=registro.get("matricula", "")).grid(row=linha_idx, column=2, padx=15, pady=2, sticky="w")
			
			nome_limite = registro.get("nome", "")
			if len(nome_limite) > 30:
				nome_limite = nome_limite[:27] + "..."
				
			ctk.CTkLabel(self.tabela_presencas, text=nome_limite).grid(row=linha_idx, column=3, padx=15, pady=2, sticky="w")
			ctk.CTkLabel(self.tabela_presencas, text=registro.get("turma", "")).grid(row=linha_idx, column=4, padx=15, pady=2, sticky="w")