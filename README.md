# Trabajo práctico final: Enriquecimiento de anotaciones GO
CLI que permite comparar y enriquecer de proteínas homólogas

## Integrantes:

* Enrique Alonso.
* Lucas Alvarez.
* Gaston Da Silva.

## Instalación

### Prerrequisitos

Asegúrate de tener Python 3 instalado en tu sistema. Puedes verificar la versión de Python instalada con el siguiente comando:

```sh
python3 --version
```

### Pasos a seguir

1. Clona el repositorio (o descarga el código fuente):

```bash
git clone https://github.com/BioinformaticaUNQ/EnriquecimientoAnotacionesGO.git
cd EnriquecimientoAnotacionesGO
```

2. Crea un entorno virtual:

```bash
python3 -m venv venv  
```

3. Activa el entorno virtual:
```bash
source venv/bin/activate
```

4. Instala dentro del entorno virtual las dependencias configuradas en el archivo requeriments.txt

```bash
pip install -r requeriments.txt
```


## Uso

Podes ejecutar con los siguientes comandos:

query-protein [codigoUniprot]
Retorna una secuencia de aminoacidos para la proteina solicitada.

run-blast [proteina] [baseDeDatos] 
Ejecuta una corrida blast y retorna los resultados de tal corrida.

get-goterms[codigoUniprot]
Retorna los terminos go para una proteina.