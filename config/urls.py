from django.urls import path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ingestion.views import (
    upload_sap, upload_utility, upload_travel,
    list_records, approve_record, flag_record
)

def homepage(request):
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Breathe ESG</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f4f6f8;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .container { max-width: 560px; width: 100%; }
    .header { text-align: center; margin-bottom: 36px; }
    .header h1 { font-size: 26px; font-weight: 700; color: #1a1a1a; }
    .header p  { color: #666; font-size: 14px; margin-top: 6px; }

    .section-title {
      font-size: 11px; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.08em; color: #999; margin-bottom: 10px;
    }

    .card {
      background: #fff;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      padding: 20px 24px;
      margin-bottom: 16px;
    }

    .link-row {
      display: flex; align-items: center; gap: 14px;
      padding: 12px 0; border-bottom: 1px solid #f0f0f0;
      text-decoration: none; color: inherit;
      transition: background 0.15s;
      border-radius: 8px;
      padding: 10px 8px;
    }
    .link-row:last-child { border-bottom: none; }
    .link-row:hover { background: #f9fafb; }

    .icon {
      width: 36px; height: 36px; border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 17px; flex-shrink: 0;
    }
    .icon.blue    { background: #eff6ff; }
    .icon.green   { background: #f0fdf4; }
    .icon.amber   { background: #fffbeb; }
    .icon.red     { background: #fef2f2; }
    .icon.purple  { background: #f5f3ff; }

    .link-text strong { font-size: 14px; font-weight: 600; color: #1a1a1a; display: block; }
    .link-text span   { font-size: 12px; color: #888; }

    .arrow { margin-left: auto; color: #ccc; font-size: 16px; }

    .badge {
      margin-left: auto; margin-right: 8px;
      background: #f0fdf4; color: #166534;
      font-size: 11px; font-weight: 600;
      padding: 2px 8px; border-radius: 20px;
    }
    .badge.warning { background: #fffbeb; color: #92400e; }
  </style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🌿 Breathe ESG</h1>
    <p>Emissions data ingestion and analyst review platform</p>
  </div>

  <!-- Main actions -->
  <p class="section-title">Dashboard</p>
  <div class="card">
    <a href="/api/records/" class="link-row">
      <div class="icon blue">📋</div>
      <div class="link-text">
        <strong>View All Records</strong>
        <span>Browse, filter and approve emission records</span>
      </div>
      <span class="arrow">›</span>
    </a>
    <a href="/admin/" class="link-row">
      <div class="icon purple">⚙️</div>
      <div class="link-text">
        <strong>Admin Panel</strong>
        <span>Manage data sources, records and audit logs</span>
      </div>
      <span class="arrow">›</span>
    </a>
  </div>

  <!-- Upload -->
  <p class="section-title">Upload Data</p>
  <div class="card">
    <a href="/api/upload/sap/" class="link-row">
      <div class="icon blue">🏭</div>
      <div class="link-text">
        <strong>SAP — Fuel & Procurement</strong>
        <span>Scope 1 · Diesel, petrol, fuel consumption</span>
      </div>
      <span class="arrow">›</span>
    </a>
    <a href="/api/upload/utility/" class="link-row">
      <div class="icon green">⚡</div>
      <div class="link-text">
        <strong>Utility — Electricity</strong>
        <span>Scope 2 · Meter readings, kWh billing data</span>
      </div>
      <span class="arrow">›</span>
    </a>
    <a href="/api/upload/travel/" class="link-row">
      <div class="icon amber">✈️</div>
      <div class="link-text">
        <strong>Travel — Flights & Ground</strong>
        <span>Scope 3 · Flights, trains, car journeys</span>
      </div>
      <span class="arrow">›</span>
    </a>
  </div>

  <!-- Footer note -->
  <p style="text-align:center; font-size:12px; color:#bbb; margin-top:8px;">
    Breathe ESG · Prototype · DEFRA 2023 emission factors
  </p>

</div>
</body>
</html>
    """)

urlpatterns = [
    path('', homepage),
    path('admin/', admin.site.urls),
    path('api/upload/sap/',                upload_sap),
    path('api/upload/utility/',            upload_utility),
    path('api/upload/travel/',             upload_travel),
    path('api/records/',                   list_records),
    path('api/records/<int:pk>/approve/',  approve_record),
    path('api/records/<int:pk>/flag/',     flag_record),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)