from typing import List
from pydantic import BaseModel


class DisposicionBoe(BaseModel):
    boe_num: str
    fecha_de_publicacion: str
    pdf_link: str
    contenido: str


class Boe(BaseModel):
    boe_num: str
    fecha_de_publicacion: str
    link: str
    contenido: str
    disposiciones: List[DisposicionBoe]


