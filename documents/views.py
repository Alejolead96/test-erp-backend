import uuid
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


from documents.services.s3_service import generate_presigned_upload_url, download_from_s3
from .serializers import CompanySerializer,BusinessEntitySerializer,DocumentSerializer,ValidationFlowSerializer,ValidationStepSerializer
from .models import Company,BusinessEntity,Document,ValidationFlow,ValidationStep


@extend_schema_view(
    list=extend_schema(
        summary="Listar empresas",
        description="Obtiene la lista de todas las empresas registradas en el sistema",
        tags=["Empresas"]
    ),
    create=extend_schema(
        summary="Crear empresa",
        description="Crea una nueva empresa en el sistema",
        tags=["Empresas"]
    ),
    retrieve=extend_schema(
        summary="Obtener empresa",
        description="Obtiene los detalles de una empresa específica",
        tags=["Empresas"]
    ),
    update=extend_schema(
        summary="Actualizar empresa",
        description="Actualiza completamente los datos de una empresa",
        tags=["Empresas"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente empresa",
        description="Actualiza parcialmente los datos de una empresa",
        tags=["Empresas"]
    ),
    destroy=extend_schema(
        summary="Eliminar empresa",
        description="Elimina una empresa del sistema",
        tags=["Empresas"]
    )
)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar entidades de negocio",
        description="Obtiene la lista de todas las entidades de negocio (vehículos, empleados, etc.)",
        tags=["Entidades de Negocio"]
    ),
    create=extend_schema(
        summary="Crear entidad de negocio",
        description="Crea una nueva entidad de negocio",
        tags=["Entidades de Negocio"]
    ),
    retrieve=extend_schema(
        summary="Obtener entidad de negocio",
        description="Obtiene los detalles de una entidad de negocio específica",
        tags=["Entidades de Negocio"]
    ),
    update=extend_schema(
        summary="Actualizar entidad de negocio",
        description="Actualiza completamente los datos de una entidad de negocio",
        tags=["Entidades de Negocio"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente entidad de negocio",
        description="Actualiza parcialmente los datos de una entidad de negocio",
        tags=["Entidades de Negocio"]
    ),
    destroy=extend_schema(
        summary="Eliminar entidad de negocio",
        description="Elimina una entidad de negocio del sistema",
        tags=["Entidades de Negocio"]
    )
)
class BusinessEntityViewSet(viewsets.ModelViewSet):
    queryset = BusinessEntity.objects.all()
    serializer_class = BusinessEntitySerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar flujos de validación",
        description="Obtiene la lista de todos los flujos de validación configurados",
        tags=["Flujos de Validación"]
    ),
    create=extend_schema(
        summary="Crear flujo de validación",
        description="Crea un nuevo flujo de validación para documentos",
        tags=["Flujos de Validación"]
    ),
    retrieve=extend_schema(
        summary="Obtener flujo de validación",
        description="Obtiene los detalles de un flujo de validación específico",
        tags=["Flujos de Validación"]
    ),
    update=extend_schema(
        summary="Actualizar flujo de validación",
        description="Actualiza completamente un flujo de validación",
        tags=["Flujos de Validación"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente flujo de validación",
        description="Actualiza parcialmente un flujo de validación",
        tags=["Flujos de Validación"]
    ),
    destroy=extend_schema(
        summary="Eliminar flujo de validación",
        description="Elimina un flujo de validación del sistema",
        tags=["Flujos de Validación"]
    )
)
class ValidationFlowViewSet(viewsets.ModelViewSet):
    queryset = ValidationFlow.objects.all()
    serializer_class = ValidationFlowSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar pasos de validación",
        description="Obtiene la lista de todos los pasos de validación",
        tags=["Pasos de Validación"]
    ),
    create=extend_schema(
        summary="Crear paso de validación",
        description="Crea un nuevo paso dentro de un flujo de validación",
        tags=["Pasos de Validación"]
    ),
    retrieve=extend_schema(
        summary="Obtener paso de validación",
        description="Obtiene los detalles de un paso de validación específico",
        tags=["Pasos de Validación"]
    ),
    update=extend_schema(
        summary="Actualizar paso de validación",
        description="Actualiza completamente un paso de validación",
        tags=["Pasos de Validación"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente paso de validación",
        description="Actualiza parcialmente un paso de validación",
        tags=["Pasos de Validación"]
    ),
    destroy=extend_schema(
        summary="Eliminar paso de validación",
        description="Elimina un paso de validación del sistema",
        tags=["Pasos de Validación"]
    )
)
class ValidationStepViewSet(viewsets.ModelViewSet):
    queryset = ValidationStep.objects.all()
    serializer_class = ValidationStepSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Listar documentos",
        description="Obtiene la lista de todos los documentos subidos al sistema con sus estados de validación",
        tags=["Documentos"]
    ),
    create=extend_schema(
        summary="Crear documento y obtener URL de subida",
        description="""
        Crea un nuevo documento en el sistema y genera una URL presignada de S3 para subir el archivo.
        
        **Proceso:**
        1. Se crea el registro del documento en la base de datos
        2. Se genera una URL presignada de S3 para subir el archivo
        3. Se configura el flujo de validación si está habilitado
        
        **Respuesta:**
        - `document`: Datos del documento creado
        - `upload_url`: URL presignada para subir el archivo (método PUT)
        - `upload_method`: Método HTTP a usar (PUT)
        - `content_type`: Tipo de contenido del archivo
        
        **Para subir el archivo:**
        - Método: PUT
        - URL: La URL devuelta en `upload_url`
        - Headers: `Content-Type: {content_type}`
        - Body: Archivo en formato binary
        """,
        tags=["Documentos"],
        examples=[
            OpenApiExample(
                'Documento con validación',
                value={
                    "document_data": {
                        "name": "contrato-empleado.pdf",
                        "mime_type": "application/pdf",
                        "size_bytes": 1024000
                    },
                    "entity_data": {
                        "entity_type": "employee",
                        "entity_id": "8b2e4f1a-9c3d-4e5f-b6a7-1d8e9f0a2b3c"
                    },
                    "company_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "validation_flow_data": {
                        "enabled": True,
                        "steps": [
                            {
                                "order": 1,
                                "approver_user_id": "user-1-uuid",
                                "description": "Revisión de RRHH"
                            },
                            {
                                "order": 2,
                                "approver_user_id": "user-2-uuid",
                                "description": "Aprobación gerencial"
                            }
                        ]
                    },
                    "created_by": "admin-user-uuid"
                }
            ),
            OpenApiExample(
                'Documento sin validación',
                value={
                    "document_data": {
                        "name": "factura-123.pdf",
                        "mime_type": "application/pdf",
                        "size_bytes": 512000
                    },
                    "entity_data": {
                        "entity_type": "vehicle",
                        "entity_id": "2153fb24-334c-4b53-a4ed-a5181396e27b"
                    },
                    "company_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                    "validation_flow_data": {
                        "enabled": False
                    },
                    "created_by": "admin-user-uuid"
                }
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Obtener documento",
        description="Obtiene los detalles completos de un documento específico incluyendo su estado de validación",
        tags=["Documentos"]
    ),
    update=extend_schema(
        summary="Actualizar documento",
        description="Actualiza completamente los metadatos de un documento",
        tags=["Documentos"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente documento",
        description="Actualiza parcialmente los metadatos de un documento",
        tags=["Documentos"]
    ),
    destroy=extend_schema(
        summary="Eliminar documento",
        description="Elimina un documento del sistema y de S3",
        tags=["Documentos"]
    )
)
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            company_id = request.data.get('company_id')
            entity_data = request.data.get('entity')
            document_data = request.data.get('document')
            validation_flow_data = request.data.get('validation_flow')


            if not company_id or not entity_data or not document_data:
                return Response({'error': 'Missing required fields: company_id, entity, document'}, status=400)

            if document_data.get('size_bytes', 0) > 10 * 1024 * 1024:
                return Response({'error': 'File size exceeds 10MB limit'}, status=400)

            allowed_mimes = [
                'application/pdf', 'image/jpeg', 'image/png', 'image/jpg', 
                'application/msword', 
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
            if document_data.get('mime_type') not in allowed_mimes:
                return Response({'error': f'MIME type not allowed. Allowed: {", ".join(allowed_mimes)}'}, status=400)

            
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return Response({'error': f'Company with id {company_id} does not exist'}, status=400)

            
            try:
                business_entity = BusinessEntity.objects.get(id=entity_data['entity_id'])
            except BusinessEntity.DoesNotExist:
                return Response({'error': f'BusinessEntity with id {entity_data["entity_id"]} does not exist'}, status=400)
            except KeyError:
                return Response({'error': 'entity_id is required in entity data'}, status=400)

            
            bucket_key = document_data.get('bucket_key')
            if not bucket_key:
                entity_type = entity_data.get('entity_type', 'entity')
                bucket_key = f'companies/{company_id}/{entity_type}s/{entity_data["entity_id"]}/docs/{uuid.uuid4()}-{document_data.get("name")}'

            has_validation = validation_flow_data.get('enabled', False) if validation_flow_data else False
            initial_status = Document.STATUS.PENDING if has_validation else None
            
            upload_url = generate_presigned_upload_url(
                bucket_key=bucket_key,
                content_type=document_data['mime_type'],
            )
            
            
            document = Document.objects.create(
                name=document_data['name'],
                mime_type=document_data['mime_type'],
                size_bytes=document_data['size_bytes'],
                bucket_key=bucket_key,
                company=company,
                business_entity=business_entity,
                status=initial_status,
                created_by=request.data.get('created_by')
            )

            
            if has_validation and validation_flow_data.get('steps'):
                validation_flow = ValidationFlow.objects.create(document=document, enable=True)
                
                for step_data in validation_flow_data['steps']:
                    ValidationStep.objects.create(
                        order=step_data['order'],
                        approver_user_id=step_data['approver_user_id'],
                        validation_flow=validation_flow
                    )

            serializer = self.serializer_class(document)
            response_data = {
                'document': serializer.data,
                'upload_url': upload_url,
            }
            
            return Response(response_data, status=201)

        except Exception as e:
            return Response({'error': f'Failed to create document: {str(e)}'}, status=500)

    @extend_schema(
        summary="Descargar documento",
        description="""
        Genera una URL presignada para descargar un documento desde S3.
        
        **Requisitos:**
        - El documento debe existir
        - El documento debe estar aprobado (si tiene flujo de validación)
        
        **Respuesta:**
        - `download_url`: URL presignada válida por 1 hora para descargar el archivo
        """,
        tags=["Documentos"],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'download_url': {
                        'type': 'string', 
                        'format': 'uri',
                        'description': 'URL presignada para descargar el archivo'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensaje de error'
                    }
                }
            },
            404: {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Documento no encontrado'
                    }
                }
            }
        }
    )
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        document = self.get_object()
    
        if document.status != Document.STATUS.APPROVED:
            return Response({'error': 'Document is not available for download'}, status=400)
    
        try:
            url = download_from_s3(document.bucket_key)
            return Response({'download_url': url}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @extend_schema(
        summary="Aprobar documento",
        description="""
        Aprueba un paso específico del flujo de validación de un documento.
        
        **Proceso:**
        1. Valida que el usuario tenga permisos para aprobar
        2. Verifica que el paso esté pendiente
        3. Marca el paso como aprobado
        4. Si es el último paso, aprueba todo el documento
        5. Deshabilita el flujo de validación al completarse
        
        **Estados del documento:**
        - `PENDING`: Documento en proceso de validación
        - `APPROVED`: Documento completamente aprobado
        """,
        tags=["Validación de Documentos"],
        request={
            'type': 'object',
            'properties': {
                'approver_user_id': {
                    'type': 'string', 
                    'format': 'uuid', 
                    'description': 'ID del usuario que aprueba el documento'
                },
                'reason': {
                    'type': 'string', 
                    'description': 'Razón de la aprobación (opcional)',
                    'example': 'Documento revisado y cumple con todos los requisitos'
                }
            },
            'required': ['approver_user_id']
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'enum': ['Step approved', 'Document approved'],
                        'description': 'Resultado de la aprobación'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            },
            403: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            },
            404: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        examples=[
            OpenApiExample(
                'Aprobar paso intermedio',
                value={
                    'approver_user_id': 'f47ac10b-58cc-4372-a567-0e02b2c3d479',
                    'reason': 'Documento revisado por RRHH - Aprobado'
                }
            ),
            OpenApiExample(
                'Aprobar paso final',
                value={
                    'approver_user_id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
                    'reason': 'Aprobación gerencial final'
                }
            )
        ]
    )
    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        document = self.get_object()
        approver_user_id = request.data.get('approver_user_id')
        reason = request.data.get('reason', '')

        if not approver_user_id:
            return Response({'error': 'Actor user ID is required'}, status=400)

        flow = document.validation_flow

        if not flow or not flow.enable:
            return Response({'error': 'Validation flow is not enabled'}, status=400)

        try:
            step = flow.steps.get(approver_user_id=approver_user_id)
        except ValidationStep.DoesNotExist:
            return Response({
                'error': f'User {approver_user_id} is not authorized to approve this document'
            }, status=403)

        if step.status != ValidationStep.STATUS.PENDING:
            return Response({'error': 'Your validation step is not pending'}, status=400)

        order = step.order
        total_steps = flow.steps.count()
        
        if order == total_steps:
            for s in flow.steps.filter(order__lte=order):
                s.status = ValidationStep.STATUS.APPROVED
                if s.order == order:
                    s.reason = reason
                s.save()
            document.status = Document.STATUS.APPROVED
            document.save()
            document.validation_flow.enable = False
            document.validation_flow.save()
            return Response({'message': 'Document approved'}, status=200)
        else:
            steps_to_approve = flow.steps.filter(order__lte=order)
            for s in steps_to_approve:
                s.status = ValidationStep.STATUS.APPROVED
                if s.order == order:
                    s.reason = reason
                s.save()
            return Response({'message': 'Step approved'}, status=200)


    @extend_schema(
        summary="Rechazar documento",
        description="""
        Rechaza un documento en cualquier paso del flujo de validación.
        
        **Proceso:**
        1. Valida que el usuario tenga permisos para rechazar
        2. Verifica que el paso esté pendiente
        3. Marca el paso como rechazado
        4. Marca todo el documento como rechazado
        5. Deshabilita el flujo de validación
        
        **Importante:** 
        - Un rechazo detiene todo el flujo de validación
        - El documento queda en estado `REJECTED` permanentemente
        - Se requiere obligatoriamente una razón del rechazo
        """,
        tags=["Validación de Documentos"],
        request={
            'type': 'object',
            'properties': {
                'approver_user_id': {
                    'type': 'string', 
                    'format': 'uuid', 
                    'description': 'ID del usuario que rechaza el documento'
                },
                'reason': {
                    'type': 'string', 
                    'description': 'Razón obligatoria del rechazo',
                    'example': 'El documento no cumple con los requisitos de formato establecidos'
                }
            },
            'required': ['approver_user_id', 'reason']
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'enum': ['Document rejected'],
                        'description': 'Confirmación del rechazo'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            },
            403: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            },
            404: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        examples=[
            OpenApiExample(
                'Rechazar por formato incorrecto',
                value={
                    'approver_user_id': 'f47ac10b-58cc-4372-a567-0e02b2c3d479',
                    'reason': 'El documento no está en formato PDF como se requiere'
                }
            ),
            OpenApiExample(
                'Rechazar por contenido incompleto',
                value={
                    'approver_user_id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
                    'reason': 'Faltan firmas requeridas en el contrato'
                }
            )
        ]
    )
    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        document = self.get_object()
        approver_user_id = request.data.get('approver_user_id')
        reason = request.data.get('reason', '')

        if not approver_user_id:
            return Response({'error': 'Approver user ID is required'}, status=400)

        if not reason:
            return Response({'error': 'Reason is required for rejection'}, status=400)

        flow = document.validation_flow
        if not flow or not flow.enable:
            return Response({'error': 'Validation flow is not enabled'}, status=400)

        try:
            step = flow.steps.get(approver_user_id=approver_user_id)
        except ValidationStep.DoesNotExist:
            return Response({
                'error': f'User {approver_user_id} is not authorized to reject this document'
            }, status=403)

        if step.status != ValidationStep.STATUS.PENDING:
            return Response({'error': 'Your validation step is not pending'}, status=400)

  
        step.status = ValidationStep.STATUS.REJECTED
        step.reason = reason
        step.save()


        document.status = Document.STATUS.REJECTED
        document.save()

        flow.enable = False
        flow.save()

        return Response({'message': 'Document rejected'}, status=200)

















 
        


