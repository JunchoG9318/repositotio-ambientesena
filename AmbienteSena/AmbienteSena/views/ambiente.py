from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from AmbienteSena.Models.ambiente import Ambiente


def RegistrarAmbiente(request):
    if request.method == 'POST':
        ## Validacion de datos al frontend##
        if request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observacion'):
            ## Definicion de Variables##
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            observacion = request.POST.get('observacion')
            ## Conexion a base de datos##
            try:
                ambiente = Ambiente
                ambiente.NombreAmbiente = nombre
                ambiente.TipoAmbiente = tipo
                ambiente.Observaciones = observacion
                Ambiente.save()
                messages.success(
                    request, 'Ambiente de formacion registrado correctamente')
            except Exception as e:
                messages.error(
                    request, 'Ocurrio un error en el sisteme. Intentelo mas tarde')
            return redirect('/Ambientes/ListaAmbientes')
    else:
        return render(request, 'Ambientes/RegistrarAmbiente.html')

### Consultar Ambientes de Formaciom###


def ListarAmbientes(request):
    try:
        ListarAmbientes = Ambiente.objects.all()
    except Exception as e:
        messages.error(request, 'Ocurrio un error en el sistema')
        return render(request, 'Ambientes/ListaAmbientes.html')
    return render(request, 'Ambientes/ListaAmbientes.html', {'ambientes': ListarAmbientes})


def EliminarAmbiente(request):
    if request.method == 'POST':
        try:
            # Obtener el id desde el formulario
            ambiente=Ambiente.objects.get(id=request.POST.get('id'))

            # Usar with para asegurar el cierre del cursor
            ambiente.delete()
            messages.success(request, "Ambiente de formación eliminado correctamente")
        except Exception as e:
            # Mensaje de error con el detalle real (opcional, puedes dejarlo genérico)
            messages.error(request, f"Ocurrió un error en el sistema: {e}")
        return redirect('/Ambientes/ListaAmbientes')
    else:
        # Si alguien intenta acceder por GET, redirigir a la lista
        return redirect('/Ambientes/ListaAmbientes')

#### ESTO ES PARA EDITAR UN AMBIENTE DE FORMACION EN LA BASE DE DATOS###
def ActualizarAmbiente(request, id_ambiente):
    if request.method == 'POST':
        try:
            ambiente = Ambiente.objects.get(id=id_ambiente)
            ambiente.NombreAmbiente = request.POST.get('nombre')
            ambiente.TipoAmbiente = request.POST.get('tipo')
            ambiente.Observaciones = request.POST.get('observacion')
            ambiente.save()
            messages.success(request, "ambiente actualizado correctamente")
        except Exception as e:
            messages.error(
                request, "surgio un error en el sistema. Purbe mas tarde")
        return redirect('/Ambientes/ListaAmbientes')
    else:
        try:
            ambiente = Ambiente.objects.get(id=id_ambiente)
            return render(request, 'Ambientes/ActualizarAmbiente.html', {'ambiente': ambiente})
        except Exception as e:
            messages.error(request, 'error en el sistemaaaaa')
            return redirect('/Ambientes/ListaAmbientes')
