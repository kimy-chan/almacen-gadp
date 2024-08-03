
from django.contrib.auth.models import AbstractBaseUser , UserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.db import models
from  persona.models import Persona






    




class Secretaria(models.Model):
    secretaria = models.CharField(max_length=100, blank=False , null=False, unique=True)
    def __str__(self) -> str:
        return f"{self.secretaria}"
    

class Unidad(models.Model):
    nombre =models.CharField(max_length=100,blank=False, null=False, unique=True )
    secretaria=models.ForeignKey(Secretaria, on_delete=models.RESTRICT, blank= True, null=True)
    def __str__(self) -> str:
        return f"{self.nombre}"
    
class Oficinas(models.Model):
    nombre =models.CharField(max_length=100,blank=False, null=False, unique=True)
    unidad=models.ForeignKey(Unidad, on_delete=models.RESTRICT, blank= True, null=True)
    def __str__(self) -> str:
        return f"{self.nombre}"
    
@receiver(post_migrate)
def crear_entidades_por_defecto(sender, **kwargs):
    if sender.name == 'usuarios':
        secretaria, created = Secretaria.objects.get_or_create(secretaria='Secretaria departamental administrativa financiera')
        unidad, created = Unidad.objects.get_or_create(nombre='Financiera', secretaria=secretaria)
        Oficinas.objects.get_or_create(nombre='Ninguna', unidad=unidad)
        Oficinas.objects.get_or_create(nombre='Almacenes', unidad=unidad)
      

    
class Usuario(AbstractBaseUser, PermissionsMixin):
    ENCARGADO=[
        (True,'Encargado'),
        (False,'Personal')
    ]
    ROLES_CHOICES=[
        ('Administrador','Administrador'),
        ('Super_administrador','Super administrador'),
        ('Axuliar','Axuliar'),
        ('Personal','Personal')
    ]
    username= models.CharField(max_length=150, unique=True, blank=False, null=False, verbose_name='Usuario')
    password = models.CharField(max_length=128, blank=False, null=False, verbose_name='Contraseña')
    email=models.EmailField(max_length=255, blank=True, null=True)
    item = models.CharField(max_length=100, blank=True, null=True)
    is_staff= models.CharField(default=True)#desactivar usuario
    encargado=models.BooleanField(blank=False, null=False, choices=ENCARGADO, default=False, verbose_name='Jefe  de la secretaria' ) 
    crear = models.BooleanField(default=False,verbose_name='Crear material')
    editar= models.BooleanField(default=False,verbose_name='editar material')
    eliminar=models.BooleanField(default=False,verbose_name='Eliminar material')
    rol=models.CharField(max_length=250, choices=ROLES_CHOICES, default='Personal')
    unidad= models.ForeignKey(Unidad, on_delete=models.RESTRICT,blank=True, null=True)
    oficina= models.ForeignKey(Oficinas, on_delete=models.RESTRICT,blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.RESTRICT)

    es_habilitado=models.BooleanField(default=True)
    es_activo=models.BooleanField(default=True)

    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['rol']
    def __str__(self) -> str:
        return f" Activo:{self.es_activo}"
