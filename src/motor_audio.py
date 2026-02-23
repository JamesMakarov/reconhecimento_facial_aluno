import asyncio
import edge_tts
import pygame
import threading
import os
import queue

fila_audio = queue.Queue()
thread_worker = None

def _worker_audio():
	while True:
		item = fila_audio.get()
		if item is None:
			break
			
		if isinstance(item, str):
			item = [item]
			
		for caminho in item:
			if os.path.exists(caminho):
				pygame.mixer.music.load(caminho)
				pygame.mixer.music.play()
				while pygame.mixer.music.get_busy():
					pygame.time.Clock().tick(10)
		fila_audio.task_done()

def inicializar_mixer():
	global thread_worker
	if not pygame.mixer.get_init():
		pygame.mixer.init()
		
	if thread_worker is None or not thread_worker.is_alive():
		thread_worker = threading.Thread(target=_worker_audio, daemon=True)
		thread_worker.start()

async def gerar_audio_neural_async(texto, caminho_saida):
	comunicador = edge_tts.Communicate(texto, "pt-BR-FranciscaNeural")
	await comunicador.save(caminho_saida)

def gerar_audio_neural(texto, caminho_saida):
	asyncio.run(gerar_audio_neural_async(texto, caminho_saida))

def tocar_audio_background(arquivos):
	fila_audio.put(arquivos)