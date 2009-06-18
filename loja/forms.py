from django import forms
from sgc.loja.models import Compra
from sgc.loja.models import Cliente
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.contrib.admin import widgets

class CompraForm(forms.ModelForm):
	class Meta:
		model = Compra
#	def __init__(self, *args, **kwargs):
#		super(CompraForm, self).__init__(*args, **kwargs)
#		self.fields['mydate'].widget = widgets.AdminDateWidget()
#		self.fields['mytime'].widget = widgets.AdminTimeWidget()
#		self.fields['data'].widget = widgets.AdminSplitDateTime()


class ClienteModelForm(forms.ModelForm):
	data_cadastro = forms.DateTimeField(widget=AdminDateWidget())
	class Meta:
		model = Cliente
