from django.db import models
from django.utils import timezone


class Category(models.Model):
    class Kind(models.TextChoices):
        INCOME = "INCOME", "Receita"
        EXPENSE = "EXPENSE", "Despesa"

    name = models.CharField(max_length=80, unique=True)
    kind = models.CharField(max_length=10, choices=Kind.choices)

    def __str__(self):
        return f"{self.get_kind_display()}: {self.name}"


class Transaction(models.Model):
    class Method(models.TextChoices):
        CASH = "CASH", "Dinheiro"
        PIX = "PIX", "PIX"
        DEBIT = "DEBIT", "Cartão débito"
        CREDIT = "CREDIT", "Cartão crédito"
        IFOOD = "IFOOD", "iFood"
        OTHER = "OTHER", "Outro"

    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=140)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=10, choices=Method.choices, default=Method.PIX)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.description} - R$ {self.amount}"
