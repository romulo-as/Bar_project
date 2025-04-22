from django.db import models


class Coquetel(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField(max_length=200, null=True)
    recipiente = models.CharField(
        choices=(
            ('ld', 'Long Drink'), 
            ('otr', 'On The Rocks'), 
            ('tac', 'Taça'),
        ), 
        default=''
    )
    preco_custo = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    preco_venda = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    salario = models.DecimalField(decimal_places=2, max_digits=6, default=0.0)
    funcao = models.CharField(
        choices=(
            ('brt', 'bartender'), 
            ('coz', 'cozinheiro'),
            ('gar', 'garçom'),
            ('cai', 'caixa'),
            ('ger', 'gerente')
        ), default=''
    )
    cpf = models.CharField(max_length=11, null=True, default=None, unique=True)
    email = models.EmailField(blank= True, null=True, default=None, unique=True)

    def __str__(self):
        return self.nome
    
class Porcao(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField(max_length=300, null=True)
    adicional = models.CharField(
        choices=(
            ('', '---'),
            ('Cal', 'Calabresa'), 
            ('Mus', 'Mussarela'),
            ('Bac', 'Bacon'),
            ('Che', 'Cheddar'),
            ('Cat', 'Catupiry')
        ), default='', blank=True
    )
    preco_custo = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    preco_venda = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)

    def __str__(self):
        return self.nome
    
class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    pago = models.BooleanField()
    forma_pagamento = models.CharField(
        choices=(
            ('Cre', 'Crédito'), 
            ('Deb', 'Débito'),
            ('Pix', 'Pix'),
            ('Din', 'Dinheiro')
        )
    )
    datahora = models.DateTimeField(auto_now_add=True)
    coqueteis = models.ForeignKey('Coquetel', on_delete=models.PROTECT)
    porcoes = models.ForeignKey('Porcao', on_delete=models.PROTECT)
    atendente = models.ForeignKey('Funcionario', on_delete=models.DO_NOTHING)


