import pandas as pd
import re
import chardet
from typing import Tuple


def dms_to_decimal_degrees(d, m, s, direction):
    degrees = float(d) + float(m) / 60 + float(s) / 3600
    if direction in ["S", "W"]:
        degrees = -degrees
    return degrees


latitud = "Latitud en S R  WGS84 (cruce)"
longitud = "Longitud en S R  WGS84 (cruce)"

regex = re.compile(r"([0-9]+)º(\d+)'([0-9.]+)'' ([NEWS])")


def cambiar(location) -> Tuple[float, float]:
    lat = location[latitud]
    lon = location[longitud]

    match = regex.search(lat)
    if not match:
        print(match, lat)
    d, m, s, direction = match.group(1), match.group(2), match.group(3), match.group(4)
    lat = dms_to_decimal_degrees(d, m, s, direction)

    match = regex.search(lon)
    d, m, s, direction = match.group(1), match.group(2), match.group(3), match.group(4)
    lon = dms_to_decimal_degrees(d, m, s, direction)

    return lat, lon


def get_encoding(path) -> str:
    # Open the file in binary mode and read a portion for detection
    rawdata = open(path, "rb").read(1000)
    # Use chardet to detect the encoding
    result = chardet.detect(rawdata)

    # The detected encoding will be in the 'encoding' key of the result dictionary
    encoding = result["encoding"]

    return encoding.lower()


def cruces_read(path: str) -> pd.DataFrame:
    cruces = pd.read_csv(
        path,
        encoding_errors="replace",
        sep=";",
        encoding=get_encoding(path),
        low_memory=False,
    )
    return cruces


def clean_names(df: pd.DataFrame, columns) -> pd.DataFrame:
    df = df.copy()

    for col in columns:
        df[col] = df[col].str.strip()
    return df


def cruces_as_int(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    columns = [
        "Codigo de vía tratado",
        "Codigo de via que cruza o enlaza",
        "Coordenada X (Guia Urbana) cm (cruce)",
        "Coordenada Y (Guia Urbana) cm (cruce)",
    ]
    for col in columns:
        if df[col].dtype != "int64":
            df[col] = df[col].astype("int")
    return df


def direcciones_read(path: str) -> pd.DataFrame:
    direcciones = pd.read_csv(
        path,
        encoding_errors="replace",
        sep=";",
        encoding=get_encoding(path),
        low_memory=False,
    )
    return direcciones


def direcciones_as_int(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    pattern = re.compile(r"0*([+-]?(:?\d+))")

    for col in ["Coordenada X (Guia Urbana) cm", "Coordenada Y (Guia Urbana) cm"]:
        df[col] = df[col].apply(lambda x: pattern.match(x).group(1)).astype("int")
    return df


def literal_split(df: pd.DataFrame) -> pd.DataFrame:
    pattern = re.compile(r"(KM\.|NUM)?(\d+)([A-Za-z]*)?")
    df = df.copy()

    df[["Prefijo de numeracion", "Numero", "Sufijo de numeracion"]] = df[
        "Literal de numeracion"
    ].str.extract(pattern)
    df["Numero"] = df["Numero"].astype("int")
    return df


def join_name(r, clase, particula, nombre) -> str:
    r[clase] = r[clase].capitalize()
    r[particula] = r[particula].lower()
    r[nombre] = r[nombre].title()
    return " ".join(r).replace("  ", " ")


def process_data(
    path_cruces: str, path_direcciones: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    columns_cruces = [
        "Literal completo del vial tratado",
        "Literal completo del vial que cruza",
        "Clase de la via tratado",
        "Clase de la via que cruza",
        "Particula de la via tratado",
        "Particula de la via que cruza",
        "Nombre de la via tratado",
        "Nombre de la via que cruza",
    ]

    columns_via_tratado = [
        "Clase de la via tratado",
        "Particula de la via tratado",
        "Nombre de la via tratado",
    ]
    columns_via_cruza = [
        "Clase de la via que cruza",
        "Particula de la via que cruza",
        "Nombre de la via que cruza",
    ]

    columns_direcciones = ["Clase de la via", "Partícula de la vía", "Nombre de la vía"]

    cruces = cruces_as_int(
        clean_names(cruces_read(path_cruces), columns_cruces).drop_duplicates()
    )

    cruces["latitud"], cruces["longitud"] = zip(
        *cruces[[latitud, longitud]].apply(lambda x: cambiar(x), axis=1)
    )
    direcciones = literal_split(
        direcciones_as_int(
            clean_names(direcciones_read(path_direcciones), columns_direcciones)
        ).drop_duplicates()
    )

    cruces["Nombre completo de la via tratado"] = cruces[columns_via_tratado].apply(
        lambda r: join_name(r, *columns_via_tratado), axis=1
    )
    cruces["Nombre completo de la via que cruza"] = cruces[columns_via_cruza].apply(
        lambda r: join_name(r, *columns_via_cruza), axis=1
    )

    direcciones["Nombre completo de la via"] = direcciones[columns_direcciones].apply(
        lambda r: join_name(r, *columns_direcciones), axis=1
    )
    return (cruces, direcciones)
