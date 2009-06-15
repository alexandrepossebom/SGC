# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from datetime import datetime
from django.forms import ModelForm

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

ESTADO_CIVIL_CHOICES = [ ['Solteiro(a)','Solteiro(a)' ],
                    ['Casado(a)','Casado(a)' ],
                    ['Viúvo(a)','Viúvo(a)' ],
                    ['Separado(a), ou Divorciado(a)','Separado(a), ou Divorciado(a)' ]]

class Empresa(models.Model):
	nome = models.CharField(max_length=70)
	def __unicode__(self):
		return "%s" % (unicode(self.nome))

class Cliente(models.Model):
	nome = models.CharField(max_length=100)
	cpf = models.IntegerField(null=True, blank=True)
	rg  = models.CharField(max_length=30,null=True, blank=True)
	nat_estado = models.CharField('Estado',choices=STATE_CHOICES, max_length=2, null=True, blank=True, default="PR")
	end_estado = models.CharField('Estado',choices=STATE_CHOICES, max_length=2, null=True, blank=True, default="PR")
	nat_cidade = models.CharField('Cidade',max_length=30, null=True, blank=True, default='São José dos Pinhais')
	end_cidade = models.CharField('Cidade',max_length=50, null=True, blank=True, default='São José dos Pinhais')
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
	emp_cargo =models.CharField('Cargo',max_length=50, null=True, blank=True)
	emp_renda = models.FloatField('Renda Mensal',max_length=50, null=True, blank=True)
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
	emp_renda = models.DecimalField('Renda Mensal', max_digits=5, decimal_places=2, null=True, blank=True)
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


class Parcela(models.Model):
	valor = models.FloatField()
	vencimento = models.DateField()
	paga = models.BooleanField(default=False)
	data_pagamento = models.DateTimeField(null=True, blank=True)
	def __unicode__(self):
		return "%s" % (self.valor)

class Vendedor(models.Model):
	nome = models.CharField(max_length=3)
	def __unicode__(self):
		return "%s" % (self.nome)


class Compra(models.Model):
	data = models.DateTimeField(default=datetime.now)
	total = models.FloatField()
	saldo = models.FloatField()
	forma = models.ForeignKey(FormaPagamento)
	vendedor = models.ForeignKey(Vendedor)
	item = models.PositiveSmallIntegerField(null=True, blank=True)
	def __unicode__(self):
		return "%s,%s" % (self.data,self.total)

