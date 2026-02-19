from django.db import DatabaseError
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse

from ..Models.instructor import Instructor
from ..Models.elemento import Elemento
from ..Models.cuentadante import Cuentadante

def RegistrarCuentadante(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor')
        elementos_ids = request.POST.getlist('elementos[]')  # Cambiado a elementos[]
        observaciones = request.POST.get('observaciones')

        try:
            # Verificar si existe el instructor
            instructor = get_object_or_404(Instructor, id=instructor_id)

            # Verificar si el usuario seleccionó al menos un elemento
            if not elementos_ids:
                messages.error(request, 'Debe seleccionar al menos un elemento')
                return redirect('/Cuentadante/RegistrarCuentadante')
            
            elementos_asignados = 0
            elementos_ya_asignados = 0
            
            # Recorrer los elementos
            for elemento_id in elementos_ids:
                elemento = get_object_or_404(Elemento, id=elemento_id)
                
                # Verificar si ya existe esta asignación
                if Cuentadante.objects.filter(instructor=instructor, elemento=elemento).exists():
                    messages.warning(request, f"El elemento: '{elemento.Nombre}' ya está asignado al instructor: '{instructor.NombreCompleto}'")
                    elementos_ya_asignados += 1
                    continue
                
                # Crear los objetos cuentadante
                cuentadante = Cuentadante(
                    instructor=instructor,
                    elemento=elemento,
                    observaciones=observaciones
                )
                
                # Guardar los datos
                cuentadante.save()
                elementos_asignados += 1
            
            # Mensaje de éxito
            if elementos_asignados > 0:
                messages.success(request, f'Asignación de {elementos_asignados} elementos realizada correctamente')
            if elementos_ya_asignados > 0:
                messages.info(request, f'{elementos_ya_asignados} elementos ya estaban asignados')

            return redirect('/Cuentadante/ListarCuentadante')   
            
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
            return redirect('/Cuentadante/RegistrarCuentadante')
    
    else:
        ListadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
        ListadoElementos = Elemento.objects.all().order_by('Nombre')
        return render(request, "Cuentadante/RegistrarCuentadante.html", 
                     {'instructores': ListadoInstructores, 'elementos': ListadoElementos})

### Listar los cuentadantes ###
def ListarCuentadantes(request):
    listadoElementos = Elemento.objects.all().order_by('Nombre')
    listadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
    listadoCuentadantes = Cuentadante.objects.select_related('instructor', 'elemento').all().order_by('instructor__NombreCompleto', 'elemento__Nombre')
    return render(request, 'Cuentadante/ListarCuentadante.html', 
                 {'cuentadantes': listadoCuentadantes, 'elementos': listadoElementos, 'instructores': listadoInstructores})

### ELIMINAR CUENTADANTE ###
def EliminarCuentadante(request):
    if request.method == 'POST' and request.POST.get('id'):
        try:
            cuentadante = Cuentadante.objects.get(id=request.POST.get('id'))
            cuentadante.delete()
            messages.success(request, 'Cuentadante eliminado correctamente')
        except DatabaseError as e:
            messages.error(request, f"Ocurrió un error en el sistema: {e}")
        return redirect('/Cuentadante/ListarCuentadante')
    else:
        return redirect('/Cuentadante/ListarCuentadante')

def APIConsultarCuentadante(request, id_cuentadante):
    try:
        unCuentadante = Cuentadante.objects.filter(id=id_cuentadante)
        cuentadante_json = serialize('json', unCuentadante)
        return HttpResponse(cuentadante_json, content_type='application/json')
    except Exception as e:
        return HttpResponse(f'{{"error": "{str(e)}"}}', content_type='application/json', status=400)

def ActualizarCuentadante(request):
    if request.method == 'POST':
        cuentadante_id = request.POST.get('id_cuentadante')
        instructor_id = request.POST.get('instructor')
        elemento_id = request.POST.get('elementos')
        observaciones = request.POST.get('observaciones')
        
        # Validar que todos los campos estén presentes
        if not all([cuentadante_id, instructor_id, elemento_id, observaciones]):
            messages.warning(request, 'Debe diligenciar todos los campos')
            return redirect('/Cuentadante/ListarCuentadante')
        
        try:
            cuentadante = Cuentadante.objects.get(id=cuentadante_id)
            cuentadante.observaciones = observaciones
            cuentadante.elemento_id = elemento_id
            cuentadante.instructor_id = instructor_id
            cuentadante.save()
            messages.success(request, 'Cuentadante actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Ocurrió un error en el sistema: {e}')
        
        return redirect('/Cuentadante/ListarCuentadante')
    else:
        return redirect('/Cuentadante/ListarCuentadante')