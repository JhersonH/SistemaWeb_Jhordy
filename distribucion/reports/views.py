from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO

# Modelos
from transport.models import Trip, Incident, Expense
from inventory_receiving.models import ProductReception
from inventory_movements.models import InventoryMovement
from inventory_adjustments.models import InventoryAdjustment
from inventory_stock.models import ProductStock
from inventory_alerts.models import StockAlert
from inventory_kardex.models import KardexEntry
from suppliers.models import Supplier


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def paginate_queryset(request, queryset, per_page=20):
    """Aplica paginación a un queryset"""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def export_xlsx(queryset, headers, rows, filename, sheet_name="Reporte"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.append(headers)
    for row in rows(queryset):
        ws.append(row)
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response


def export_pdf(queryset, title, row_func, filename, headers=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))

    # Encabezados y filas
    data = []
    if headers:
        data.append(headers)
    for obj in queryset:
        data.append(row_func(obj))  # row_func debe retornar lista, no string

    # Tabla
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    # Crear PDF
    doc.build(elements)
    buffer.seek(0)

    # Respuesta
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


# ============================================================
# TRANSPORTE
# ============================================================

def trips_report(request):
    trips = paginate_queryset(request, Trip.objects.all().order_by("-date"), per_page=5)
    return render(request, "reports/transport/trips_report.html", {"trips": trips})

def trips_report_xlsx(request):
    return export_xlsx(
        Trip.objects.all(),
        ["ID", "Ruta", "Conductor", "Fecha", "Recepción"],
        lambda qs: [[t.id, str(t.route), str(t.driver), t.date.strftime("%Y-%m-%d"), "Sí" if t.is_reception else "No"] for t in qs],
        "reporte_viajes.xlsx",
        "Viajes"
    )

def trips_report_pdf(request):
    return export_pdf(
        Trip.objects.all(),
        "Reporte de Viajes",
        lambda t: [t.id, str(t.route), str(t.driver), t.date.strftime("%Y-%m-%d"), "Sí" if t.is_reception else "No"],
        "reporte_viajes.pdf",
        headers=["ID", "Ruta", "Conductor", "Fecha", "Recepción"]
    )

def incidents_report(request):
    incidents = paginate_queryset(request, Incident.objects.all().order_by("-occurred_at"), per_page=5)
    return render(request, "reports/transport/incidents_report.html", {"incidents": incidents})

def incidents_report_xlsx(request):
    return export_xlsx(
        Incident.objects.all(),
        ["ID", "Viaje", "Tipo", "Severidad", "Fecha"],
        lambda qs: [[i.id, str(i.trip), i.type, i.severity, i.occurred_at.strftime("%Y-%m-%d")] for i in qs],
        "reporte_incidentes.xlsx",
        "Incidentes"
    )

def incidents_report_pdf(request):
    return export_pdf(
        Incident.objects.all(),
        "Reporte de Incidentes",
        lambda i: [i.id, str(i.trip), i.type, i.severity, i.occurred_at.strftime("%Y-%m-%d %H:%M")],
        "reporte_incidentes.pdf",
        headers=["ID", "Viaje", "Tipo", "Severidad", "Fecha"]
    )


def expenses_report(request):
    expenses = paginate_queryset(request, Expense.objects.all().order_by("-created_at"), per_page=5)
    return render(request, "reports/transport/expenses_report.html", {"expenses": expenses})

def expenses_report_xlsx(request):
    return export_xlsx(
        Expense.objects.all(),
        ["ID", "Viaje", "Tipo", "Monto", "Fecha"],
        lambda qs: [[e.id, str(e.trip), e.type, float(e.amount), e.created_at.strftime("%Y-%m-%d")] for e in qs],
        "reporte_gastos.xlsx",
        "Gastos"
    )

def expenses_report_pdf(request):
    return export_pdf(
        Expense.objects.all(),
        "Reporte de Gastos",
        lambda e: [e.id, str(e.trip), e.type, float(e.amount), e.created_at.strftime("%Y-%m-%d")],
        "reporte_gastos.pdf",
        headers=["ID", "Viaje", "Tipo", "Monto", "Fecha"]
    )


# ============================================================
# INVENTARIO
# ============================================================

def receptions_report(request):
    receptions = paginate_queryset(request, ProductReception.objects.all().order_by("-reception_date"), per_page=5)
    return render(request, "reports/inventory/receptions_report.html", {"receptions": receptions})

def receptions_report_xlsx(request):
    return export_xlsx(
        ProductReception.objects.all(),
        ["ID", "Producto", "Cantidad", "Proveedor", "Ubicación", "Fecha"],
        lambda qs: [[r.id, str(r.product), r.quantity_received, str(r.supplier), str(r.location), r.reception_date.strftime("%Y-%m-%d")] for r in qs],
        "reporte_recepciones.xlsx",
        "Recepciones"
    )

def receptions_report_pdf(request):
    return export_pdf(
        ProductReception.objects.all(),
        "Reporte de Recepciones",
        lambda r: [r.id, str(r.product), r.quantity_received, str(r.supplier), str(r.location), r.reception_date.strftime("%Y-%m-%d")],
        "reporte_recepciones.pdf",
        headers=["ID", "Producto", "Cantidad", "Proveedor", "Ubicación", "Fecha"]
    )

def movements_report(request):
    movements = paginate_queryset(request, InventoryMovement.objects.all().order_by("-date"), per_page=5)
    return render(request, "reports/inventory/movements_report.html", {"movements": movements})

