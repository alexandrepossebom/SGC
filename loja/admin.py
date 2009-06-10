from sgc.loja.models import Cliente
from sgc.loja.models import TipoTelefone
from sgc.loja.models import Telefone
from django.contrib import admin

class TipoTelefoneAdmin(admin.ModelAdmin):
	pass


class TelefoneAdmin(admin.TabularInline):
	model = Telefone

class ClienteAdmin(admin.ModelAdmin):
	inlines = [ TelefoneAdmin, ]
	list_display = ("nome","cpf","criado")
	ordering = ["-nome"]
	search_fields = ("nome","cpf")
	list_filter = ("nome",)



admin.site.register(Cliente, ClienteAdmin)
#admin.site.register(Telefone, TelefoneAdmin)
admin.site.register(TipoTelefone, TipoTelefoneAdmin)
