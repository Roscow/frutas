from typing import ContextManager
from django.core.exceptions import EmptyResultSet
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Color, ComparacionFrutas, EstadisticaGenero, EstadisticaGlobal, Genero, LogFrutas, Region, Usuario , Fruta, PreferenciasFrutas, Sabor, EstadoFruta, LogUsuarios, UltimaPreferencia
from django.contrib.auth.models import User
import math
import random
from django.urls import reverse
from .forms import create_fruta
from django.utils import timezone
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.



def index(request):
    #return render(request,'frutas/base.html')
    #return render(request,'frutas/frutas.html')
    return HttpResponseRedirect('/frutas/1/')


def agregar_fruta(request):
    if request.method == 'POST':
        nombre_get= request.POST.get('nombre')
        descripcion_get=request.POST.get('descripcion')
        imagen_get=request.POST.get('imagen')
        color_object =  Color.objects.get(id=request.POST.get('color'))   
        sabor_object = Sabor.objects.get(id=request.POST.get('sabor'))   
        estado_fruta_object= EstadoFruta.objects.get(nombre__icontains='enviado')
        Fruta.objects.create(nombre =nombre_get , color_principal =color_object , sabor= sabor_object, estado_fruta=estado_fruta_object , descripcion =descripcion_get ,imagen=imagen_get)
        form = create_fruta(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/frutas/1/')
    else:
        form = create_fruta()
        list_sabores = Sabor.objects.all()
        list_colores = Color.objects.all()
        context= {'list_sabores':list_sabores, 'list_colores':list_colores, 'form':form}
    return render(request,'frutas/agregar_fruta.html', context)


def ranking(request):
    return render(request,'frutas/ranking.html')


def faltantes(request):
    if request.method == 'POST':
        id_fruta_aux =request.POST.get('id_fruta')
        id_user_aux = request.POST.get('id_usuario')
        #revisar lo de abajo
        pref_object = PreferenciasFrutas.objects.get(id=id_fruta_aux, usuario=id_user_aux)
        max_ranking = PreferenciasFrutas.objects.filter(usuario=id_user_aux).exclude(ranking_valor__isnull=True).count()
        pref_object.ranking_valor = max_ranking+1
        pref_object.save()

        #ACTUALIZAR ULTIMA PREFERENCIA
        conn = pymysql.connect(host='127.0.0.1', user=os.getenv('db_user'), password=os.getenv('db_pass'), database=os.getenv('db_name'), charset='utf8')
        cur = conn.cursor()
        cur.callproc("actualizar_ultima_preferencia", (request.user.id,))
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/faltantes/')
    else:
        form = create_fruta()
        list_sabores = Sabor.objects.all()
        list_colores = Color.objects.all()
        context= {'list_sabores':list_sabores, 'list_colores':list_colores, 'form':form}

    



    return render(request,'frutas/faltantes.html')


def actualizar_foto(request):
    conn = pymysql.connect(host='127.0.0.1', user=os.getenv('db_user'), password=os.getenv('db_pass'), database=os.getenv('db_name'), charset='utf8')
    cur = conn.cursor()
    cur.callproc("actualizar_foto", (request.user.id,))
    conn.commit()
    conn.close()
    #return render(request,'frutas/perfil_usuario.html')    
    return perfil_usuario(request)


def versus(request):
    if request.method == 'POST':
        accion_aux =request.POST.get('accion')
        id_user_aux = request.POST.get('id_usuario')
        usuario_obj = Usuario.objects.get(id=id_user_aux)

        if accion_aux=='preferencia' :
            fruta1_obj= Fruta.objects.get(id=request.POST.get('fruta1'))
            fruta2_obj= Fruta.objects.get(id=request.POST.get('fruta2'))
            elecccion_obj = Fruta.objects.get(id=request.POST.get('eleccion'))
            ComparacionFrutas.objects.create(usuario=usuario_obj,fruta1=fruta1_obj, fruta2=fruta2_obj, eleccion=elecccion_obj, fecha_comparacion= timezone.now())

        if accion_aux=='sinprobar' :            
            fruta3_aux =request.POST.get('id_fruta')
            fruta3_obj = Fruta.objects.get(id=fruta3_aux)
            pref_bool = PreferenciasFrutas.objects.filter(usuario=usuario_obj, fruta= fruta3_aux).exists()

            if pref_bool==True:
                fruta3_obj = PreferenciasFrutas.objects.get(usuario=usuario_obj, fruta= fruta3_aux)
                fruta3_obj.ranking_valor = None
                fruta3_obj.save()
            else:
                PreferenciasFrutas.objects.create(usuario=usuario_obj, fruta= fruta3_obj, ranking_valor= None)

    user_id= request.user.id
    #ver si existen comparaciones por realizar 
    estado_object = EstadoFruta.objects.get(nombre__icontains='aprobado')
    list_frutas_validas= Fruta.objects.all().filter(estado_fruta=estado_object)
        #verificar en esta lista que no hayan valores que el usuario no haya probado
    for f in list_frutas_validas:
        pref_bool = PreferenciasFrutas.objects.filter(usuario=user_id, fruta=f.id).exists()
        if(pref_bool==True):
            pref_object = PreferenciasFrutas.objects.get(usuario=user_id, fruta=f.id)
            if(pref_object.ranking_valor == None ):
                list_frutas_validas=list_frutas_validas.exclude(id=f.id)
    total_frutas_validas=len(list_frutas_validas)
        
    comparacion_valida=False
    contador_novalidas=0
    while comparacion_valida==False:
        if(contador_novalidas==20):
            return render(request,'frutas/versus.html')

        num1=random.randint(0, (total_frutas_validas-1))
        num2=random.randint(0, (total_frutas_validas-1))

        if(num1 != num2):
            #obtengo valor desde la lista de objetos 
            fruta1_obj= list_frutas_validas[num1]
            fruta2_obj= list_frutas_validas[num2]
            comparacion_object = ComparacionFrutas.objects.filter(usuario=user_id, fruta1=fruta1_obj.id , fruta2=fruta2_obj.id ).exists()
            if(comparacion_object==True):
                comparacion_valida=False
            else:
                comparacion_object = ComparacionFrutas.objects.filter(usuario=user_id, fruta1=fruta2_obj.id , fruta2=fruta1_obj.id ).exists()     
                if(comparacion_object==True):
                    comparacion_valida=False
                else:
                    comparacion_valida=True
        else:
            comparacion_valida=False

        if(comparacion_valida==False):
            contador_novalidas= contador_novalidas+1

        if(comparacion_valida==True):
            ranking_f1= PreferenciasFrutas.objects.filter(fruta=fruta1_obj, usuario=user_id)[:1]
            ranking_f2= PreferenciasFrutas.objects.filter(fruta=fruta2_obj, usuario=user_id)[:1]

    context={'total_frutas_validas':total_frutas_validas,  'fruta1_obj':fruta1_obj, 'fruta2_obj':fruta2_obj, 'ranking_f1':ranking_f1, 'ranking_f2':ranking_f2 }
    return render(request,'frutas/versus.html',context)
        

def usuarios_inicio(request):
    try:
        usuarios = Usuario.objects.all().order_by('-fecha_creacion')[:10]
        context = {'usuarios':usuarios}
        return render(request,'frutas/usuarios.html',context)
    except Usuario.DoesNotExist:
        return render(request,'frutas/usuarios.html',)


def mostrar_usuarios(request, page):
    num_datos = 10
    dato_inicio = num_datos * (page-1)
    dato_final = num_datos * page
    total_datos = Usuario.objects.count()
    num_paginas = math.ceil(total_datos / num_datos)
    list_num_paginas = list()
    c_aux=1;
    next_pag = page +1
    prev_pag = page-1
    while c_aux <= num_paginas:
        list_num_paginas.append(c_aux)
        c_aux = c_aux +1
    try:
        lista_usuarios= Usuario.objects.all().order_by('-fecha_creacion')[dato_inicio:dato_final]
        context= {'lista_usuarios':lista_usuarios, 'list_num_paginas':list_num_paginas, 'next_pag':next_pag , 'prev_pag':prev_pag , 'page':page ,'num_paginas':num_paginas}
        return render(request,'frutas/mostrar_usuarios.html',context)
    except Usuario.DoesNotExist:
        return render(request,'frutas/mostrar_usuarios.html')


def usuario_detalle(request, id_usuario):
    try:
        usuario_detalle= Usuario.objects.get(id=id_usuario)  
        ranking_detalle = PreferenciasFrutas.objects.filter(usuario=id_usuario).order_by('ranking_valor').exclude(ranking_valor__isnull=True)
        faltantes_detalle = PreferenciasFrutas.objects.filter(usuario=id_usuario).exclude(ranking_valor__isnull=False)
        context= {'usuario_detalle':usuario_detalle , 'ranking_detalle':ranking_detalle , 'faltantes_detalle':faltantes_detalle}
        return render(request,'frutas/usuario_detalle.html',context)
    except Usuario.DoesNotExist:
        return render(request,'frutas/usuario_detalle.html')


def administracion_frutas(request):
    try:
        if request.method == 'POST':
            id_aux= request.POST.get('id_fruta')
            
            if(request.POST.get('accion')== 'eliminar'):
                fruta_aux= Fruta.objects.get(id=id_aux)
                list_log_fruta = LogFrutas.objects.filter(fruta=id_aux)
                for f in list_log_fruta:
                    f.delete()
                fruta_aux.delete()

            if(request.POST.get('accion')== 'publicar'):
                fruta_aux= Fruta.objects.get(id=id_aux)
                estado_fruta_aux = EstadoFruta.objects.get(nombre__icontains='aprobado')
                fruta_aux.estado_fruta=estado_fruta_aux
                fruta_aux.save()

            return HttpResponseRedirect('/administracion_frutas/')
        else:       
            lista_estados_noaprobados = EstadoFruta.objects.all().exclude(nombre__icontains='aprobado')     
            #frutas = Fruta.objects.filter(estado_fruta__in=[1,2,4]) 
            frutas = Fruta.objects.filter(estado_fruta__in=lista_estados_noaprobados) 
            context= {'frutas':frutas}
            return render(request,'frutas/administracion_frutas.html',context)
    except Fruta.DoesNotExist:
        return render(request,'frutas/administracion_frutas.html')


def perfil_usuario(request):
    if request.method == 'POST':        
        if(request.POST.get('accion')=='eliminar_usuario' ):
                usuario_obj2 = Usuario.objects.get(id = request.POST.get('id_usuario') )
                #borrar log usuario
                log_usuario_obj= LogUsuarios.objects.filter(usuario_emisor=usuario_obj2)
                for lu in log_usuario_obj:
                    lu.delete()  

                #borrar comparaciones 
                comparaciones_usuario_obj = ComparacionFrutas.objects.filter(usuario=usuario_obj2)
                for cu in comparaciones_usuario_obj:
                    cu.delete()

                #borrar ultima preferencia
                ultimapref_usuario_obj = UltimaPreferencia.objects.filter(usuario=usuario_obj2)
                for up in ultimapref_usuario_obj:
                    up.delete() 
                
                #borrar preferencias usuarios 
                pref_usuario_obj = PreferenciasFrutas.objects.filter(usuario=usuario_obj2)
                for pu in pref_usuario_obj:
                    pu.delete() 

                #borrar usuario
                usuario_obj2.delete()  
                #cerrar sesion 
                #eliminar cuenta
                #redirigir a inicio
                return HttpResponseRedirect('/frutas/1/')            
                #return HttpResponseRedirect(reverse{% url 'logout' %}"
        else:
            usuario_obj = Usuario.objects.get(id=request.user.id)
            if (request.POST.get('region') != ''):
                region_obj = Region.objects.get(id = request.POST.get('region'))
                usuario_obj.region = region_obj
            if (request.POST.get('genero') != ''):
                genero_obj = Genero.objects.get(id = request.POST.get('genero'))
                usuario_obj.genero = genero_obj
            usuario_obj.nombre= request.POST.get('nombre')
            usuario_obj.save()
        
    regiones_list = Region.objects.all().order_by('nombre')
    genero_list = Genero.objects.all()
    usuario_object = Usuario.objects.get(id=request.user.id)
    por_completar_list =list()
    if usuario_object.genero == None:
        por_completar_list.append('Indicar genero')
    context = {'regiones_list':regiones_list, 'genero_list':genero_list, 'por_completar_list':por_completar_list}
    return render(request,'frutas/perfil_usuario.html', context)    


def estadisticas_inicio(request):
    #obtener el ultimo valor de la tabla 
    estadistica_glob_obj = EstadisticaGlobal.objects.filter().order_by('-fecha_calculo')[:1]

    genero_masculino_obj = Genero.objects.get(titulo__icontains='masculino')
    estadistica_gen_masculino_obj = EstadisticaGenero.objects.filter(genero=genero_masculino_obj).order_by('-fecha_calculo')[:1]

    genero_femenino_obj = Genero.objects.get(titulo__icontains='femenino')
    estadistica_gen_femenino_obj = EstadisticaGenero.objects.filter(genero=genero_femenino_obj).order_by('-fecha_calculo')[:1]

    context= {'estadistica_glob_obj':estadistica_glob_obj, 'estadistica_gen_masculino_obj':estadistica_gen_masculino_obj, 'estadistica_gen_femenino_obj':estadistica_gen_femenino_obj}
    return render(request,'frutas/estadisticas.html', context)


def proyecto(request):
    return render(request,'frutas/proyecto.html')


def frutas_inicio(request,page):
    num_datos = 8
    dato_inicio = num_datos * (page-1)
    dato_final = num_datos * page
    total_datos = Fruta.objects.count()
    num_paginas = math.ceil(total_datos / num_datos)
    list_num_paginas = list()
    c_aux=1;
    estado_fruta_obj = EstadoFruta.objects.get(nombre__icontains='aprobado')
    next_pag = page +1
    prev_pag = page-1
    while c_aux <= num_paginas:
        list_num_paginas.append(c_aux)
        c_aux = c_aux +1
    try:
        frutas= Fruta.objects.filter(estado_fruta=estado_fruta_obj).order_by('nombre')[dato_inicio:dato_final]  
        context= {'frutas':frutas, 'list_num_paginas':list_num_paginas, 'next_pag':next_pag , 'prev_pag':prev_pag , 'page':page ,'num_paginas':num_paginas}
        return render(request,'frutas/frutas.html',context)
    except Usuario.DoesNotExist:
        return render(request,'frutas/frutas.html')

