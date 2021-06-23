
from frutas.views import perfil_usuario
from frutas.models import EstadoFruta, PreferenciasFrutas, Usuario ,Fruta
from django.contrib.auth.models import User



def datos_usuario(request):
    #se generan errores cuando uno de los campos no se haya y levanta excepcion
    try:
        usuario_conectado =  Usuario.objects.get(id=request.user.id)
        ranking = PreferenciasFrutas.objects.filter(usuario=request.user.id).order_by('ranking_valor').exclude(ranking_valor__isnull=True)
        faltantes = PreferenciasFrutas.objects.filter(usuario=request.user.id).exclude(ranking_valor__isnull=False)
        estados_fruta_list = EstadoFruta.objects.all().exclude(nombre__icontains='aprobado')
        #frutas_por_revisar = Fruta.objects.filter(estado_fruta__in=[1,2,4]).count()
        frutas_por_revisar = Fruta.objects.filter(estado_fruta__in=estados_fruta_list).count()
        perfil_revisar = list()
        if usuario_conectado.genero == None:
            perfil_revisar.append('Indicar genero')
        cuenta_alertas = len(perfil_revisar)
        return {'usuario_conectado':usuario_conectado, 'ranking':ranking ,'faltantes':faltantes, 'frutas_por_revisar':frutas_por_revisar, 'perfil_revisar':perfil_revisar, 'cuenta_alertas':cuenta_alertas}
    except:
        return{}
