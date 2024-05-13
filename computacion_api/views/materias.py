from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from computacion_api.serializers import *
from computacion_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

class MateriasAll(generics.CreateAPIView):
    #Esta linea se usa para pedir el token de autenticación de inicio de sesión
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        # materia = Materias.objects.filter(user__is_active = 1).order_by("NRC")
        materia = Materias.objects.filter().order_by("id")
        lista = MateriaSerializer(materia, many=True).data
        #Aquí convertimos los valores de nuevo a un array
        if not lista:
            return Response({},200)
        
        return Response(lista, 200)
    
class MateriasView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id = request.GET.get("id"))
        materia = MateriaSerializer(materia, many=False).data

        return Response(materia, 200)
    
    #Registrar nueva materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #materia = MateriaSerializer(data=request.data)
        materia = request.data
        #if materia.is_valid():
            #Grab materia data
        NRC = request.data['NRC']
        nombre_materia = request.data['nombre_materia']
        seccion = request.data['seccion']
        lun=request.data['lun']
        mar=request.data['mar']
        mie=request.data['mie']
        jue=request.data['jue']
        vie=request.data['vie']
        sab=request.data['sab']
        horario = request.data['horario']
        salon = request.data['salon']
        programa_educativo = request.data['programa_educativo']

        existing_NRC = Materias.objects.filter(NRC=NRC).first()

        if existing_NRC:
            return Response({"message":"materianame "+NRC+", is already taken"},400)

        materia = Materias.objects.create( NRC = NRC,
                            nombre_materia = nombre_materia,
                            seccion = seccion,
                            lun=lun,
                            mar=mar,
                            mie=mie,
                            jue=jue,
                            vie=vie,
                            sab=sab,
                            horario = horario,
                            salon = salon,
                            programa_educativo = programa_educativo
                        )

        materia.save()

        return Response({"materia_created_nrc": materia.NRC }, 201)

        return Response(materia.errors, status=status.HTTP_400_BAD_REQUEST)

class MateriasViewEdit(generics.CreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.data["id"])
        materia.NRC = request.data['NRC']
        materia.nombre_materia = request.data['nombre_materia']
        materia.seccion = request.data['seccion']
        materia.lun=request.data['lun']
        materia.mar=request.data['mar']
        materia.mie=request.data['mie']
        materia.jue=request.data['jue']
        materia.vie=request.data['vie']
        materia.sab=request.data['sab']
        materia.horario = request.data['horario']
        materia.salon = request.data['salon']
        materia.programa_educativo = request.data['programa_educativo']
        materia.save()
        materia = MateriaSerializer(materia, many=False).data

        return Response(materia,200)
    
    #Eliminar alumno.
    def delete(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            materia.delete()
            return Response({"details":"Materia eliminada"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
