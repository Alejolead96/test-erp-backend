from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Company(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class BusinessEntity(models.Model):

    class ENTITY_TYPE(models.TextChoices):
        VEHICLE = 'V', 'Vehicle'
        EMPLOYEE = 'E', 'Employee'
        OTHER = 'O', 'Other'

    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=1 , choices=ENTITY_TYPE.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='entities')

class Document(models.Model):

    class STATUS(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    size_bytes = models.PositiveBigIntegerField(validators=[MinValueValidator(0)])
    bucket_key = models.CharField(max_length=1250, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1, 
        choices=STATUS.choices, 
        null=True,
        blank=True,
        default=None
    )
    created_by = models.UUIDField(null=True, blank=True)

    business_entity = models.ForeignKey(BusinessEntity, on_delete=models.PROTECT, related_name='documents')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='documents')


class ValidationFlow(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='validation_flow')

class ValidationStep(models.Model):

    class STATUS(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.PositiveIntegerField()
    approver_user_id = models.CharField(blank=True, null=True)
    status =  models.CharField(max_length=1, choices=STATUS.choices, default=STATUS.PENDING)
    reason =  models.TextField(blank=True, null=True)
    
    validation_flow = models.ForeignKey(ValidationFlow, on_delete=models.CASCADE, related_name='steps')

    class Meta:
        ordering = ['order']
