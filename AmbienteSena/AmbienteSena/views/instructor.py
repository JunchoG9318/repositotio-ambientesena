from django.contrib import messages
from django.shortcuts import redirect, render
from AmbienteSena.Models.instructor import Instructor


def RegistrarInstructor(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('area') and request.POST.get('celular') and request.POST.get('cedula'):
            try:
                instructor = Instructor()
                instructor.NombreCompleto = request.POST.get('nombre')
                instructor.Area = request.POST.get('area')
                instructor.Celular = request.POST.get('celular')
                instructor.Cedula = request.POST.get('cedula')
                instructor.save()
                messages.success(request,"Instructor Registrado correctamente")
            except Exception as e:
                messages.error(request, "surguio un error intentelo mañana")
            return redirect('/instructores/ListarInstructores')
    else:
        return render(request,'instructores/RegistrarInstructor.html')
    
###metodo para listar isntructores#
def ListarInstructores(request):
    try:
        listadoInstructores = Instructor.objects.all().order_by('-id')
        return render(request, 'instructores/ListarInstructores.html',{'listadoInstructores':listadoInstructores})
    except Exception as e:
        messages.error(request,"surguio un error intentelo mañana {{ e }}")
    return render(request, 'instructores/ListarInstructores.html',
                      {'listadoInstructores':listadoInstructores})

#metodo para eliminar instructiores##
def EliminarInstructor(request): 
    if request.method == 'POST':
        try:
            instructor = Instructor.objects.get(id = request.POST.get('id'))
            instructor.delete()
            messages.success(request,'Instructor eiliminado correctamente')

        except Exception as e:
            messages.error(request, f'surguio un error intentelo mañana { e }')
        return redirect('/instructores/ListarInstructores')
## metodo para actualizar instructores 
def ActualizarInstructor(request, id_instructor):
    if request.method == 'POST': 
        if request.POST.get('nombre') and request.POST.get('area') and request.POST.get('celular') and request.POST.get('cedula'):

            try:
                instructor = Instructor.objects.get(id = id_instructor)
                instructor.NombreCompleto = request.POST.get('nombre')
                instructor.Area = request.POST.get('area')
                instructor.Celular = request.POST.get('celular')
                instructor.Cedula = request.POST.get('cedula')
                instructor.save()
                messages.success(request,'Instructor actualizado actualmente')
            except Exception as e:
                messages.error(request,'surguio un error intentelo mañana {e}')
            return redirect('/instructores/ListarInstructores')
        else:
            messages.error(request,f' falta diligenciar un campo')
            return redirect('/instructores/ListarInstructores' )
    else:
        try:
            instructor = Instructor.objects.filter(id = id_instructor)
            return render(request,'instructores/ActualizarInstructor.html',{'instructor':instructor})
        except Exception as e:
            messages.error(request,f'ocurrio un error en el sistema. intentelo mañana {e}')
            return redirect('/instructores/ListarInstructores')
