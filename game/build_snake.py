import subprocess
import sys

try:
    import PyInstaller
except ImportError:
    print("PyInstaller não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

try:
    import pygame
except ImportError:
    print("Pygame não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

print("Iniciando o processo de construção do executável...")
try:
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "--onefile", "snake.py"])
except subprocess.CalledProcessError as e:
    print(f"Erro ao chamar PyInstaller: {e}")
    sys.exit(1)

print("Construção concluída. O executável está na pasta 'dist'.")
