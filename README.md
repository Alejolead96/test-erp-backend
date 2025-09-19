# Storage API - Sistema de Gestión de Documentos

Un sistema completo de gestión de documentos con validación por flujos de aprobación, integrado con Amazon S3 para almacenamiento de archivos.

## 🚀 Características

- **Gestión de Documentos**: Subida, descarga y gestión de documentos con integración S3
- **Sistema de Validación**: Flujos de aprobación con múltiples pasos
- **Entidades de Negocio**: Gestión de vehículos, empleados y otras entidades
- **API REST**: Endpoints completos con documentación Swagger
- **Base de Datos PostgreSQL**: Almacenamiento robusto y escalable
- **Docker**: Configuración lista para desarrollo

## 🛠️ Tecnologías

- **Backend**: Django 5.2.6 + Django REST Framework
- **Base de Datos**: PostgreSQL 15
- **Almacenamiento**: Amazon S3
- **Documentación**: drf-spectacular (Swagger/OpenAPI)
- **Contenedores**: Docker & Docker Compose

## 📋 Requisitos Previos

- Python 3.8+
- Docker y Docker Compose
- Cuenta de AWS con acceso a S3

## ⚙️ Configuración

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd storage
```

### 2. Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=tu_access_key_aqui
AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
AWS_STORAGE_BUCKET_NAME=tu_bucket_name
AWS_S3_REGION_NAME=us-east-1
```

### 3. Instalación con Docker

```bash
# Levantar la base de datos
docker-compose up -d

# Instalar dependencias Python
pip install django djangorestframework psycopg2-binary python-dotenv drf-spectacular boto3

# Ejecutar migraciones
python manage.py migrate

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## 🏗️ Estructura del Proyecto


## 📊 Modelos de Datos

### Company
- Empresas del sistema
- Campos: `id`, `name`, `created_at`

### BusinessEntity
- Entidades de negocio (Vehículos, Empleados, Otros)
- Campos: `id`, `entity_type`, `company`, `created_at`

### Document
- Documentos almacenados en S3
- Estados: `PENDING`, `APPROVED`, `REJECTED`
- Campos: `id`, `name`, `mime_type`, `size_bytes`, `bucket_key`, `status`, etc.

### ValidationFlow
- Flujos de validación para documentos
- Campos: `id`, `enable`, `document`, `created_at`

### ValidationStep
- Pasos individuales de validación
- Estados: `PENDING`, `APPROVED`, `REJECTED`
- Campos: `id`, `order`, `approver_user_id`, `status`, `reason`

## 🔗 Endpoints API

### Base URL: `http://localhost:8000/api/`

#### Empresas
- `GET /companies/` - Listar empresas
- `POST /companies/` - Crear empresa
- `GET /companies/{id}/` - Obtener empresa
- `PUT /companies/{id}/` - Actualizar empresa
- `DELETE /companies/{id}/` - Eliminar empresa

#### Entidades de Negocio
- `GET /entities/` - Listar entidades
- `POST /entities/` - Crear entidad
- `GET /entities/{id}/` - Obtener entidad
- `PUT /entities/{id}/` - Actualizar entidad
- `DELETE /entities/{id}/` - Eliminar entidad

#### Documentos
- `GET /documents/` - Listar documentos
- `POST /documents/` - Crear documento (genera URL de subida S3)
- `GET /documents/{id}/` - Obtener documento
- `GET /documents/{id}/download/` - Descargar documento
- `POST /documents/approve/` - Aprobar documento
- `PUT /documents/{id}/reject/` - Rechazar documento

#### Flujos de Validación
- `GET /validationflows/` - Listar flujos
- `POST /validationflows/` - Crear flujo
- `GET /validationflows/{id}/` - Obtener flujo
- `PUT /validationflows/{id}/` - Actualizar flujo
- `DELETE /validationflows/{id}/` - Eliminar flujo

#### Pasos de Validación
- `GET /validationsteps/` - Listar pasos
- `POST /validationsteps/` - Crear paso
- `GET /validationsteps/{id}/` - Obtener paso
- `PUT /validationsteps/{id}/` - Actualizar paso
- `DELETE /validationsteps/{id}/` - Eliminar paso

## 📚 Documentación API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema JSON**: `http://localhost:8000/api/schema/`

## 🔄 Flujo de Trabajo con Documentos

### 1. Subir Documento

```bash
# 1. Crear documento y obtener URL de subida
POST /api/documents/
{
    "name": "documento.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 1024000,
    "business_entity": "uuid-entidad",
    "company": "uuid-empresa"
}

# 2. Usar la URL presignada para subir el archivo a S3
PUT <presigned_url>
# Body: archivo binario
# Headers: Content-Type: application/pdf
```

### 2. Proceso de Aprobación

```bash
# 1. Crear flujo de validación
POST /api/validationflows/
{
    "document": "uuid-documento",
    "enable": true
}

# 2. Crear pasos de validación
POST /api/validationsteps/
{
    "validation_flow": "uuid-flujo",
    "order": 1,
    "approver_user_id": "user123"
}

# 3. Aprobar documento
POST /api/documents/approve/
{
    "document_id": "uuid-documento",
    "approver_user_id": "user123"
}

# 4. Rechazar documento (si es necesario)
PUT /api/documents/{id}/reject/
{
    "approver_user_id": "user123",
    "reason": "Documento incompleto"
}
```