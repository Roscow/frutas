from django.contrib import admin

from .models import Sabor, Color, Region, EstadoFruta, Genero, TipoUsuario
from .models import Fruta, Usuario, ComparacionFrutas, UltimaPreferencia, PreferenciasFrutas
from .models import EstadisticaGenero, EstadisticaGlobal, EstadisticaRegion, EstadisticaRegionGenero
from .models import LogFrutas, LogUsuarios
# Register your models here.


admin.site.register(Color)
admin.site.register(Region)
admin.site.register(Fruta)
admin.site.register(EstadisticaGenero)
admin.site.register(EstadoFruta)
admin.site.register(Genero)
admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(Sabor)
admin.site.register(ComparacionFrutas)
admin.site.register(UltimaPreferencia)
admin.site.register(PreferenciasFrutas)
admin.site.register(LogFrutas)
admin.site.register(LogUsuarios)
admin.site.register(EstadisticaGlobal)
admin.site.register(EstadisticaRegion)
admin.site.register(EstadisticaRegionGenero)