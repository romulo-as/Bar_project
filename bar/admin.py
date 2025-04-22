from django.contrib import admin
from bar.models import Coquetel
from bar.models import Funcionario
from bar.models import Porcao
from bar.models import Pedido

admin.site.register(Coquetel)
admin.site.register(Funcionario)
admin.site.register(Porcao)
admin.site.register(Pedido)