#!/ usr/bin/env python

 # make sure to install these packages before running :
 # pip install pandas
 # pip install sodapy
import pandas as pd
from sodapy import Socrata
from ui import limite_consultas, departamento_solicitado, municipio_solicitado, cultivo_solicitado
from statistics import median


 # Unauthenticated client only works with public data sets . Note ’None ’
 # in place of application token , and no username or password :
client = Socrata("www.datos.gov.co", None)

 # Example authenticated client ( needed for non - public datasets ):
 # client = Socrata (www. datos .gov.co ,
 # MyAppToken ,
 # username =" user@example . com" ,
 # password =" AFakePassword ")

 # First 2000 results , returned as JSON from API / converted to Python list of
 # dictionaries by sodapy
results = client.get("ch4u-f3i5", limit=limite_consultas)

 # Convert to pandas DataFrame
df = pd.DataFrame.from_records(results)


def mediana_variables_edaficas(resultado):
    resultado = resultado.copy()
    for columna in ["ph_agua_suelo_2_5_1_0", "f_sforo_p_bray_ii_mg_kg", "potasio_k_intercambiable_cmol_kg"]:
        if any(isinstance(value, str) for value in resultado[columna]):
            resultado.loc[:, columna]= pd.to_numeric(resultado[columna], errors='coerce')

        resultado.dropna(subset=[columna], inplace=True)

    mediana_ph = resultado["ph_agua_suelo_2_5_1_0"].median()
    mediana_fosforo = resultado["f_sforo_p_bray_ii_mg_kg"].median()
    mediana_potasio = resultado["potasio_k_intercambiable_cmol_kg"].median()

    mediana_edafica = pd.DataFrame({"mediana_ph": mediana_ph, "mediana_fosforo": mediana_fosforo, "mediana_potasio": mediana_potasio},index=[0])

    return mediana_edafica



def hacer_consulta_y_ver_resultado():  #en resultado se hace la consulta, en resultado_mediana llamo a la funcion de mediana y en resultado_total toda la tabla concatenada con la de medianas

    resultado = df[(df["departamento"] == departamento_solicitado) & (df["municipio"] == municipio_solicitado) & (df["cultivo"] == cultivo_solicitado)]
    resultado_mediana = mediana_variables_edaficas(resultado)
    resultado_total = pd.concat([resultado.loc[:, ["departamento", "municipio", "cultivo", "topografia"]], resultado_mediana], axis = 1).to_string(index = False)

    print(resultado_total)


