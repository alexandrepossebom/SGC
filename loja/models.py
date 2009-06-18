# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from datetime import datetime
from django.forms import ModelForm
import locale

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

ESTADO_CIVIL_CHOICES = [ ['Solteiro(a)','Solteiro(a)' ],
                    ['Casado(a)','Casado(a)' ],
                    ['Viúvo(a)','Viúvo(a)' ],
                    ['Separado(a), ou Divorciado(a)','Separado(a), ou Divorciado(a)' ]]

def moeda_brasileira(numero):
	try:
		contador = 0
		preco_str = ''
		num = numero.__str__()
		if '.' in num:
			preco, centavos = num.split('.')
		else:
			preco = num
			centavos = '00'
		tamanho = len(preco)
		while tamanho > 0:
			preco_str = preco_str + preco[tamanho-1]
			contador += 1
			if contador == 3 and tamanho > 1:
				preco_str = preco_str + '.'
				contador = 0
			tamanho -= 1
 		tamanho = len(preco_str)
		str_preco = ''
		while tamanho > 0:
			str_preco = str_preco + preco_str[tamanho-1]
			tamanho -= 1
			return "R$ %s,%s" % (str_preco, centavos)
	except:
		return 'Erro. Nao foi possivel formatar.'


class Empresa(models.Model):
	nome = models.CharField(max_length=70)
	def __unicode__(self):
		return "%s" % (unicode(self.nome))


class Cidade(models.Model):
	nome = models.CharField(max_length=100)
	def __unicode__(self):
		return "%s" % (unicode(self.nome))

def get_sjp():
	if Cidade.objects.get(id=1) is not None:
		return Cidade.objects.get(id=1)
	else:
		return None

class Cliente(models.Model):
	nome = models.CharField(max_length=100)
	cpf = models.IntegerField(null=True, blank=True)
	rg  = models.CharField(max_length=30,null=True, blank=True)
	nat_estado = models.CharField('Estado',choices=STATE_CHOICES, max_length=2, null=True, blank=True, default="PR")
	end_estado = models.CharField('Estado',choices=STATE_CHOICES, max_length=2, null=True, blank=True, default="PR")
	end_cidade = models.ForeignKey(Cidade,verbose_name="Cidade",null=True, blank=True,related_name='end_cidade')#, default=get_sjp)
	nat_cidade = models.ForeignKey(Cidade,verbose_name="Cidade",null=True, blank=True,related_name='nat_cidade')#, default=get_sjp)
	end_rua = models.CharField('Rua',max_length=50, null=True, blank=True)
	end_numero = models.PositiveSmallIntegerField('Número',max_length=5, null=True, blank=True)
	end_cep = models.IntegerField('Cep',null=True, blank=True)
	sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
	estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
	pai = models.CharField(u'Nome do Pai',max_length=100, null=True, blank=True)
	mae = models.CharField(u'Nome da Mãe',max_length=100, null=True, blank=True)
	data_cadastro = models.DateTimeField('Data do Cadastro',default=datetime.now)
	nascimento = models.DateField(u'Data',null=True, blank=True)
	end_bairro = models.CharField('Bairro',max_length=50, null=True, blank=True)
	tempoderesidencia = models.DateField(u'Data',null=True, blank=True)
	emp_firma = models.ForeignKey(Empresa,verbose_name="Empresa",null=True, blank=True)
	emp_cargo = models.CharField('Cargo',max_length=50, null=True, blank=True)
	emp_renda = models.FloatField('Renda Mensal', null=True, blank=True)
	emp_tempo = models.DateField('Data Admissão',max_length=50, null=True, blank=True)

	class Meta:
		verbose_name_plural = u'Clientes'
		db_table = 'cliente'
		ordering = ['nome']

	def __unicode__(self):
		return "%s" % (unicode(self.nome))

class Conjuge(models.Model):	
	conj_nome = models.CharField('Nome',max_length=50, null=True, blank=True)
	emp_firma = models.ForeignKey(Empresa,verbose_name="Empresa",null=True, blank=True)
	emp_cargo = models.CharField('Cargo',max_length=50, null=True, blank=True)
	emp_tempo = models.DateField('Data Admissão',max_length=50, null=True, blank=True)
	emp_renda = models.FloatField('Renda Mensal',null=True, blank=True)
	cliente = models.OneToOneField(Cliente)
	class Meta:
 		verbose_name_plural = u'Conjuge'

	def __unicode__(self):
		return "%s" % (self.nome)

class TipoTelefone(models.Model):
	nome = models.CharField(max_length=15)
	def __unicode__(self):
		return "%s" % (self.nome)

class Telefone(models.Model):
	numero = models.IntegerField()
	tipo = models.ForeignKey(TipoTelefone)
	client = models.ForeignKey(Cliente)
	class Meta:
		ordering = ['numero']
	def __unicode__(self):
		return "%s (%s)" % (self.numero, self.tipo)

class FormaPagamento(models.Model):
	nome = models.CharField(max_length=15)
	entrada = models.BooleanField(default=False)
	ajuste = models.FloatField()
	num_parcelas = models.PositiveSmallIntegerField('Parcelas',default=1)
	def __unicode__(self):
		return "%s" % (self.nome)


class Vendedor(models.Model):
	nome = models.CharField(max_length=30)
	def __unicode__(self):
		return "%s" % (self.nome)
	class Meta:
		verbose_name_plural = u'Vendedores'

class Compra(models.Model):
	data = models.DateTimeField(default=datetime.now)
	total = models.FloatField()
	saldo = models.FloatField()
	forma = models.ForeignKey(FormaPagamento)
	vendedor = models.ForeignKey(Vendedor)
	item = models.PositiveSmallIntegerField(null=True, blank=True)
	cliente = models.ForeignKey(Cliente)
	def __unicode__(self):
		return "%s,%s" % (self.data,self.total)

class Parcela(models.Model):
	valor = models.FloatField()
	vencimento = models.DateField()
	compra = models.ForeignKey(Compra)
	ispaga = models.BooleanField(default=False) 
	def __unicode__(self):
		return "%s" % (self.valor)
	def getPrecoFormatado(self):
		return moeda_brasileira("%.2f" % self.valor)

class Pagamento(models.Model):
	valor = models.FloatField()
	data_pagamento = models.DateTimeField(null=True, blank=True)
	parcela = models.ForeignKey(Parcela)
	def __unicode__(self):
		return "%s" % (self.valor)

class PreVenda(models.Model):
	data = models.DateTimeField(default=datetime.now)
	previsao = models.DateTimeField(default=datetime.now)
	total = models.FloatField()
	vendedor = models.ForeignKey(Vendedor)
	item = models.PositiveSmallIntegerField(null=True, blank=True)
	cliente = models.ForeignKey(Cliente)
	def __unicode__(self):
		return "%s,%s" % (self.data,self.total)

