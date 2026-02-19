from django.db import models
from django.utils import timezone

class Ingreso(models.Model):
    instructor = models.ForeignKey('Instructor', on_delete=models.RESTRICT)  # ✅
    ambiente = models.ForeignKey('Ambiente', on_delete=models.RESTRICT)  # ✅
    observacion = models.CharField(max_length=255, blank=True, null=True)  # ✅ Corregido
    fecha_hora_entrada = models.DateTimeField(default=timezone.now)  # ✅ Corregido
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)  # ✅ Corregido

    class Meta:
        db_table = 'ingreso'