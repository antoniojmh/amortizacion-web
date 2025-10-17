from __future__ import annotations
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def calcular_amortizacion(monto: float, cuotas: int, tasa_periodica: float, fecha_inicio: datetime) -> pd.DataFrame:
    P = monto
    r = tasa_periodica
    n = cuotas
    if r == 0:
        cuota = P / n
    else:
        cuota = r * P / (1 - (1 + r) ** (-n))

    filas = []
    saldo = P
    fecha = fecha_inicio
    for i in range(1, n + 1):
        interes = saldo * r
        abono = cuota - interes
        if i == n:
            abono = saldo
            cuota = interes + abono
            saldo_fin = 0.0
        else:
            saldo_fin = saldo - abono
        filas.append({
            'Per': i,
            'Fecha': fecha.strftime('%Y-%m-%d'),
            'Saldo_Inic': round(saldo, 2),
            'Interes': round(interes, 2),
            'Abono': round(abono, 2),
            'Cuota': round(cuota, 2),
            'Saldo_Fin': round(saldo_fin, 2)
        })
        saldo = saldo_fin
        fecha = fecha + relativedelta(months=+1)

    return pd.DataFrame(filas)

def generar_pdf(df, monto, cuotas, tasa_periodica, salida, moneda, fecha_generacion):
    doc = SimpleDocTemplate(salida, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(f'Amortización - {cuotas} cuotas | Generado: {fecha_generacion.strftime("%d/%m/%Y, %H:%M:%S")}', styles['Title'])
    story.append(title)
    story.append(Spacer(1, 6))

    info = Paragraph(f'<b>Monto:</b> {moneda} {monto:,.2f} | <b>Tasa:</b> {tasa_periodica*100:.2f}% por periodo', styles['Normal'])
    story.append(info)
    story.append(Spacer(1, 8))

    table_data = [['Per', 'Fecha', 'Saldo Inic', 'Interés', 'Abono', 'Cuota', 'Saldo Fin']]
    for _, row in df.iterrows():
        table_data.append([
            int(row['Per']), row['Fecha'],
            f"{moneda} {row['Saldo_Inic']:,.2f}",
            f"{moneda} {row['Interes']:,.2f}",
            f"{moneda} {row['Abono']:,.2f}",
            f"{moneda} {row['Cuota']:,.2f}",
            f"{moneda} {row['Saldo_Fin']:,.2f}"
        ])

    tbl = Table(table_data, repeatRows=1, hAlign='LEFT')
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)

    doc.build(story)
