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

		# Componente mestre de Abas
		self.sistema_abas = ctk.CTkTabview(self)
		self.sistema_abas.pack(fill="both", expand=True, padx=10, pady=10)

		# Criando as páginas
		self.aba_operacao = self.sistema_abas.add("Operação")
		self.aba_relatorios = self.sistema_abas.add("Relatórios")

		self.configurar_aba_operacao()
		self.configurar_aba_relatorios()

	def configurar_aba_operacao(self):
		self.aba_operacao.grid_columnconfigure(0, weight=1)
		self.aba_operacao.grid_columnconfigure(1, weight=2)
		self.aba_operacao.grid_rowconfigure(0, weight=1)

		# ----- PAINEL ESQUERDO (Controles) -----
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

		# ----- PAINEL DIREITO (Console de Log) -----
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

		# Barra superior da aba de relatórios
		frame_topo = ctk.CTkFrame(self.aba_relatorios, fg_color="transparent")
		frame_topo.grid(row=0, column=0, sticky="ew", pady=(0, 10))

		ctk.CTkLabel(frame_topo, text="Lista de Presenças Consolidadas", font=("Roboto", 18, "bold")).pack(side="left", padx=10)
		
		botao_atualizar = ctk.CTkButton(frame_topo, text="Atualizar Tabela", fg_color="#2980b9", hover_color="#3498db", command=self.carregar_presencas)
		botao_atualizar.pack(side="right", padx=10)

		# Tabela Rolável
		self.tabela_presencas = ctk.CTkScrollableFrame(self.aba_relatorios)
		self.tabela_presencas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
		
		# Carrega a tabela assim que o programa abrir
		self.carregar_presencas()

	def log_sistema(self, mensagem):
		self.caixa_texto_log.insert("end", mensagem + "\n")
		self.caixa_texto_log.see("end") # Rola o console para o final automaticamente

	def carregar_presencas(self):
		caminho_db = "db/presencas.json"
		
		# Destrói os rótulos antigos antes de desenhar os novos
		for widget in self.tabela_presencas.winfo_children():
			widget.destroy()

		# Desenha os Cabeçalhos
		cabecalhos = ["Data", "Hora", "Matrícula", "Nome do Aluno", "Turma"]
		for col, texto in enumerate(cabecalhos):
			lbl = ctk.CTkLabel(self.tabela_presencas, text=texto, font=("Roboto", 14, "bold"))
			lbl.grid(row=0, column=col, padx=15, pady=10, sticky="w")

		if not os.path.exists(caminho_db):
			lbl_erro = ctk.CTkLabel(self.tabela_presencas, text="Nenhum registro de presença encontrado.", text_color="#e74c3c")
			lbl_erro.grid(row=1, column=0, columnspan=5, pady=20)
			return

		try:
			with open(caminho_db, "r", encoding="utf-8") as arquivo_json:
				dados = json.load(arquivo_json)
			
			# Preenche as linhas com os dados
			for linha_idx, registro in enumerate(dados, start=1):
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("data", "")).grid(row=linha_idx, column=0, padx=15, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("hora", "")).grid(row=linha_idx, column=1, padx=15, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("matricula", "")).grid(row=linha_idx, column=2, padx=15, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("nome", "")[:25] + "...").grid(row=linha_idx, column=3, padx=15, pady=2, sticky="w")
				ctk.CTkLabel(self.tabela_presencas, text=registro.get("turma", "")).grid(row=linha_idx, column=4, padx=15, pady=2, sticky="w")
				
		except json.JSONDecodeError:
			lbl_erro = ctk.CTkLabel(self.tabela_presencas, text="O arquivo JSON está vazio ou corrompido.", text_color="#f39c12")
			lbl_erro.grid(row=1, column=0, columnspan=5, pady=20)