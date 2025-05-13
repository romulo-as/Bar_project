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
    

    def __str__(self):
        return self.nome

class Pacote(models.Model):
    nomePacote = models.CharField(max_length=100)
    coquetel = models.ManyToManyField(Coquetel)
    duracaoHora = models.IntegerField(max_length=1)
    garcom = models.BooleanField()
    valorPorPessoa = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)

    class Meta:
        verbose_name_plural = "Pacotes"

    def __str__(self):
        return self.nomePacote

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    valorDiaria = models.DecimalField(decimal_places=2, max_digits=6, default=0.0)
    funcao = models.CharField(
        choices=(
            ('brt', 'bartender'), 
            ('brb', 'barback'),
            ('gar', 'garçom'),
            ('ger', 'gerente')
        ), default=''
    )
    cpf = models.CharField(max_length=11, null=True, default=None, unique=True)
    email = models.EmailField(blank= True, null=True, default=None, unique=True)

    class Meta:
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, null=True, default=None, unique=True)
    email = models.EmailField(blank= True, null=True, default=None, unique=True)
    endereco = models.CharField(max_length=200)
    dataNasc = models.DateField()

    class Meta:
        verbose_name_plural = "Clientes"

    def calcular_idade(self):
        today = date.today()
        idade = today.year - self.dataNasc.year
        if today.month < self.dataNasc or (today.month == self.dataNasc and today.day < self.dataNasc.day):
            idade -= 1
        return idade

    def __str__(self):
        return self.nome
    
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
    coqueteis = models.ForeignKey('Coquetel', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Eventos"
