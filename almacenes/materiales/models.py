from django.db import models


class Categoria(models.Model):
    codigo_clasificacion = models.CharField(max_length=100, unique=True , blank=False, null=False, error_messages={'unique':'El codigo de la categoria ya existe'})
    nombre= models.CharField(max_length=200, blank=False, unique=True, null=False, error_messages={'unique':'El nombre de la categoria ya existe'})
    fecha_creacion= models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.nombre},{self.codigo_clasificacion}, {self.fecha_creacion}"

class Materiales(models.Model):
    nombre = models.CharField(max_length=255,blank=False, null=False,)
    codigo = models.CharField(max_length=255, blank=False, null=False, unique=True,  error_messages={'unique':'El codigo de producto ya existe'})
    marca = models.CharField(max_length=255, blank=False, null=False)
    cantidad_paquete=models.IntegerField(blank=False, null=False, verbose_name='Cantidad por paquetes')
    cantidad_paquete_unidad = models.IntegerField(blank=False, null=False,verbose_name='Cantidad por paquetes (en unidades)')
    stock = models.IntegerField(null=True, blank=True)
    precio_paquete = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False,verbose_name='Precio por paquetes')
    precio_unidad=models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False,verbose_name='Precio por Unidad')
    total_precio= models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    tamaño = models.CharField(max_length=255,blank=True, null=True)
    color = models.CharField(max_length=100,blank=True, null=True)
    unidad_medida = models.CharField(max_length=255,blank=True, null=True, verbose_name='Unidad de medida')
    material = models.CharField(max_length=255,blank=True, null=True)
    codigo_paquete = models.CharField(max_length=255, unique=True, blank=True, null=True,  error_messages={'unique':'El codigo ya existe'}, verbose_name='Codigo de paquete')
    categoria =models.ForeignKey(Categoria, models.CASCADE,blank=False, null=False )
    es_habilitado=models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"""{self.nombre},{self.codigo},{self.marca},
        {self.cantidad_paquete_unidad},{self.cantidad_paquete},{self.fecha_creacion},
        {self.tamaño},{self.unidad_medida},{self.material},{self.codigo_paquete},{self.categoria}"""

    def calcular_total_paquetes(self):
        self.stock= self.cantidad_paquete * self.cantidad_paquete_unidad
        self.save()
    def calcular_precio_total(self):
        self.total_precio= self.precio_paquete * self.precio_unidad
        self.save()