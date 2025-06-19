# Multiagentes

## Pasos para instalar

1. Clonar el repositorio
```bash
# Por SSH, es requerido tener configurado el acceso SSH a GitHub
git clone git@github.com:joctan-tec/multiagentes.git
# Por HTTPS
git clone https://github.com/joctan-tec/multiagentes.git
```

2. Ejecutar el archivo ejecutable para la instalacion
```bash
./install.sh
```

3. Esperar a que se contruya la imagen de Docker y se configure el ambiente.
4. Acceder a ```http://localhost:5000/``` en su navegador.


---

1. Crear un entorno virtual
```bash
# En Linux o MacOS
python3 -m venv venv
# En Windows
python -m venv venv
```
1. Activar el entorno virtual
```bash
# En Linux o MacOS
source venv/bin/activate
# En Windows
venv\Scripts\activate
```
1. Instalar las dependencias
```bash
pip install -r requirements.txt
```
1. Ejecutar Chroma
```bash
cd app/
chroma run
```

1. Abrir una nueva terminal y activar el entorno virtual
```bash
# En Linux o MacOS
source venv/bin/activate
# En Windows
venv\Scripts\activate

1. Guardar el archivo de Codigo de Trabajo
```bash
cd app/

# En Linux o MacOS
python3 text_processor/save_to_chromadb.py
# En Windows
python text_processor\save_to_chromadb.py
```





