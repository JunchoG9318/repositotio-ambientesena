from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse

from ..Models.ambiente import Ambiente
from ..Models.instructor import Instructor
from ..Models.ingreso import Ingreso

def RegistrarIngresos(request):
    if request.method == 'POST':
        ambiente_id = request.POST.get('ambiente')
        instructor_id = request.POST.get('instructor')
        fecha_hora_entrada = request.POST.get('fecha_hora_entrada')
        fecha_hora_salida = request.POST.get('fecha_hora_salida')
        observacion = request.POST.get('observacion', '')

        try:
            # Verificar si existe el ambiente
            ambiente = get_object_or_404(Ambiente, id=ambiente_id)
            
            # Verificar si existe el instructor
            instructor = get_object_or_404(Instructor, id=instructor_id)
            
            # CREAR EL OBJETO INGRESO SIN VALIDACIÓN DE FECHAS
            ingreso = Ingreso(
                ambiente=ambiente,
                instructor=instructor,
                fecha_hora_entrada=fecha_hora_entrada if fecha_hora_entrada else timezone.now(),
                fecha_hora_salida=fecha_hora_salida if fecha_hora_salida else None,
                observacion=observacion
            )
            
            # Guardar los datos
            ingreso.save()
            messages.success(request, 'Ingreso registrado correctamente')
            return redirect('/Ingresos/ListarIngresos')   
            
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
            return redirect('/Ingresos/RegistrarIngresos')
    
    else:
        listadoambiente = Ambiente.objects.all().order_by('NombreAmbiente')
        listadoinstructor = Instructor.objects.all().order_by('NombreCompleto')
        return render(request, "Ingresos/RegistrarIngresos.html", {
            'ambientes': listadoambiente,
            'instructores': listadoinstructor,
            'now': timezone.now()  # Añadido para el template
        })

# Listar los ingresos
def ListarIngresos(request):
    listadoingresos = Ingreso.objects.filter(fecha_hora_salida__isnull=True).select_related('instructor','ambiente')
    return render(request, 'Ingresos/ListarIngresos.html', {'ingresos': listadoingresos})

# Registrar salida - CORREGIDO
def RegistrarSalida(request):
    if request.method == 'POST':
        try:
            ingreso = get_object_or_404(Ingreso, id=request.POST.get('id'))
            if ingreso.fecha_hora_salida is None:
                ingreso.fecha_hora_salida = timezone.now()
                ingreso.save()
                messages.success(request, 'Salida registrada correctamente')
            else:
                messages.info(request, 'Este ingreso ya tenía una salida registrada')
            
            return redirect('/Ingresos/ListarIngresos')
            
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar la salida: {e}')
            return redirect('/Ingresos/ListarIngresos')
    else:
        # Si no es POST, redirigir a la lista de ingresos
        return redirect('/Ingresos/ListarIngresos')