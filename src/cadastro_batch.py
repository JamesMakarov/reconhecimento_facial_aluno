import os
import json
import face_recognition
from utils_texto import construir_base_alunos
from motor_audio import gerar_audio_neural

def processar_cadastros(caminho_txt, diretorio_imagens, diretorio_audios, caminho_json):
	alunos = construir_base_alunos(caminho_txt)
	banco_dados = []

	os.makedirs(diretorio_audios, exist_ok=True)
	os.makedirs(os.path.dirname(caminho_json), exist_ok=True)
	extensoes = [".jpg", ".jpeg", ".png"]

	for aluno in alunos:
		matricula = aluno["matricula"]
		caminho_imagem = None
		
		for ext in extensoes:
			caminho_teste = os.path.join(diretorio_imagens, f"{matricula}{ext}")
			if os.path.exists(caminho_teste):
				caminho_imagem = caminho_teste
				break
				
		if not caminho_imagem:
			continue
			
		imagem = face_recognition.load_image_file(caminho_imagem)
		encodings = face_recognition.face_encodings(imagem)
		
		if not encodings:
			continue
			
		encoding_lista = encodings[0].tolist()
		caminho_audio = os.path.join(diretorio_audios, aluno["arquivo_audio"])
		
		if not os.path.exists(caminho_audio):
			gerar_audio_neural(aluno["nome_vocalizacao"], caminho_audio)
			
		aluno_db = {
			"matricula": matricula,
			"nome_completo": aluno["nome_completo"],
			"turma": aluno["turma"],
			"arquivo_audio": aluno["arquivo_audio"],
			"encoding": encoding_lista
		}
		banco_dados.append(aluno_db)

	with open(caminho_json, 'w', encoding='utf-8') as arquivo_saida:
		json.dump(banco_dados, arquivo_saida, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	processar_cadastros("alunos.txt", "imagens_cadastro", "audios/nomes", "db/alunos.json")