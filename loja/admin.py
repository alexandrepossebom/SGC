# -*- coding: utf-8 -*-
from django.contrib.localflavor.br import forms as forms_br
from django.contrib import admin
from sgc.loja.models import Cliente
from sgc.loja.models import TipoTelefone
from sgc.loja.models import Telefone
from sgc.loja.models import FormaPagamento
from sgc.loja.models import Empresa
from sgc.loja.models import Conjuge


class TelefoneAdmin(admin.TabularInline):
	model = Telefone
	extra = 2

class ConjugeAdmin(admin.TabularInline):
	model = Conjuge
	extra = 1

class ClienteAdmin(admin.ModelAdmin):
	cpf = forms_br.BRCPFField(label=u'CPF',required=False)
	inlines = [ TelefoneAdmin, ConjugeAdmin]
	list_display = ("nome","cpf","data_cadastro")
	ordering = ["-nome"]
	search_fields = ("nome","cpf")
	list_filter = ("nome",)
	radio_fields = {'sexo': admin.HORIZONTAL}  
	fieldsets = [
        ('Dados Pessoais'  , {'fields': ['nome','cpf','rg','estado_civil','sexo']}),
        ('Nascimento'      , {'fields': ['nascimento','nat_estado','nat_cidade']}),
        ('Paternidade', {'fields': [('pai','mae')]}),
        ('Endereço',    {'fields': [('end_rua','end_numero'),'end_cep','end_cidade','end_estado','end_bairro','tempoderesidencia']}),
        ('Trabalho',    {'classes': ['wide', 'extrapretty'],'fields': ['emp_firma',('emp_cargo','emp_renda','emp_tempo')]}),
#        (None, {'fields': ['data_cadastro']}),
	]
	class Meta:
		model = Cliente

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(FormaPagamento)
admin.site.register(TipoTelefone)
admin.site.register(Empresa)
