import asyncio
import edge_tts
import pygame
import threading
import os

def inicializar_mixer():
	pygame.mixer.init()

async def gerar_audio_neural_async(texto, caminho_saida):
	comunicador = edge_tts.Communicate(texto, "pt-BR-FranciscaNeural")
	await comunicador.save(caminho_saida)

def gerar_audio_neural(texto, caminho_saida):
	asyncio.run(gerar_audio_neural_async(texto, caminho_saida))

def reproduzir_audio(caminho_arquivo):
	if not os.path.exists(caminho_arquivo):
		return
		
	pygame.mixer.music.load(caminho_arquivo)
	pygame.mixer.music.play()
	
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(10)

def tocar_audio_background(caminho_arquivo):
	thread_audio = threading.Thread(target=reproduzir_audio, args=(caminho_arquivo,))
	thread_audio.start()