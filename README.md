# Multiagentes

## Pasos para instalar

**1.** Clonar el repositorio
```bash
# Por SSH, es requerido tener configurado el acceso SSH a GitHub
git clone git@github.com:joctan-tec/multiagentes.git
# Por HTTPS
git clone https://github.com/joctan-tec/multiagentes.git
```

**2.** Ingresar al directorio del proyecto
```bash
cd multiagentes
```

**3.** Ejecutar el archivo init.sh
```bash
chmod +x init.sh
./init.sh
```

> ℹ️
>
> El script `init.sh` construirá las imagenes de Docker de forma local y levantará el ambiente de desarrollo como pods de Kubernetes.

**4.** Verificar que los pods estén corriendo
```bash
kubectl get pods
```

**5.** Acceder a la aplicación
```bash
# Acceder a la aplicación en el navegador
http://localhost:30080
```

**Extra.** Si se desea verificar de forma gráfica el estado del API, se puede acceder al endpoint `/` de la aplicación:
```bash
# Acceder al endpoint de la aplicación en el navegador
http://localhost:30500/
```