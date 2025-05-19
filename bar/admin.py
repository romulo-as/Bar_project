from django.contrib import admin
from bar.models import Coquetel
from bar.models import Servico
from bar.models import Pacote
from bar.models import Funcionario
from bar.models import Cliente
from bar.models import Reserva
from bar.models import Fornecedor
from bar.models import Produto

from bar.models import Evento


admin.site.register(Coquetel)
admin.site.register(Servico)
admin.site.register(Pacote)
admin.site.register(Funcionario)
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Evento)
