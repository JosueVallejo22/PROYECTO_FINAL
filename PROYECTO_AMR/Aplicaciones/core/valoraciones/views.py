from django.shortcuts import render
from django.views.generic import *
# Create your views here.

class ValoracionesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'modulo_valoraciones.html')

class FormularioValoracionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'form_valoraciones.html')