def movements_report_xlsx(request):
    return export_xlsx(
        InventoryMovement.objects.all(),
        ["ID", "Producto", "Cantidad", "Tipo", "Ubicación", "Fecha"],
        lambda qs: [[m.id, str(m.product), m.quantity, m.movement_type, str(m.location), m.date.strftime("%Y-%m-%d")] for m in qs],
        "reporte_movimientos.xlsx",
        "Movimientos"
    )

def movements_report_pdf(request):
    return export_pdf(
        InventoryMovement.objects.all(),
        "Reporte de Movimientos",
        lambda m: [m.id, str(m.product), m.quantity, m.movement_type, str(m.location), m.date.strftime("%Y-%m-%d")],
        "reporte_movimientos.pdf",
        headers=["ID", "Producto", "Cantidad", "Tipo", "Ubicación", "Fecha"]
    )

def adjustments_report(request):
    adjustments = paginate_queryset(request, InventoryAdjustment.objects.all().order_by("-created_at"), per_page=5)
    return render(request, "reports/inventory/adjustments_report.html", {"adjustments": adjustments})

def adjustments_report_xlsx(request):
    return export_xlsx(
        InventoryAdjustment.objects.all(),
        ["ID", "Producto", "Cantidad", "Tipo", "Motivo", "Fecha"],
        lambda qs: [[a.id, str(a.product), a.quantity, a.adjustment_type, a.reason, a.created_at.strftime("%Y-%m-%d")] for a in qs],
        "reporte_ajustes.xlsx",
        "Ajustes"
    )

def adjustments_report_pdf(request):
    return export_pdf(
        InventoryAdjustment.objects.all(),
        "Reporte de Ajustes",
        lambda a: [a.id, str(a.product), a.quantity, a.adjustment_type, a.reason, a.created_at.strftime("%Y-%m-%d")],
        "reporte_ajustes.pdf",
        headers=["ID", "Producto", "Cantidad", "Tipo", "Motivo", "Fecha"]
    )

def stock_report(request):
    stocks = paginate_queryset(request, ProductStock.objects.all(), per_page=5)
    return render(request, "reports/inventory/stock_report.html", {"stocks": stocks})

def stock_report_xlsx(request):
    return export_xlsx(
        ProductStock.objects.all(),
        ["ID", "Producto", "Ubicación", "Cantidad"],
        lambda qs: [[s.id, str(s.product), str(s.location), s.quantity] for s in qs],
        "reporte_stock.xlsx",
        "Stock"
    )

def stock_report_pdf(request):
    return export_pdf(
        ProductStock.objects.all(),
        "Reporte de Stock",
        lambda s: [s.id, str(s.product), str(s.location), s.quantity],
        "reporte_stock.pdf",
        headers=["ID", "Producto", "Ubicación", "Cantidad"]
    )

def alerts_report(request):
    alerts = paginate_queryset(request, StockAlert.objects.all().order_by("-created_at"), per_page=5)
    return render(request, "reports/inventory/alerts_report.html", {"alerts": alerts})

def alerts_report_xlsx(request):
    return export_xlsx(
        StockAlert.objects.all(),
        ["ID", "Producto", "Ubicación", "Mínimo", "Fecha"],
        lambda qs: [[a.id, str(a.product), str(a.location), a.minimum_quantity, a.created_at.strftime("%Y-%m-%d")] for a in qs],
        "reporte_alertas.xlsx",
        "Alertas"
    )

def alerts_report_pdf(request):
    return export_pdf(
        StockAlert.objects.all(),
        "Reporte de Alertas",
        lambda a: [a.id, str(a.product), str(a.location), a.minimum_quantity, a.created_at.strftime("%Y-%m-%d")],
        "reporte_alertas.pdf",
        headers=["ID", "Producto", "Ubicación", "Mínimo", "Fecha"]
    )

def kardex_report(request):
    kardex = paginate_queryset(request, KardexEntry.objects.all().order_by("-date"), per_page=5)
    return render(request, "reports/inventory/kardex_report.html", {"kardex": kardex})

def kardex_report_xlsx(request):
    return export_xlsx(
        KardexEntry.objects.all(),
        ["ID", "Producto", "Tipo", "Cantidad", "Referencia", "Fecha"],
        lambda qs: [[k.id, str(k.product), k.entry_type, k.quantity, k.reference, k.date.strftime("%Y-%m-%d")] for k in qs],
        "reporte_kardex.xlsx",
        "Kardex"
    )

def kardex_report_pdf(request):
    return export_pdf(
        KardexEntry.objects.all(),
        "Reporte de Kardex",
        lambda k: [k.id, str(k.product), k.entry_type, k.quantity, k.reference, k.date.strftime("%Y-%m-%d")],
        "reporte_kardex.pdf",
        headers=["ID", "Producto", "Tipo", "Cantidad", "Referencia", "Fecha"]
    )

# ============================================================
# PROVEEDORES
# ============================================================

def suppliers_report(request):
    suppliers = paginate_queryset(request, Supplier.objects.all().order_by("name"), per_page=5)
    return render(request, "reports/suppliers/suppliers_report.html", {"suppliers": suppliers})

def suppliers_report_xlsx(request):
    return export_xlsx(
        Supplier.objects.all(),
        ["ID", "Nombre", "Contacto", "Teléfono", "Correo"],
        lambda qs: [[s.id, s.name, s.contact_name, s.phone, s.email] for s in qs],
        "reporte_proveedores.xlsx",
        "Proveedores"
    )

def suppliers_report_pdf(request):
    return export_pdf(
        Supplier.objects.all(),
        "Reporte de Proveedores",
        lambda s: [s.id, s.name, s.contact_name, s.phone, s.email],
        "reporte_proveedores.pdf",
        headers=["ID", "Nombre", "Contacto", "Teléfono", "Correo"]
    )