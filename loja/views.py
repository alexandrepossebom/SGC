# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sgc.loja.models import Cliente
from sgc.loja.models import Compra
from sgc.loja.models import Vendedor
from sgc.loja.models import Parcela
from sgc.loja.models import FormaPagamento
from sgc.loja.forms import CompraForm
from sgc.loja.forms import ClienteModelForm

def index(request):
	clientes = Cliente.objects.all()
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

def compra_add(request,codigo):
	cliente =  get_object_or_404(Cliente, pk=codigo)	
	vendedores = Vendedor.objects.all()
	formas = FormaPagamento.objects.order_by('nome')
	compra = CompraForm()
	return render_to_response('compra_add.html', {'cliente': cliente, 'vendedores': vendedores, 'formas': formas, 'form': compra.as_table()})

def compra_end(request,codigo):
	compra = Compra()
	compra.data = request.POST['data']
	compra.total = request.POST['total']
	compra.item = request.POST['itens']
	compra.total = compra.total.replace(".","")
	compra.total = compra.total.replace(",",".")
	compra.saldo = compra.total
	compra.forma = get_object_or_404(FormaPagamento, pk=request.POST['forma'])
	compra.cliente = get_object_or_404(Cliente, pk=codigo)
	compra.vendedor = get_object_or_404(Vendedor, pk=request.POST['vendedor'])
	compra.save()
	parcela_valor = float(compra.total) * float(compra.forma.ajuste) / float(compra.forma.num_parcelas)
	venc = datetime.strptime(compra.data, "%Y-%m-%d")
	if compra.forma.entrada:
		venc = venc - relativedelta(months=+1)
	for i in range(0, compra.forma.num_parcelas):
		parc = Parcela()
		venc = venc + relativedelta(months=+1)
		parc.valor = parcela_valor
		parc.vencimento = venc
		parc.compra = compra
		parc.save()
	return render_to_response('compra_end.html', {'compra': compra})


def atrasado(request, dias):
	hoje = datetime.now()
	hoje = hoje + relativedelta(days=+int(dias))
	parcelas = Parcela.objects.filter(vencimento__lte=hoje)
	p = Parcela.objects.filter(vencimento__lte=hoje)
	for parcela in parcelas:
		valor = 0
		for pagamento in parcela.pagamento_set.all():
			valor = valor + pagamento.valor
			if valor > parcela.valor:
				parcelas = parcelas.exclude(pk=parcela.id)	
	return render_to_response('atrasado.html', {'parcelas': parcelas})

