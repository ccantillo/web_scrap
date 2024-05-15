# API WEB SCRAP SERVICIOS JUDICIALES

## Stack:
- Python 3.11.0
- MySQL
- FastApi
- Selenium
- BS4
- Uvicorn
- Tortoise ORM

## Instalación
1. Clona el repositorio.
2. Instala las dependencias:
    - Ejecuta `pip install -r requirements.txt`

## Ejecutar el API
- Antes de ejecutar el programa, asegúrate de tener creada una base de datos MySQL con el nombre "procesos_judiciales":
  `CREATE DATABASE procesos_judiciales DEFAULT CHARACTER SET utf8mb3 DEFAULT ENCRYPTION='N';`
- Estando en el directorio `api`, ejecuta `python app.py`
- Cuando se ejecute el API, realizará el proceso de scraping automáticamente y guardará en la base de datos los primeros datos.

## Uso del API
- El servidor se iniciará en http://127.0.0.1:8000

### Endpoints:
- `/api/login` - POST: login de la api, el usuario inicial es username: admin password: P@ssW0rd (usuario creado automaticamente al momento de iniciar el api).
- `/api/personas` - GET: Trae lista de personas en la base de datos.
- `/api/personas/{persona_id}` - GET: Trae detalles de una persona.
- `/api/actuaciones` - GET: Trae lista de actuaciones en la base de datos.
- `/api/actuaciones/{actuacion_id}` - GET: Trae detalles de una actuación.
- `/api/causas` - GET: Trae lista de causas en la base de datos.
- `/api/causas/{causa_id}` - GET: Trae detalles de una causa.
- `/api/movimientos` - GET: Trae lista de movimientos en la base de datos.
- `/api/movimientos/{movimiento_id}` - GET: Trae detalles de un movimiento.
- `/api/llenar_informacion` - GET: Permite llenar la información de las identificaciones (0968599020001, 1791251237001, 0992339411001).
- `/api/llenar_informacion/{persona_id}` - GET: Permite llenar información con los datos de la persona que se pase en el endpoint.

- Para más información sobre los endpoints, al momento de ejecutar el API, se podrá acceder a la URL http://127.0.0.1:8000/docs donde podrás observar el Swagger UI con más información. Además, en el directorio raíz del proyecto encontrarás el archivo "datos_judiciales.postman_collection.json" que puedes usar para importar una colección de Postman con los endpoints y más información.

### Tests:
- Estando en el directorio `api`, ejecuta `python -m pytest tests/`