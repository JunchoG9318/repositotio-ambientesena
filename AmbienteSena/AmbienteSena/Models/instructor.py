from django.db import models


class Instructor(models.Model):
    NombreCompleto = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    Celular = models.CharField(max_length=20)
    Cedula = models.IntegerField()

    elementos = models.ManyToManyField(
        'AmbienteSena.Elemento',
        through='AmbienteSena.cuentadante',
        related_name= 'instructores'
    )

    class Meta:
        db_table ='instructor'
