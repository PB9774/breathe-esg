from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.utils import timezone
from .models import DataSource, EmissionRecord, AuditLog
import csv, io


# ─── SAP (Scope 1 — Fuel/Procurement) ───────────────────────────────────────

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_sap(request):
    file = request.FILES['file']
    source = DataSource.objects.create(
        name=file.name,
        source_type='SAP',
        client_name=request.data.get('client', 'demo'),
        uploaded_file=file
    )
    file.seek(0) 
    decoded = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    count = 0
    for row in reader:
        qty = float(row.get('quantity', 0) or 0)
        unit = row.get('unit', '').strip().upper()
        if unit == 'L':
            co2e = qty * 2.68      # diesel: 2.68 kg CO2e per litre (DEFRA 2023)
        elif unit == 'KG':
            co2e = qty * 2.54      # petrol approximation
        else:
            co2e = qty * 2.68      # default to diesel factor

        suspicious = qty > 100000
        EmissionRecord.objects.create(
            source=source,
            raw_data=dict(row),
            activity_description=row.get('material', 'Unknown material'),
            quantity=qty,
            unit=unit or 'L',
            co2e_kg=round(co2e, 4),
            scope=1,
            is_suspicious=suspicious,
            suspicious_reason='Unusually high quantity' if suspicious else ''
        )
        count += 1
    return Response({'source': source.id, 'records_created': count})


# ─── Utility (Scope 2 — Electricity) ────────────────────────────────────────

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_utility(request):
    file = request.FILES['file']
    source = DataSource.objects.create(
        name=file.name,
        source_type='UTILITY',
        client_name=request.data.get('client', 'demo'),
        uploaded_file=file
    )
    file.seek(0) 
    decoded = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    count = 0
    for row in reader:
        kwh = float(row.get('kwh', 0) or 0)
        co2e = kwh * 0.233         # UK grid average: 0.233 kg CO2e per kWh (DEFRA 2023)

        suspicious = kwh > 500000  # flag if over 500,000 kWh in one bill
        EmissionRecord.objects.create(
            source=source,
            raw_data=dict(row),
            activity_description=f"Meter {row.get('meter_id', 'unknown')} — {row.get('billing_period', '')}",
            quantity=kwh,
            unit='kWh',
            co2e_kg=round(co2e, 4),
            scope=2,
            is_suspicious=suspicious,
            suspicious_reason='Unusually high kWh reading' if suspicious else ''
        )
        count += 1
    return Response({'source': source.id, 'records_created': count})


# ─── Travel (Scope 3 — Flights / Ground) ────────────────────────────────────

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_travel(request):
    file = request.FILES['file']
    source = DataSource.objects.create(
        name=file.name,
        source_type='TRAVEL',
        client_name=request.data.get('client', 'demo'),
        uploaded_file=file
    )
    file.seek(0)
    decoded = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    count = 0
    for row in reader:
        distance_km = float(row.get('distance_km', 0) or 0)
        mode = row.get('mode', 'flight').strip().lower()

        # Emission factors per passenger-km (DEFRA 2023)
        factors = {
            'flight': 0.255,
            'train':  0.041,
            'car':    0.168,
            'taxi':   0.149,
        }
        factor = factors.get(mode, 0.255)  # default to flight if unknown
        co2e = distance_km * factor

        suspicious = distance_km > 20000   # flag if single trip > 20,000 km
        EmissionRecord.objects.create(
            source=source,
            raw_data=dict(row),
            activity_description=f"{row.get('origin','?')} → {row.get('destination','?')} ({mode})",
            quantity=distance_km,
            unit='km',
            co2e_kg=round(co2e, 4),
            scope=3,
            is_suspicious=suspicious,
            suspicious_reason='Unusually long trip distance' if suspicious else ''
        )
        count += 1
    return Response({'source': source.id, 'records_created': count})


# ─── List all records ────────────────────────────────────────────────────────

@api_view(['GET'])
def list_records(request):
    records = EmissionRecord.objects.select_related('source').order_by('-id')
    data = []
    for r in records:
        data.append({
            'id': r.id,
            'source_type': r.source.source_type,
            'source_name': r.source.name,
            'client': r.source.client_name,
            'description': r.activity_description,
            'quantity': r.quantity,
            'unit': r.unit,
            'co2e_kg': r.co2e_kg,
            'scope': r.scope,
            'status': r.status,
            'is_suspicious': r.is_suspicious,
            'suspicious_reason': r.suspicious_reason,
            'approved_at': r.approved_at,
        })
    return Response(data)


# ─── Approve a record ────────────────────────────────────────────────────────

@api_view(['POST'])
def approve_record(request, pk):
    try:
        record = EmissionRecord.objects.get(pk=pk)
    except EmissionRecord.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if record.status == 'approved':
        return Response({'error': 'Already approved'}, status=400)

    record.status = 'approved'
    record.approved_at = timezone.now()
    record.save()

    AuditLog.objects.create(
        record=record,
        action='approved',
        note=request.data.get('note', '')
    )
    return Response({'status': 'approved', 'approved_at': record.approved_at})


# ─── Flag a record ───────────────────────────────────────────────────────────

@api_view(['POST'])
def flag_record(request, pk):
    try:
        record = EmissionRecord.objects.get(pk=pk)
    except EmissionRecord.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    record.status = 'flagged'
    record.is_suspicious = True
    record.suspicious_reason = request.data.get('reason', 'Manually flagged by analyst')
    record.save()

    AuditLog.objects.create(
        record=record,
        action='flagged',
        note=record.suspicious_reason
    )
    return Response({'status': 'flagged'})