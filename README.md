# PruebaNTSeccion1

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Yes-blue)](https://www.docker.com/)

## Descripción
Este proyecto implementa un **ETL (Extract, Transform, Load)** de un dataset de compras y una **aplicación web con Flask** para visualizar los totales diarios por compañía.  
Se incluyen **Docker y Docker Compose** para facilitar la instalación y ejecución de todo el entorno.

El proyecto tiene dos secciones:  

1. Procesamiento y transformación de datos (ETL).  
2. Visualización de resultados a través de una página web.

---

## Requisitos
- Docker  
- Docker Compose  
- Python 3.13 (opcional, solo para ejecutar localmente sin Docker)

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Jorge-laureano/PruebaNTSeccion1.git
cd PruebaNTSeccion1

# 2. Ejecutar con Docker Compose
# Esto iniciará MySQL y Flask automáticamente, y ejecutará el ETL antes de levantar la app
docker-compose up --build

# La app Flask estará disponible en: http://localhost:5000
# MySQL escuchará en el puerto 3306

# 3. Ejecutar localmente (opcional)
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
