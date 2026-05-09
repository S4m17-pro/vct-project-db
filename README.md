
🛠️ Requisitos Previos
Antes de empezar, asegúrate de tener instalado:

Docker Desktop (o Docker Engine en Linux).

Git.

pgAdmin 4 (para gestionar la base de datos visualmente).

🚀 Configuración Inicial
Clonar el repositorio:

Bash
git clone git@github.com:S4m17-pro/vct-project-db.git
cd vct-project-db
Levantar la infraestructura:
Ejecuta el siguiente comando para iniciar la base de datos. Docker se encargará de crear las tablas automáticamente gracias al script en init-db/:

Bash
docker-compose up -d
Verificación de estado:
Asegúrate de que el contenedor esté corriendo y el puerto 5432 esté libre:

Bash
docker ps
Deberías ver el contenedor vct_postgres_db mapeado al puerto 5432.

🐘 Conexión a pgAdmin
Para conectarte a la base de datos desde pgAdmin, usa estos datos:

Host name/address: localhost

Port: 5432

Maintenance database: vct_stats

Username: admin

Password: password123

📋 Reglas de Trabajo (Workflow)
Para mantener el proyecto organizado mientras avanzamos en el semestre:

Sincronización: Antes de empezar a trabajar, haz siempre un git pull para traer mis cambios.

Bash
git pull origin main
Nuevas Tablas o Cambios: Si necesitas modificar el diseño de la base de datos, edita el archivo en init-db/schema.sql y avísame para reiniciar los volúmenes.

Commits Claros: Usa mensajes descriptivos para tus avances (ej: git commit -m "Agregada tabla de estadísticas de armas").

📁 Estructura del Proyecto
/init-db: Contiene el script schema.sql que inicializa todas las tablas (Agentes, Equipos, Partidas, etc.).

docker-compose.yml: Configuración de la imagen de PostgreSQL.

README.md: Esta guía.
