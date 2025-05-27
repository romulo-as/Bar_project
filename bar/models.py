from django.db import models
from django.core.validators import MinValueValidator

class Coquetel(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField(max_length=200, null=True)
    recipiente = models.CharField(
        choices=(
            ('ld', 'Long Drink'), 
            ('otr', 'On The Rocks'), 
            ('tac', 'Taça'),
            ('ilh', 'Ilhabela')
        ), 
        default=''
    )
    preco_custo = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    preco_venda = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.SET_NULL, null=True, blank=True)  # Nova relação
    
    class Meta:
        verbose_name = "Coquetel"
        verbose_name_plural = "Coqueteis"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome'], name='idx_coquetel_nome'),
        ]
    
    def __str__(self):
        return self.nome
    
    @property
    def lucro_unitario(self):
        return self.preco_venda - self.preco_custo
    
    @property
    def margem_lucro(self):
        if self.preco_custo:
            return (self.preco_venda - self.preco_custo) / self.preco_custo
        return 0

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    valor_hora = models.DecimalField(decimal_places=2, max_digits=6, default=0.0)
    funcao = models.CharField(    
        choices=(
            ('brt', 'bartender'), 
            ('gar', 'garçom'),
            ('chef', 'cheff_pista')
        ), default=''
    )
    funcionarios = models.ManyToManyField('Funcionario', related_name='servicos')  # Nova relação
    
    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ['-valor_hora']
    
    def __str__(self):
        return self.nome
    
    @property
    def custo_diario_estimado(self):
        return self.valor_hora * 8
    
    @property
    def is_gerencial(self):
        return self.funcao == 'ger'

class Pacote(models.Model):
    nomePacote = models.CharField(max_length=100)
    coqueteis = models.ForeignKey('Coquetel', on_delete=models.PROTECT)
    produtos = models.ForeignKey('Produto', on_delete=models.PROTECT)
    duracaoHora = models.IntegerField()
    servicos = models.ForeignKey('Servico', on_delete=models.PROTECT)
    valorPorPessoa = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    eventos = models.ManyToManyField('Evento', related_name='pacotes')  # Nova relação
    
    class Meta:
        verbose_name = "Pacote"
        verbose_name_plural = "Pacotes"
        ordering = ['nomePacote']
        unique_together = ['nomePacote', 'coqueteis']
    
    def __str__(self):
        return self.nomePacote
    
    @property
    def duracao_total_minutos(self):
        return self.duracaoHora * 60
    
    @property
    def valor_total_estimado(self):
        return self.valorPorPessoa * 10  # estimativa para 10 pessoas

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    valorDiaria = models.DecimalField(decimal_places=2, max_digits=6, default=0.0)
    funcao = models.CharField(
        choices=(
            ('brt', 'bartender'), 
            ('brb', 'barback'),
            ('gar', 'garçom'),
            ('ger', 'gerente'),
            ('chef', 'cheff_pista')
        ), default=''
    )
    cpf = models.CharField(max_length=11, null=True, default=None, unique=True)
    email = models.EmailField(blank=True, null=True, default=None, unique=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Auto-relação
    
    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['-valorDiaria', 'nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def cargo_superior(self):
        return self.funcao in ['ger', 'chef']
    
    @property
    def email_profissional(self):
        if self.email:
            return self.email
        return f"{self.nome.replace(' ', '.').lower()}@bar.com"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    indicado_por = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Auto-relação
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']
        indexes = [
            models.Index(fields=['email'], name='idx_cliente_email'),
        ]
    
    def __str__(self):
        return self.nome
    
    @property
    def primeiro_nome(self):
        return self.nome.split(' ')[0]
    
    @property
    def contato_resumido(self):
        return f"{self.nome} ({self.telefone})"

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pacote = models.ForeignKey(Pacote, on_delete=models.SET_NULL, null=True)
    data = models.DateField()
    convidados = models.IntegerField()
    funcionario_responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)  # Nova relação
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-data']
        unique_together = ['cliente', 'data']
    
    def __str__(self):
        return f"Reserva de {self.cliente.nome} em {self.data}"
    
    @property
    def total_estimado(self):
        return self.pacote.valorPorPessoa * self.convidados if self.pacote else 0
    
    @property
    def dia_semana(self):
        return self.data.strftime('%A')

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)  # Novo campo
    endereco = models.TextField(blank=True)  # Novo campo
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def contato_comercial(self):
        return f"{self.nome} ({self.email})"
    
    @property
    def identificador(self):
        return f"{self.nome[:3].upper()}-{self.cnpj[-4:]}"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(decimal_places=2, max_digits=6)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    estoque = models.IntegerField(default=0)  # Novo campo
    estoque_minimo = models.IntegerField(default=5)  # Novo campo
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def preco_formatado(self):
        return f"R${self.preco:.2f}"
    
    @property
    def precisa_repor(self):
        return self.estoque < self.estoque_minimo

class Evento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    datahora = models.DateTimeField()
    pago = models.BooleanField()
    forma_pagamento = models.CharField(
        choices=(
            ('Cre', 'Crédito'), 
            ('Deb', 'Débito'),
            ('Pix', 'Pix'),
            ('Din', 'Dinheiro')
        )
    )
    local = models.CharField(max_length=100)  # Novo campo
    observacoes = models.TextField(blank=True)  # Novo campo
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-datahora']
    
    def __str__(self):
        return f"Evento {self.cliente.nome} em {self.datahora}"
    
    @property
    def status_pagamento(self):
        return "Pago" if self.pago else "Pendente"
    
    @property
    def horario_brasilia(self):
        return self.datahora.strftime('%d/%m/%Y %H:%M')