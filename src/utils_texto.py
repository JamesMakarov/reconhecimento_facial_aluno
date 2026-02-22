import unicodedata

def normalizar_nome_arquivo(nome):
	nome_decomposto = unicodedata.normalize('NFD', nome)
	caracteres_ascii = [c for c in nome_decomposto if unicodedata.category(c) != 'Mn']
	nome_limpo = ''.join(caracteres_ascii)
	return nome_limpo.lower().replace(" ", "_")

def extrair_nome_vocalizacao(nome_completo):
	return nome_completo.strip().title()

def construir_base_alunos(caminho_arquivo):
	lista_alunos = []
	estado_turma_atual = ""
	
	with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
		linhas = arquivo.readlines()
		
	for linha in linhas:
		linha = linha.strip()
		if not linha:
			continue
			
		if linha.startswith("TURMA:"):
			estado_turma_atual = linha.replace("TURMA:", "").strip()
		elif ";" in linha:
			dados = linha.split(";")
			matricula = dados[0].strip()
			nome_completo = dados[1].strip()
			
			if nome_completo:
				nome_vocalizacao = extrair_nome_vocalizacao(nome_completo)
				nome_arquivo_audio = normalizar_nome_arquivo(nome_vocalizacao)
				
				lista_alunos.append({
					"matricula": matricula,
					"nome_completo": nome_completo,
					"nome_vocalizacao": nome_vocalizacao,
					"arquivo_audio": f"{nome_arquivo_audio}.mp3",
					"turma": estado_turma_atual
				})
				
	return lista_alunos