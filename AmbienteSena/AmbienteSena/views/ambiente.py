from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage


def RegistrarAmbiente(request):
    if request.method == 'POST':
        ##Validacion de datos al frontend##
        if request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observacion'):
            ##Definicion de Variables##
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            observacion = request.POST.get('observacion')
            ##Conexion a base de datos##
            try:
                insertar = connection.cursor()
                insertar.execute('CALL sp_insertarambiente(%s, %s, %s)',[nombre, tipo, observacion])
                messages.success(request,'Ambiente de formacion registrado correctamente')
            except Exception as e:
                messages.error(request,'Ocurrio un error en el sisteme. Intentelo mas tarde')
            return redirect('/Ambientes/ListaAmbientes')
    else:
         return render(request,'Ambientes/RegistrarAmbiente.html')
    
###Consultar Ambientes de Formaciom###
def ListarAmbientes(request):
    try:
        ListarAmbientes = connection.cursor()
        ListarAmbientes.execute('CALL sp_listarambientes()')
    except Exception as e:
        messages.error(request,'Ocurrio un error en el sistema')
        return render(request,'Ambientes\ListaAmbientes.html' )
    return render(request,'Ambientes/ListaAmbientes.html', {'ambientes': ListarAmbientes})


def EliminarAmbiente(request):
    if request.method == 'POST':
        try:
            eliminar = connection.cursor()
            eliminar.execute('CALL sp_eliminarambiente(%s)',[request.POST.get('id')])
            messages.success(request,"Ambiente de formacion eliminado correctamente")
        except Exception as e: 
            messages.error(request,"Ocurrio un error en el sistema: {{e}}")
        return redirect('/Ambientes/ListaAmbientes')
    
#### ESTO ES PARA EDITAR UN AMBIENTE DE FORMACION EN LA BASE DE DATOS###
def ActualizarAmbiente(request, id_ambiente):
    if request.method == 'POST':
        try:
            actualizar = connection.cursor()
            actualizar.execute("CALL sp_actualizarambiente(%s,%s,%s,%s)",
                                           [id_ambiente,request.POST.get('nombre'),
                                            request.POST.get('tipo'),
                                            request.POST.get('observacion')])
            messages.success(request,"ambiente actualizado correctamente")
        except Exception as e:
            messages.error(request,"surgio un error en el sistema. Purbe mas tarde")
        return redirect('/Ambientes/ListaAmbientes')
    else:
            
        try:
            consulta = connection.cursor()
            consulta.execute('CALL sp_consultarambiente(%s)',[id_ambiente])
            return render(request,'Ambientes/ActualizarAmbiente.html',{'ambiente':consulta})
        except Exception as e:
            messages.error(request,'error en el sistemaaaaa')
            return redirect('/Ambientes/ListaAmbientes')
