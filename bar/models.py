from django.db import models

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
    class Meta:
        verbose_name_plural = "Coqueteis"
    def _str_(self):
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
    class Meta:
        verbose_name_plural = "Serviços"
    def _str_(self):
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
    Produtos = models.ForeignKey('Produto', on_delete=models.PROTECT)
    duracaoHora = models.IntegerField()
    Servicos = models.ForeignKey('Servico', on_delete=models.PROTECT)
    valorPorPessoa = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    class Meta:
        verbose_name_plural = "Pacotes"
    def _str_(self):
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
    class Meta:
        verbose_name_plural = "Funcionários"
    def _str_(self):
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
    class Meta:
        verbose_name_plural = "Clientes"
    def _str_(self):
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
    class Meta:
        verbose_name_plural = "Reservas"
    def _str_(self):
        return f"Reserva de {self.cliente.nome} em {self.data}"
    @property
    def total_estimado(self):
        return self.pacote.valorPorPessoa * self.convidados
    @property
    def dia_semana(self):
        return self.data.strftime('%A')

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    email = models.EmailField()
    class Meta:
        verbose_name_plural = "Fornecedores"
    def _str_(self):
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
    class Meta:
        verbose_name_plural = "Produtos"
    def _str_(self):
        return self.nome
    @property
    def preco_formatado(self):
        return f"R${self.preco:.2f}"
    @property
    def fornecedor_nome(self):
        return self.fornecedor.nome

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
    class Meta:
        verbose_name_plural = "Eventos"


