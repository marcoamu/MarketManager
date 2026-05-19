"""Analysis helpers for MarketManager - simulation module."""

from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import datetime


def generateAnalisysData(buyValues, sellvalues, normalValues, active):
    nada = ""
    try:
        from openpyxl import Workbook
        from openpyxl import load_workbook
        from datetime import datetime

        resData = list()
        for x in buyValues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in sellvalues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])
        for x in normalValues:
            resData.append(x["resData_Normal"])
        fecha_hora_actual = datetime.now()

        # Convertir la fecha y hora en una cadena de texto
        fecha_hora_string = fecha_hora_actual.strftime("%Y-%m-%d_%H-%M-%S")
        activeName = active.parameters.name+"_"+str(fecha_hora_string)
        nombre_archivo = f"f:\\SALIDA\\{activeName}.xlsx"
        libro_trabajo_existente = Workbook()
        # Comprobar si el archivo ya existe
        try:
            libro_trabajo_existente = load_workbook(nombre_archivo)
            # Si el archivo existe, elimina todas las hojas excepto la primera (por defecto)
            libro_trabajo_existente.remove(libro_trabajo_existente.active)
            # Obtén la hoja activa del libro de trabajo existente
            # hoja = libro_trabajo_existente.active
        except FileNotFoundError:
            # Si el archivo no existe, crea uno nuevo
            libro_trabajo_existente = Workbook()
            # hoja = libro_trabajo_existente.active
            # Agrega una fila con los títulos de los campos

        hoja = libro_trabajo_existente.active
        titulos = list(resData[0].keys())
        hoja.append(titulos)

        # Llenar la hoja con los datos de los diccionarios
        for fila_dict in resData:
            fila = [fila_dict[titulo] for titulo in titulos]
            hoja.append(fila)

        for columna in hoja.columns:
            max_length = 0
            for celda in columna:
                try:
                    if len(str(celda.value)) > max_length:
                        max_length = len(celda.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            hoja.column_dimensions[columna[0].column_letter].width = adjusted_width

        # Guardar el libro de trabajo en un archivo (sobrescribiendo si ya existe)
        libro_trabajo_existente.save(nombre_archivo)
    except Exception as e:
        print(f"error generateAnalisysData :{str(e)}")


def generateAnalisysDataColoredOK(buyValues, sellvalues, normalValues, active):
    try:
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import PatternFill
        from openpyxl.formatting.rule import FormulaRule
        from openpyxl.utils import get_column_letter
        from datetime import datetime

        # =========================
        # COLORES
        # =========================
        green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        yellow_fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")

        # =========================
        # RECOLECTAR DATOS
        # =========================
        resData = []

        for x in buyValues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in sellvalues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in normalValues:
            resData.append(x["resData_Normal"])

        if not resData:
            print("No hay datos para exportar")
            return

        # =========================
        # NOMBRE ARCHIVO
        # =========================
        fecha_hora_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        activeName = active.parameters.name + "_" + fecha_hora_string
        nombre_archivo = f"f:\\SALIDA\\{activeName}.xlsx"

        # =========================
        # CREAR / CARGAR EXCEL
        # =========================
        try:
            libro = load_workbook(nombre_archivo)
            libro.remove(libro.active)
        except FileNotFoundError:
            libro = Workbook()

        hoja = libro.active

        # =========================
        # CABECERAS
        # =========================
        titulos = list(resData[0].keys())
        hoja.append(titulos)

        # Índices clave
        idx_start = titulos.index("START") if "START" in titulos else None
        idx_is_buy = titulos.index("IS_BUY") if "IS_BUY" in titulos else None

        # =========================
        # INSERTAR DATOS + COLOR FILA
        # =========================
        for fila_dict in resData:
            fila = [fila_dict.get(t, None) for t in titulos]
            hoja.append(fila)

            if idx_start is not None and idx_is_buy is not None:
                start_val = fila[idx_start]
                is_buy_val = fila[idx_is_buy]

                # Normalizar valores por si vienen como string
                start_val = str(start_val).lower() == "true"
                is_buy_val = str(is_buy_val).lower() == "true"

                if start_val:
                    fill = green_fill if is_buy_val else red_fill
                    row_num = hoja.max_row

                    for col in range(1, len(titulos) + 1):
                        hoja.cell(row=row_num, column=col).fill = fill

        # =========================
        # FORMATO CONDICIONAL PRO
        # =========================
        max_row = hoja.max_row
        max_col = hoja.max_column

        for col in range(1, max_col + 1):
            col_letter = get_column_letter(col)
            rango_col = f"{col_letter}2:{col_letter}{max_row}"

            hoja.conditional_formatting.add(
                rango_col,
                FormulaRule(formula=[f'ISNUMBER(SEARCH("BUY",{col_letter}2))'], fill=green_fill)
            )
            hoja.conditional_formatting.add(
                rango_col,
                FormulaRule(formula=[f'ISNUMBER(SEARCH("SELL",{col_letter}2))'], fill=red_fill)
            )
            hoja.conditional_formatting.add(
                rango_col,
                FormulaRule(formula=[f'ISNUMBER(SEARCH("WAIT",{col_letter}2))'], fill=yellow_fill)
            )

        # =========================
        # AUTOAJUSTE COLUMNAS
        # =========================
        for columna in hoja.columns:
            max_length = 0
            for celda in columna:
                try:
                    if celda.value:
                        max_length = max(max_length, len(str(celda.value)))
                except:
                    pass

            adjusted_width = (max_length + 2) * 1.2
            hoja.column_dimensions[columna[0].column_letter].width = adjusted_width

        # =========================
        # GUARDAR
        # =========================
        libro.save(nombre_archivo)

    except Exception as e:
        print(f"error generateAnalisysData :{str(e)}")


def generateAnalisysDataColored(buyValues, sellvalues, normalValues, active):
    try:
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import PatternFill
        from datetime import datetime

        # Colores
        green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

        resData = list()
        for x in buyValues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in sellvalues:
            if "resData_Start" in x:
                resData.append(x["resData_Start"])
            if "resData_Stop" in x:
                resData.append(x["resData_Stop"])

        for x in normalValues:
            resData.append(x["resData_Normal"])

        fecha_hora_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        activeName = active.parameters.name + "_" + fecha_hora_string
        nombre_archivo = f"f:\\SALIDA\\{activeName}.xlsx"

        try:
            libro_trabajo_existente = load_workbook(nombre_archivo)
            libro_trabajo_existente.remove(libro_trabajo_existente.active)
        except FileNotFoundError:
            libro_trabajo_existente = Workbook()

        hoja = libro_trabajo_existente.active

        titulos = list(resData[0].keys())
        hoja.append(titulos)

        # Índices de columnas importantes
        idx_start = titulos.index("START")
        idx_is_buy = titulos.index("IS_BUY")

        # Llenar datos
        for fila_dict in resData:
            fila = [fila_dict[titulo] for titulo in titulos]
            hoja.append(fila)

            # Evaluar condiciones
            start_val = fila[idx_start]
            is_buy_val = fila[idx_is_buy]

            if start_val:  # START == True
                fill = green_fill if is_buy_val else red_fill

                # Aplicar color a toda la fila recién añadida
                row_num = hoja.max_row
                for col in range(1, len(titulos) + 1):
                    hoja.cell(row=row_num, column=col).fill = fill

        # Ajustar ancho de columnas
        for columna in hoja.columns:
            max_length = 0
            for celda in columna:
                try:
                    if len(str(celda.value)) > max_length:
                        max_length = len(str(celda.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            hoja.column_dimensions[columna[0].column_letter].width = adjusted_width

        libro_trabajo_existente.save(nombre_archivo)

    except Exception as e:
        print(f"error generateAnalisysData :{str(e)}")


def evaluateMarketMovements(buyValues, sellValues, sortedList = False):
    buyAccumulated = 0
    sellAccumulated = 0
    if buyValues is not None and len(buyValues) > 0:

        print(f" BUY MOVEMENTS")
        if sortedList:
            mi_lista_ordenada = sorted(buyValues, key=lambda x: float(x['STOP'])-float(x['START']), reverse=True)
        else:
            mi_lista_ordenada = buyValues
        for x in mi_lista_ordenada:
            try:
                start = float(x['START'])
                start_date = x['START_DATE']
                stop = float(x['STOP'])
                stop_date = x['STOP_DATE']
                val = stop - start
                buyAccumulated = buyAccumulated + val
                print(f" start: {start} start_date: {start_date} stop: {stop} stop_date: {stop_date} value :{val}")
            except Exception as e:
                print(f"ERROR evaluateMarketMovements {str(e)}")
        print(f"TOTAL BUY VALUE: {buyAccumulated}")

    if sellValues is not None and len(sellValues) > 0:
        print(f" SELL MOVEMENTS")
        if sortedList:
            mi_lista_ordenada = sorted(sellValues, key=lambda x: float(x['STOP'])-float(x['START']), reverse=True)
        else:
            mi_lista_ordenada = sellValues
        for x in mi_lista_ordenada:
            try:
                start = float(x['START'])
                start_date = x['START_DATE']
                stop = float(x['STOP'])
                stop_date = x['STOP_DATE']
                val = start - stop
                sellAccumulated = sellAccumulated + val
                print(f" start: {start} start_date: {start_date} stop: {stop} stop_date: {stop_date} value :{val}")

            except Exception as e:

                print(f"ERROR sellValues {str(e)}")
        print(f"TOTAL SELL VALUE: {sellAccumulated}")
    print(f"Numero de operaciones BUY {len(buyValues)}")
    print(f"Numero de operaciones SELL {len(sellValues)}")
    if sellAccumulated is not None and buyAccumulated is not None:
        print(f"TOTAL GANANCIAS {buyAccumulated + sellAccumulated}")
    return buyAccumulated, sellAccumulated




