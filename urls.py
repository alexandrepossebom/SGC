from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'sgc.loja.views.index'),
    (r'^adicionar_cliente/$', 'sgc.loja.views.adicionar_cliente'),
    (r'^mostra_dados_cliente/(?P<codigo>\d+)/$', 'sgc.loja.views.mostra_dados_cliente'),
    (r'^compra/add/(?P<codigo>\d+)/$', 'sgc.loja.views.compra_add'),
    (r'^compra/end/(?P<codigo>\d+)/$', 'sgc.loja.views.compra_end'),
    (r'^atrasado/(?P<dias>\d+)/$', 'sgc.loja.views.atrasado'),
    (r'^detalhes/(?P<codigo>\d+)/$', 'sgc.loja.views.detalhes'),
    (r'^pagar/(?P<codigo>\d+)/$', 'sgc.loja.views.pagar'),
    (r'^pagar/end/(?P<codigo>\d+)/$', 'sgc.loja.views.pagar_end'),
    (r'^admin/(.*)', admin.site.root),
)
