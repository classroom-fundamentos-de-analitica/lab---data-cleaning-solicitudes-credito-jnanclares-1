"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd
import re
from datetime import datetime


def clean_data():

    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)

    #null and dups
    df = df.dropna(axis=0)
    df = df.drop_duplicates()

    #uppercase and lowercase
    cat_cols = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', "barrio"]

    df[cat_cols] = df[cat_cols].apply(lambda x: x.str.lower())

    #modify spaces and replace values
    cols_to_modify_spaces = ["idea_negocio", "barrio", "línea_credito"]

    df[cols_to_modify_spaces] = df[cols_to_modify_spaces].apply(lambda x: x.str.replace("-", " "))
    df[cols_to_modify_spaces] = df[cols_to_modify_spaces].apply(lambda x: x.str.replace("_", " "))

    # convert comuna to int
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    #format monto_del_credito
    df["monto_del_credito"] = df["monto_del_credito"].str.strip("$")
    df["monto_del_credito"] = df["monto_del_credito"].apply(lambda x: x.replace(",", "").strip())
    df["monto_del_credito"] = df["monto_del_credito"].apply(lambda x: x.split(".")).str[0]

    #date
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d") if (len(re.findall("^\d+/", x)[0]) - 1) == 4 else datetime.strptime(x, "%d/%m/%Y"))

    #drop dups again
    df.drop_duplicates(inplace = True)

    return df
