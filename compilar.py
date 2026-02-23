import os
import sys
import subprocess
import face_recognition_models

def iniciar_compilacao():
    # Descobre automaticamente onde a IA está instalada no seu PC
    caminho_ia = os.path.dirname(face_recognition_models.__file__)
    caminho_modelos = os.path.join(caminho_ia, 'models')

    # Monta a regra de injeção de dados (CaminhoOrigem;CaminhoDestino)
    argumento_dados = f"{caminho_modelos};face_recognition_models/models"

    # Monta o comando de compilação impecável
    comando = [
        sys.executable, "-m", "PyInstaller",
        "--name", "Chamada_Inteligente",
        "--onedir",
        "--noconsole",
        "--icon", "icone.ico",
        "--collect-all", "customtkinter",
        "--add-data", argumento_dados,
        "src/main.py"
    ]

    print("-" * 50)
    print("Iniciando a compilação do sistema...")
    print(f"Injetando a IA a partir de: {caminho_modelos}")
    print("-" * 50)
    
    subprocess.run(comando)
    
    print("-" * 50)
    print("Compilação finalizada com sucesso! Verifique a pasta 'dist'.")

if __name__ == "__main__":
    iniciar_compilacao()