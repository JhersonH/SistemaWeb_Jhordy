from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    # Transporte
    path("trips/", views.trips_report, name="trips_report"),
    path("trips/xlsx/", views.trips_report_xlsx, name="trips_report_xlsx"),
    path("trips/pdf/", views.trips_report_pdf, name="trips_report_pdf"),

    path("incidents/", views.incidents_report, name="incidents_report"),
    path("incidents/xlsx/", views.incidents_report_xlsx, name="incidents_report_xlsx"),
    path("incidents/pdf/", views.incidents_report_pdf, name="incidents_report_pdf"),

    path("expenses/", views.expenses_report, name="expenses_report"),
    path("expenses/xlsx/", views.expenses_report_xlsx, name="expenses_report_xlsx"),
    path("expenses/pdf/", views.expenses_report_pdf, name="expenses_report_pdf"),

    # Inventario
    path("receptions/", views.receptions_report, name="receptions_report"),
    path("receptions/xlsx/", views.receptions_report_xlsx, name="receptions_report_xlsx"),
    path("receptions/pdf/", views.receptions_report_pdf, name="receptions_report_pdf"),

    path("movements/", views.movements_report, name="movements_report"),
    path("movements/xlsx/", views.movements_report_xlsx, name="movements_report_xlsx"),
    path("movements/pdf/", views.movements_report_pdf, name="movements_report_pdf"),

    path("adjustments/", views.adjustments_report, name="adjustments_report"),
    path("adjustments/xlsx/", views.adjustments_report_xlsx, name="adjustments_report_xlsx"),
    path("adjustments/pdf/", views.adjustments_report_pdf, name="adjustments_report_pdf"),

    path("stock/", views.stock_report, name="stock_report"),
    path("stock/xlsx/", views.stock_report_xlsx, name="stock_report_xlsx"),
    path("stock/pdf/", views.stock_report_pdf, name="stock_report_pdf"),

    path("alerts/", views.alerts_report, name="alerts_report"),
    path("alerts/xlsx/", views.alerts_report_xlsx, name="alerts_report_xlsx"),
    path("alerts/pdf/", views.alerts_report_pdf, name="alerts_report_pdf"),

    path("kardex/", views.kardex_report, name="kardex_report"),
    path("kardex/xlsx/", views.kardex_report_xlsx, name="kardex_report_xlsx"),
    path("kardex/pdf/", views.kardex_report_pdf, name="kardex_report_pdf"),

    # Proveedores
    path("suppliers/", views.suppliers_report, name="suppliers_report"),
    path("suppliers/xlsx/", views.suppliers_report_xlsx, name="suppliers_report_xlsx"),
    path("suppliers/pdf/", views.suppliers_report_pdf, name="suppliers_report_pdf"),
]
