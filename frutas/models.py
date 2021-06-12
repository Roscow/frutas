# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   (listo )* Rearrange models' order
#   (listo )* Make sure each model has one field with primary_key=True
#   (??)* Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   ()* Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Color(models.Model):
    id = models.BigAutoField(primary_key=True)
    color = models.CharField(unique=True, max_length=100)
    
    def __str__(self):
        return self.color

    class Meta:
        managed = False
        db_table = 'color'

class EstadoFruta(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'estado_fruta'


class Genero(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo

    class Meta:
        managed = False
        db_table = 'genero'



class Region(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(unique=True, max_length=5)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'region'


class Sabor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'sabor'


class TipoUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.titulo

    class Meta:
        managed = False
        db_table = 'tipo_usuario'


class Fruta(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    color_principal = models.ForeignKey(Color, models.DO_NOTHING, db_column='color_principal')
    sabor = models.ForeignKey('Sabor', models.DO_NOTHING, db_column='sabor')
    estado_fruta = models.ForeignKey(EstadoFruta, models.DO_NOTHING, db_column='estado_fruta')
    descripcion = models.CharField(max_length=500)
    imagen = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'fruta'



class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    correo = models.CharField(unique=True, max_length=100)
    passwrd = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    genero = models.ForeignKey(Genero, models.DO_NOTHING, db_column='genero', blank=True, null=True)
    fecha_creacion = models.DateTimeField()
    region = models.ForeignKey(Region, models.DO_NOTHING, db_column='region')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    imagen_avatar = models.CharField(max_length=250, blank=True, null=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='tipo_usuario')

    def __str__(self):
        return self.correo

    class Meta:
        managed = False
        db_table = 'usuario'



class ComparacionFrutas(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario', blank=True, null=True)
    fruta1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='fruta1', related_name='f1')
    fruta2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='fruta2', related_name='f2')
    eleccion = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='eleccion', blank=True, null=True, related_name='eleccion')
    fecha_comparacion = models.DateTimeField()

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'comparacion_frutas'
        unique_together = (('usuario', 'fruta1', 'fruta2'),)


class UltimaPreferencia(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario', blank=True, null=True)
    fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='fruta', blank=True, null=True)

    def __str__(self):
        return self.id
        
    class Meta:
        managed = False
        db_table = 'ultima_preferencia'
        unique_together = (('usuario', 'fruta'),)



class PreferenciasFrutas(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')
    fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='fruta')
    ranking_valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preferencias_frutas'
        unique_together = (('fruta', 'usuario'),)



class EstadisticaGenero(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_calculo = models.DateTimeField()
    porcentaje_ranking3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ranking3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking3', blank=True, null=True, related_name='ranking3GE')
    ranking2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking2', blank=True, null=True, related_name='ranking2GE')
    ranking1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking1', blank=True, null=True, related_name='ranking1GE')
    porcentaje_ranking_neg3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ranking_neg3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg3', blank=True, null=True, related_name='ranking_neg3GE')
    ranking_neg2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg2', blank=True, null=True, related_name='ranking_neg2GE')
    ranking_neg1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg1', blank=True, null=True, related_name='ranking_neg1GE')
    porcentaje_no_probado3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    no_probado3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado3', blank=True, null=True, related_name='no_probado3GE')
    no_probado2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado2', blank=True, null=True, related_name='no_probado2GE')
    no_probado1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado1', blank=True, null=True, related_name='no_probado1GE')
    genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='genero')

    class Meta:
        managed = False
        db_table = 'estadistica_genero'


class EstadisticaGlobal(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_calculo = models.DateTimeField()
    total_frutas = models.IntegerField()
    porcentaje_ranking3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking1 = models.DecimalField(max_digits=5, decimal_places=2)
    ranking3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking3', blank=True, null=True, related_name='ranking3GL')
    ranking2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking2', blank=True, null=True, related_name='ranking2GL')
    ranking1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking1', related_name='ranking1GL')
    porcentaje_ranking_neg3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ranking_neg3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg3', blank=True, null=True, related_name='ranking_neg3GL')
    ranking_neg2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg2', blank=True, null=True, related_name='ranking_neg2GL')
    ranking_neg1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg1', related_name='ranking_neg1GL')
    porcentaje_no_probado3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    no_probado3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado3', blank=True, null=True, related_name='no_probado3GL')
    no_probado2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado2', blank=True, null=True, related_name='no_probado2GL')
    no_probado1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado1', related_name='no_probado1GL')

    class Meta:
        managed = False
        db_table = 'estadistica_global'


class EstadisticaRegion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_calculo = models.DateTimeField()
    porcentaje_ranking3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ranking3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking3', blank=True, null=True, related_name='ranking3R')
    ranking2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking2', blank=True, null=True, related_name='ranking2R')
    ranking1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking1', blank=True, null=True, related_name='ranking1R')
    porcentaje_ranking_neg3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ranking_neg3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg3', blank=True, null=True, related_name='ranking_neg3R')
    ranking_neg2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg2', blank=True, null=True, related_name='ranking_neg2R')
    ranking_neg1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg1', blank=True, null=True, related_name='ranking_neg1R')
    porcentaje_no_probado3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    no_probado3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado3', blank=True, null=True, related_name='no_probado3R')
    no_probado2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado2', blank=True, null=True, related_name='no_probado2R')
    no_probado1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado1', blank=True, null=True, related_name='no_probado1R')
    region = models.ForeignKey('Region', models.DO_NOTHING, db_column='region')

    class Meta:
        managed = False
        db_table = 'estadistica_region'


class EstadisticaRegionGenero(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_calculo = models.DateTimeField()
    total_frutas = models.IntegerField()
    porcentaje_ranking3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    porcentaje_ranking2 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    porcentaje_ranking1 = models.DecimalField(max_digits=4, decimal_places=2)
    ranking3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking3', blank=True, null=True, related_name='ranking3RG')
    ranking2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking2', blank=True, null=True, related_name='ranking2RG')
    ranking1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking1', related_name='ranking1RG')
    porcentaje_ranking_neg3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg2 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    porcentaje_ranking_neg1 = models.DecimalField(max_digits=4, decimal_places=2)
    ranking_neg3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg3', blank=True, null=True, related_name='ranking_neg3RG')
    ranking_neg2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg2', blank=True, null=True, related_name='ranking_neg2RG')
    ranking_neg1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='ranking_neg1', related_name='ranking_neg1RG')
    porcentaje_no_probado3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado2 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    porcentaje_no_probado1 = models.DecimalField(max_digits=4, decimal_places=2)
    no_probado3 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado3', blank=True, null=True, related_name='no_probado3RG')
    no_probado2 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado2', blank=True, null=True, related_name='no_probado2RG')
    no_probado1 = models.ForeignKey('Fruta', models.DO_NOTHING, db_column='no_probado1', related_name='no_probado1RG')
    region = models.ForeignKey('Region', models.DO_NOTHING, db_column='region')
    genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='genero')

    class Meta:
        managed = False
        db_table = 'estadistica_region_genero'





class LogFrutas(models.Model):
    id = models.BigAutoField(primary_key=True)
    fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='fruta')
    estado_fruta = models.ForeignKey(EstadoFruta, models.DO_NOTHING, db_column='estado_fruta')
    usuario_emisor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_emisor', blank=True, null=True, related_name='usuario_emisorLF')
    tipo_usuario_emisor = models.ForeignKey('TipoUsuario', models.DO_NOTHING, db_column='tipo_usuario_emisor', blank=True, null=True, related_name='tipo_usuario_emisorLF')
    usuario_receptor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_receptor', blank=True, null=True, related_name='usuario_receptorLF')
    tipo_usuario_receptor = models.ForeignKey('TipoUsuario', models.DO_NOTHING, db_column='tipo_usuario_receptor', blank=True, null=True, related_name='tipo_usuario_receptorLF')
    fecha = models.DateTimeField()
    accion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_frutas'


class LogUsuarios(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario_emisor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_emisor', related_name='usuario_emisorLU')
    tipo_usuario_emisor = models.ForeignKey('TipoUsuario', models.DO_NOTHING, db_column='tipo_usuario_emisor', related_name='tipo_usuario_emisorLU')
    usuario_receptor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_receptor', blank=True, null=True, related_name='usuario_receptorLU')
    tipo_usuario_receptor = models.ForeignKey('TipoUsuario', models.DO_NOTHING, db_column='tipo_usuario_receptor', blank=True, null=True, related_name='tipo_usuario_receptorLU')
    fecha = models.DateTimeField()
    accion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_usuarios'


