import threading
import os
from gui_painel import PainelReconhecimento
from motor_visao import MotorVisao
import motor_audio

class AppPrincipal:
	def __init__(self):
		motor_audio.inicializar_mixer()
		self.interface = PainelReconhecimento()
		self.motor = MotorVisao(
			caminho_db_alunos="db/alunos.json",
			caminho_db_presencas="db/presencas.json",
			diretorio_audios="audios/nomes"
		)
		self.interface.botao_iniciar.configure(command=self.iniciar_chamada_thread)
		self.interface.botao_encerrar.configure(command=self.encerrar_chamada)

	def iniciar_chamada_thread(self):
		turma_selecionada = self.interface.seletor_turma.get()
		camera_selecionada = self.interface.seletor_camera.get()
		indice_camera = int(camera_selecionada.split(" - ")[0])
		
		self.motor.carregar_banco_turma(turma_selecionada)
		if not self.motor.encodings_conhecidos:
			self.interface.log_sistema(f"[ERRO] Nenhum aluno cadastrado na biometria para: {turma_selecionada}")
			return
			
		caminho_audio_iniciar = "audios/sistema/iniciando_chamada.mp3"
		os.makedirs(os.path.dirname(caminho_audio_iniciar), exist_ok=True)
		
		if not os.path.exists(caminho_audio_iniciar):
			motor_audio.gerar_audio_neural("Iniciando chamada.", caminho_audio_iniciar)
			
		motor_audio.tocar_audio_background(caminho_audio_iniciar)
		
		self.interface.log_sistema(f"[SISTEMA] Iniciando reconhecimento para: {turma_selecionada} na {camera_selecionada}")
		self.thread_visao = threading.Thread(target=self.motor.iniciar_reconhecimento, args=(turma_selecionada, indice_camera))
		self.thread_visao.start()

	def encerrar_chamada(self):
		self.motor.parar_reconhecimento()
		self.interface.log_sistema("[SISTEMA] Processo de visão encerrado. Dados salvos no banco.")
		self.interface.carregar_banco_presencas()

	def executar(self):
		self.interface.mainloop()

if __name__ == "__main__":
	app = AppPrincipal()
	app.executar()