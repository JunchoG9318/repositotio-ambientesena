import os
import uuid

from django.core.serializers import serialize
from django.http import HttpResponse

from django.db import DatabaseError
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from AmbienteSena import settings
from AmbienteSena.Models.ambiente import Ambiente
from AmbienteSena.Models.elemento import Elemento


def RegistrarElemento(request):
    ambientes = Ambiente.objects.all().order_by('NombreAmbiente')
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('tipo') and request.FILES.get('foto') and request.POST.get('observaciones') and request.POST.get('ambiente'):
            try:
                ambiente = Ambiente.objects.get(id=request.POST.get('ambiente'))
                elemento = Elemento()
                elemento.Nombre = request.POST.get('nombre')
                elemento.Tipo = request.POST.get('tipo')
                elemento.Observaciones = request.POST.get('observaciones')
                elemento.ambiente = ambiente
                elemento.Foto = request.FILES.get('foto')
                ## manejo de django para guardar imagenes##
                imagen = FileSystemStorage(location='AmbienteSena/Public/Img/elementos')
                extension = os.path.splitext(elemento.Foto.name)[1]
                nombrealeatorio = str(uuid.uuid4()) + extension
                imagen.save(nombrealeatorio, elemento.Foto)
                elemento.Foto = nombrealeatorio

                elemento.save()
                messages.success(request, 'Elemento Registrado Correctamente')
            except DatabaseError as e:
                messages.error(request, f'Ocurrio un error en el sistema {e}')
            return redirect('/Elementos/ListarElementos')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'Elementos/RegistrarElemento.html', {'ambientes': ambientes})
    else:
        return render(request, 'Elementos/RegistrarElemento.html', {'ambientes': ambientes})


def ListarElementos(request):
    try:
        listadoelementos = Elemento.objects.all().order_by('-id')
        listadoambientes= Ambiente.objects.all().order_by('NombreAmbiente')
        return render(request, 'Elementos/ListarElementos.html', {'listadoelementos': listadoelementos,'ambientes':listadoambientes})
    except DatabaseError as e:
        messages.error(request, f'Ocurrio un error en el sistema {e}')

###API PARA CONSULTAR ELEMENTO##

def APIConsultarElemento(request, idelemento):
    
    elemento = Elemento.objects.filter(id = idelemento)
    elementoJson = serialize('json', elemento)
    return HttpResponse(elementoJson, content_type='application/json')

###METODO PARA ACTUALIZAR ELEMENTO

def ActualizarElemento(request):
    try:
        ambiente = Ambiente.objects.all().order_by('NombreAmbiente')
        if request.method == 'POST': 
            if(request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observaciones') and request.POST.get('ambiente')):
                elemento = Elemento()
                elemento.id = request.POST.get('idelemento')
                elemento.Nombre = request.POST.get('nombre')
                elemento.Tipo = request.POST.get('tipo')
                elemento.Observaciones = request.POST.get('observaciones')
                elemento.ambiente = Ambiente.objects.get(id = request.POST.get('ambiente'))


                if request.FILES.get('foto'):
                    elemento.Foto = request.FILES.get('foto')
                    imagen = FileSystemStorage(location='AmbienteSena/Public/Img/elementos')
                    extension = os.path.splitext(elemento.Foto.name)[1]
                    nombrealeatorio = str(uuid.uuid4()) + extension
                    imagen.save(nombrealeatorio,elemento.Foto)
                    elemento.Foto = nombrealeatorio
                    imagen.delete(request.POST.get('nombre-foto'))
                else:
                    elemento.Foto = request.POST.get('nombre-foto')
                elemento.save()
                messages.success(request,'Elemento actualizado correctamente')
                return redirect('/Elementos/ListarElementos')
            else:
                messages.error(request,'ERROR FALTAN DATOS EN EL FORMULARIO')
                return redirect('/Elementos/ListarElementos')
    except DatabaseError as e:
        messages.error(request,f'OCURRIO UN ERROR EN EL SISTEMA {e}')
        return redirect('/Elementos/ListarElementos')
    

# METODO PARA ELIMINAR ELEMENTO

def EliminarElemento(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            try:
                elemento = Elemento.objects.get(id = request.POST.get('id'))
                ruta_imagen = settings.RUTA_IMAGENES_ELEMENTOS / str(elemento.Foto)
                if ruta_imagen.exists():
                    # print("La ruta de la imagen a eliminar es: ", ruta_imagen)
                    os.remove(ruta_imagen)
                    elemento.delete()
                    messages.success(request,'Elemento eliminado correctamente')
            except DatabaseError as e:
                messages.error(request,f'Ocurrio un error en el sistema { e }')

            return redirect('/Elementos/ListarElementos')

        else:
            messages.error(request,'El id del elemento no existe')
            return redirect('/Elementos/ListarElementos')



                    
