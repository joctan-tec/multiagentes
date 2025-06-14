# Multiagentes

## Pasos para instalar

1. Clonar el repositorio
```bash
# Por SSH, es requerido tener configurado el acceso SSH a GitHub
git clone git@github.com:joctan-tec/multiagentes.git
# Por HTTPS
git clone https://github.com/joctan-tec/multiagentes.git
```
2. Crear un entorno virtual
```bash
# En Linux o MacOS
python3 -m venv venv
# En Windows
python -m venv venv
```
3. Activar el entorno virtual
```bash
# En Linux o MacOS
source venv/bin/activate
# En Windows
venv\Scripts\activate
```
4. Instalar las dependencias
```bash
pip install -r requirements.txt
```
5. Ejecutar Chroma
```bash
cd app/
chromadb run
```

6. Guardar el archivo de Codigo de Trabajo
```bash
cd app/

# En Linux o MacOS
python3 save_to_chromadb.py
# En Windows
python save_to_chromadb.py
```





