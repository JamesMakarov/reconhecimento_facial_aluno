import cv2
import face_recognition
import json
import os
import numpy as np
from datetime import datetime
import motor_audio

class MotorVisao:
	def __init__(self, caminho_db_alunos, caminho_db_presencas, diretorio_audios):
		self.caminho_db_alunos = caminho_db_alunos
		self.caminho_db_presencas = caminho_db_presencas
		self.diretorio_audios = diretorio_audios
		self.rodando = False
		self.presencas_sessao = {}
		self.encodings_conhecidos = []
		self.dados_alunos_conhecidos = []

	def carregar_banco_turma(self, turma_alvo):
		self.encodings_conhecidos = []
		self.dados_alunos_conhecidos = []
		
		if not os.path.exists(self.caminho_db_alunos):
			return
			
		with open(self.caminho_db_alunos, 'r', encoding='utf-8') as f:
			banco_dados = json.load(f)
			
		for aluno in banco_dados:
			if aluno.get("turma") == turma_alvo:
				encoding_array = np.array(aluno["encoding"])
				self.encodings_conhecidos.append(encoding_array)
				self.dados_alunos_conhecidos.append(aluno)

	def salvar_presencas(self, turma_alvo):
		dados_existentes = []
		if os.path.exists(self.caminho_db_presencas):
			try:
				with open(self.caminho_db_presencas, 'r', encoding='utf-8') as f:
					dados_existentes = json.load(f)
			except json.JSONDecodeError:
				dados_existentes = []

		for matricula, info in self.presencas_sessao.items():
			registro = {
				"data": info["data"],
				"hora": info["hora"],
				"matricula": matricula,
				"nome": info["nome"],
				"turma": turma_alvo,
				"grupo": info["grupo"]
			}
			dados_existentes.append(registro)

		with open(self.caminho_db_presencas, 'w', encoding='utf-8') as f:
			json.dump(dados_existentes, f, ensure_ascii=False, indent=4)

	def iniciar_reconhecimento(self, turma_alvo, indice_camera=0):
		if not self.encodings_conhecidos:
			return

		self.rodando = True
		self.presencas_sessao = {}
		
		# Inicialização básica original
		captura = cv2.VideoCapture(indice_camera)
		
		total_inscritos = len(self.encodings_conhecidos)
		qtd_grupos = max(3, min(7, total_inscritos // 4))
		if qtd_grupos < 1: 
			qtd_grupos = 1
		
		while self.rodando:
			ret, frame = captura.read()
			if not ret:
				break

			# Redução simples
			frame_reduzido = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
			rgb_reduzido = cv2.cvtColor(frame_reduzido, cv2.COLOR_BGR2RGB)

			locais_faces = face_recognition.face_locations(rgb_reduzido)
			encodings_faces = face_recognition.face_encodings(rgb_reduzido, locais_faces)

			for encoding_face in encodings_faces:
				matches = face_recognition.compare_faces(self.encodings_conhecidos, encoding_face, tolerance=0.45)
				distancias = face_recognition.face_distance(self.encodings_conhecidos, encoding_face)
				
				if len(distancias) > 0:
					melhor_indice = np.argmin(distancias)
					
					if matches[melhor_indice]:
						aluno_detectado = self.dados_alunos_conhecidos[melhor_indice]
						matricula = aluno_detectado["matricula"]
						
						if matricula not in self.presencas_sessao:
							agora = datetime.now()
							indice_grupo_alocado = (len(self.presencas_sessao) % qtd_grupos) + 1
							nome_grupo_formatado = f"Grupo {indice_grupo_alocado}"
							
							self.presencas_sessao[matricula] = {
								"nome": aluno_detectado["nome_completo"],
								"data": agora.strftime("%Y-%m-%d"),
								"hora": agora.strftime("%H:%M:%S"),
								"grupo": nome_grupo_formatado
							}
							
							nome_arquivo = aluno_detectado.get("arquivo_audio")
							if nome_arquivo:
								caminho_audio_nome = os.path.join(self.diretorio_audios, nome_arquivo)
								caminho_audio_grupo = f"audios/sistema/grupo_{indice_grupo_alocado}.mp3"
								motor_audio.tocar_audio_background([caminho_audio_nome, caminho_audio_grupo])

		captura.release()
		self.salvar_presencas(turma_alvo)

	def parar_reconhecimento(self):
		self.rodando = False