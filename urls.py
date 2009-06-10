from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sgc/', include('sgc.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'sgc.loja.views.index'),
    (r'^adicionar_cliente/$', 'sgc.loja.views.adicionar_cliente'),
    (r'^mostra_dados_cliente/(?P<codigo>\d+)/$', 'sgc.loja.views.mostra_dados_cliente'),
    (r'^admin/(.*)', admin.site.root),
)
