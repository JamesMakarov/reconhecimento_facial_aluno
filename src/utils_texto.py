import unicodedata

def normalizar_nome_arquivo(nome):
	nome_decomposto = unicodedata.normalize('NFD', nome)
	caracteres_ascii = [c for c in nome_decomposto if unicodedata.category(c) != 'Mn']
	nome_limpo = ''.join(caracteres_ascii)
	return nome_limpo.lower().replace(" ", "_").replace("'", "")

def extrair_partes_nome(nome_completo, n_partes_reais):
	partes = nome_completo.strip().split()
	preposicoes = {"da", "de", "do", "das", "dos", "e"}
	nome_final = []
	partes_adicionadas = 0
	
	for p in partes:
		if partes_adicionadas < n_partes_reais:
			nome_final.append(p)
			if p.lower() not in preposicoes:
				partes_adicionadas += 1
		else:
			break
	return " ".join(nome_final).title()

def resolver_colisoes(lista_alunos):
	for aluno in lista_alunos:
		aluno['n_partes'] = 2
		
	while True:
		contagem = {}
		for aluno in lista_alunos:
			voc = extrair_partes_nome(aluno['nome_completo'], aluno['n_partes'])
			aluno['nome_vocalizacao'] = voc
			contagem[voc] = contagem.get(voc, 0) + 1
		
		houve_conflito = False
		for aluno in lista_alunos:
			if contagem[aluno['nome_vocalizacao']] > 1:
				total_validas = len([p for p in aluno['nome_completo'].split() if p.lower() not in {"da", "de", "do", "das", "dos", "e"}])
				if aluno['n_partes'] < total_validas:
					aluno['n_partes'] += 1
					houve_conflito = True
					
		if not houve_conflito:
			break
			
	for aluno in lista_alunos:
		aluno['arquivo_audio'] = normalizar_nome_arquivo(aluno['nome_vocalizacao']) + ".mp3"
		
	return lista_alunos

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
				lista_alunos.append({
					"matricula": matricula,
					"nome_completo": nome_completo,
					"turma": estado_turma_atual
				})
				
	return resolver_colisoes(lista_alunos)