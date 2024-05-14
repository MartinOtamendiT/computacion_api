from rest_framework import serializers
from rest_framework.authtoken.models import Token
from computacion_api.models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)    
    NRC = serializers.CharField(read_only=True)
    nombre_materia = serializers.CharField(required=True)
    seccion = serializers.CharField(required=True)
    programa_educativo = serializers.CharField(required=True)
    dias_materia = serializers.CharField(required=True)
    horario = serializers.CharField(required=True)
    salon = serializers.CharField(required=True)
    class Meta:
        model = Materias
        fields = ('id','NRC','nombre_materia','seccion', 'programa_educativo', 'dias_materia', 'horario', 'salon')