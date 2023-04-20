# Planteamiento

Se requiere un servicio hecho en Python que consuma el portal del SII de Chile para obtener los valores de Unidad de Fomento para una fecha específica (Ej. 2020-01-02) y poder exponerlo en un API para consumo de otros servicios.

# Solución

Se observa que el portal del SII permite obtener valores de Unidad de Fomento por año con la siguiente URL:

https://www.sii.cl/valores_y_fechas/uf/uf{anio}.htm

En respuesta a esa consulta, se obtiene un documento HTML que distribuye los valores de las Unidades de Fomento del año consultado, en tablas que representan los meses, y filas que representan los dias.

Para efectos de una extracción eficiente, se enfoco la evaluación de una tabla contenida en todas las respuestas que relaciona los 31 posibles dias de un mes (filas), con los 12 meses de un año (columnas).

# Flujo de extracción

Se consulta la URL anterior discutida con el año al que pertenece la fecha específica, notese que aunque el usuario solicita un valor específico del año, la consulta al SII devuelve todos los valores del año, lo cual sera aprovechado en un sistema de cache de resultados como discutiremos ahora para acelerar el tiempo de respuesta en una magnitud importante, esto tomando en cuenta que estos valores una vez definidos no cambian en el tiempo, son inmutables.

La contenido en texto del archivo HTML consultado con el protocolo HTTP se pasa a la dependencia de TextFSM. La cual es un motor de extracción y formato para salidas de comandos desarrollado por Google para Network Automation. 

Debido a la estructura del archivo HTML, se puede hacer uso de la herramienta TextFSM para propositos de una ágil extracción. Consulte la función parser_sii_html_response(html_response: str) en el archivo mic_serv_uf_chile/adapters/uf_request/sii/parser.py para ver este procedimiento.

Aunque TextFSM hace el extraer los valores del documento HTML una labor rápida e indolora', aun permanecen en un formato no muy gestionable para efectos del servicio.

Al capturar la salida del TextFSM se hace uso de la función format_uf_values(uf_values: List, year: str) en el mismo archivo, para construir una nueva lista con un dataclass model de Python que describe el DataValue que expone el servicio.

Pero el usuario no solicito todos los valores de Unidad de Fomento para el año dado, por lo que se procede a almacenar los valores obtenidos en una instancia de Redis y se devuelven al nivel de la función anterior, que se encargara de filtrar al registro que corresponde a la fecha dada.

Una vez resuelta la extracción, se procede a devolver el valor obtenido por medio del servicio para finalizar el hilo de la petición.

Habrá notado que en aprovechamiento de la instancia de Redis para guardar los valores obtenidos, con 3 consultas de 3 años distintos, se puede dotar al servicio de disponibilidad en cache para los aprox. 1080 registros de Unidad de Fomento que se pueden definir en 3 años.

Con lo anterior, una consulta pasa de un tiempo de respuesta de varios segundos a varios milisegundos con el almacenado en cache.

La función request_uf(date: str) en el archivo mic_serv_uf_chile/adapters/uf_request/sii/__init__.py consulta primero que el valor solicitado no este almacenado en la instancia de Redis antes de iniciar un proceso de extracción al SII.

# Roadmap

Como todo software, siempre quedan abiertos puntos de mejora. Para este caso, se detectaron el desarrollar y/o revisar para futuras iteraciones los siguientes puntos:

- Controlar una excepción cuando por temas de conexión, caída del servicio o cualquier detonante a no alcanzar la web del SII, hacerselo saber al usuario consumidor.

- Estudiar un abanico de validaciones mas riguroso para el parámetro de fecha específica enviado por el usuario. En el caso de ingresar un formato incorrecto que los algoritmos de validación de flask-restx no logre detectar para el iso 8601.

- Agregar a la pruebas automáticas revisión del almacenado en cache de los valores extraídos.

De igual forma se concluye que para el contexto del desarrollo y los objetivos propuestos, el planteamiento actual se acierta con los requerimientos para una primera iteración aprovechable del servicio.