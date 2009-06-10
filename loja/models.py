# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from datetime import datetime

# Create your models here.

GENDER_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)

class Cliente(models.Model):
	nome = models.CharField(max_length=100)
	cpf = models.IntegerField(null=True, blank=True)
	cidade = models.CharField(max_length=50, null=True, blank=True)
	estado = models.CharField(choices=STATE_CHOICES, max_length=2, null=True, blank=True, default="PR")
	cep = models.IntegerField(null=True, blank=True)
	sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
	pai = models.CharField(u'Nome do Pai',max_length=100, null=True, blank=True)
	mae = models.CharField(u'Nome da Mãe',max_length=100, null=True, blank=True)
	criado = models.DateTimeField(default=datetime.now)
	nascimento = models.DateField(null=True, blank=True)

	class Meta:
		verbose_name_plural = u'Clientes'
		db_table = 'cliente'
		ordering = ['nome']

	def __unicode__(self):
		return "%s, %s" % (self.nome, self.cpf)

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

class Item(models.Model):
	nome = models.CharField(max_length=50)

class Compra(models.Model):
	data = models.DateTimeField(default=datetime.now)
	total = models.FloatField()
	saldo = models.FloatField()
	item = models.ManyToManyField(Item, through='ItemCompra')

class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra)
    item = models.ForeignKey(Item)
    valor = models.FloatField()

