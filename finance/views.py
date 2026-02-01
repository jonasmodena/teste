from datetime import date
from decimal import Decimal
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
import csv

from .models import Transaction, Category


def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)

    tx_month = Transaction.objects.filter(
        date__gte=month_start,
        date__lte=today
    ).select_related("category")

    income_total = tx_month.filter(
        category__kind=Category.Kind.INCOME
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    expense_total = tx_month.filter(
        category__kind=Category.Kind.EXPENSE
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    balance = income_total - expense_total

    by_category = (
        tx_month.values("category__kind", "category__name")
        .annotate(total=Sum("amount"))
        .order_by("category__kind", "-total")
    )

    return render(request, "finance/dashboard.html", {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
        "by_category": by_category,
        "transactions": tx_month.order_by("-date")[:15],
        "month_start": month_start,
        "today": today,
    })


def export_csv(request):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="lancamentos.csv"'

    writer = csv.writer(response)
    writer.writerow(["Data", "Descrição", "Tipo", "Categoria", "Valor", "Método"])

    for t in Transaction.objects.select_related("category").order_by("-date"):
        writer.writerow([
            t.date,
            t.description,
            t.category.get_kind_display(),
            t.category.name,
            f"{t.amount:.2f}",
            t.get_method_display(),
        ])

    return response
