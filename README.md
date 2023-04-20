# API consultar UF en sitio del SII :dollar:

Servicio para consultar valores de la Unidad de Fomento para una fecha específica del portal https://www.sii.cl/valores_y_fechas/uf/uf2021.htm y exponerlo como API.

Para obtener un breve resumen del funcionamiento, consulte el documento DOC.md.

## Pruebas automáticas

El archivo de pruebas y health-check del servicio esta alojado en el directorio mic_serv_uf_chile/test.

Una vez el servicio se encuentre en ejecución, puede ingresar al prompt del container y ejecutar el siguiente comando en el directorio (/.venv/lib/python3.9/site-packages/mic_serv_uf_chile/tests) para validar el set de pruebas.

    pytest api_tests.py --disable-warnings -s

A continuación, instrucciones para la puesta en marcha del servicio en sus servidores/local.

## Sincronizar `setup.py`

Es necesario mantener al dia el archivo setup.py con las dependencias que se instalen, para hacer la sincronización
ejecute `pipenv-setup sync` dentro del ambiente virtual del microservicio.

## Linters y hooks de pre commit

Se agregaron varios linters en la sección de paquetes de dev:

* black https://black.readthedocs.io/en/stable/
* pylint http://pylint.pycqa.org/en/latest/
* mypy https://mypy.readthedocs.io/en/stable/
* pydocstyle http://www.pydocstyle.org/en/stable/
* pycodestyle https://pycodestyle.pycqa.org/en/latest/

Para manejar los hooks de pre commit se está usando https://pre-commit.com/ que se va a instalar con los paquetes de dev
de Pipfile, los linters que se están aplicando en el hook son: pylint, pydocstyle, pycodestyle.

Active los hooks de pre commit, haciendo `pre-commit install`, esto evaluará el código antes de llevar a cabo el commit
para asegurar la limpieza y el apego a los estándares del código.

Los linters se pueden aplicar por separado, ejecutándolos desde la línea de comando dentro del ambiente virtual. Para
más information sobre su uso consulte la página que corresponda al linter que desee usar.

## Correr con docker

1.  Instale pipenv y pipenv-setup:

    ```
    pip install pipenv pipenv-setup
    ```
2.  Establecer configuración del micro:

    Renombrar archivos 
    1. instance/envs/micro.example.env -> instance/envs/micro.env
    2. instance/etc/config.example.yml -> instance/etc/config.yml
    
3.  Luego localice el archivo create_docker_image.sh y ejecutelo.
 
    Con los siguientes flags puede especificar etiquetas para la imagen resultante: 
    1.  `-v <major.mid.minor>`: Indica la version de la imagen y debe coincidir con la version que esta especificado en el setup.py. Este flag es obligatorio.
    2.  `-l`: Crea una imagen adicional tageada con latest. No es un tag obligatorio.

    ```
    bash create_docker_image.sh
    ```

    Lo anterior creara una imagen con el siguiente nombre `mic_serv_uf_chile` y con las etiquetas 1.0.0 y/o latest

4. Seguidamente ejecute el comando con el enviroment correspondiente (dev, dev-without-redis) `bash up.sh -e dev`
5. Esto bajara las imagenes externas y construira los contenedores asociados a cada imagen.

Autor: 

Leonardo González - gonzalezrujano@gmail.com
