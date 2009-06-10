# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from sgc.loja.models import Cliente

def index(request):
	clientes= Cliente.objects.all()
	return render_to_response('index.html',{'clientes':clientes,})

def adicionar_cliente(request):
    if request.POST:
        f = ClienteModelForm(request.POST)
        if f.is_valid():
            c = f.save()
            return HttpResponseRedirect(reverse('sgc.loja.views.index'))
        else:
            return HttpResponse(f.errors)
    else:
        f = ClienteModelForm()
        return render_to_response('adicionar_cliente.html', {'form':f.as_table(),})

def mostra_dados_cliente(request, codigo):
    cliente = get_object_or_404(Cliente, pk=codigo)
    codigo = cliente.id
    f = ClienteModelForm(instance=cliente)
    return render_to_response('cliente_dados.html', {'form':f.as_table(), 'codigo':codigo})

class ClienteModelForm(ModelForm):
    class Meta:
        model = Cliente

