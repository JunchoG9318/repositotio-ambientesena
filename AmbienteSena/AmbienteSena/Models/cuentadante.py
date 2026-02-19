from django.db import models

class Cuentadante(models.Model):
    instructor = models.ForeignKey('AmbienteSena.Instructor',on_delete = models.RESTRICT)
    elemento = models.ForeignKey('AmbienteSena.Elemento', on_delete = models.RESTRICT)
    observaciones = models.TextField(blank=True)
    fechaasignacion = models.DateField(auto_now=True)

    class Meta:
        db_table = 'cuentadante'
        ##PARA EVITAR DUPLICADOS##
        unique_together = ('instructor', 'elemento')