from django.contrib import admin
from bar.models import Coquetel
from bar.models import Funcionario
from bar.models import Cliente
from bar.models import Pacote
from bar.models import Evento

admin.site.register(Coquetel)
admin.site.register(Funcionario)
admin.site.register(Cliente)
admin.site.register(Pacote)
admin.site.register(Evento)