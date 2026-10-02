"""Copia a img/ las diapositivas que Juan elige para cada sesión, con sus metadatos.

La web enseña solo 4 o 5 diapositivas por sesión: las que se proyectaron y sirven
para recordar. La elección es de Juan; aquí solo se apunta. Uso:  python herramientas/preparar_sesion.py
"""
from pathlib import Path

from PIL import Image, PngImagePlugin

RAIZ = Path(__file__).resolve().parent.parent
MATERIAL = Path(r"B:\ProyectoTestbuk\Boveda_Juan\08-Formacion\impartida"
                r"\curso-efli-herramientas-colaborativas\material-didactico-juan")
CURSO = "Coordinación interadministrativa y herramientas colaborativas en la gestión pública"
AUTOR = "Juan Antonio Agudo García · juanantonioagudo@gmail.com"

# (sesión, origen relativo a MATERIAL —o ruta absoluta—, nombre publicado, título)
# Las de la sesión 1 salieron de pasar Sesion-1-v6-Tu-modelo-de-trabajo-con-IA.pptx a PNG (LibreOffice + pypdfium2, 1600 px).
ELEGIDAS = [
    (1, RAIZ / "sesion-1/diapositivas/10.png", "s1-mapa-de-las-ia.png", "El mapa de las IA"),
    (1, RAIZ / "sesion-1/diapositivas/13.png", "s1-ocho-palabras.png", "Ocho palabras que conviene conocer"),
    (1, RAIZ / "sesion-1/diapositivas/21.png", "s1-por-que-tanto-cuidado.png", "¿Por qué tanto cuidado?"),
    (1, RAIZ / "sesion-1/diapositivas/24.png", "s1-cuatro-formas.png", "Cuatro formas de organizarse"),
    (2, "sesion-2/materiales-didacticos-sesion-2/presentacion-formas-de-organizarse-v6.png", "s2-las-cuatro-cara-a-cara.png", "Las cuatro formas, cara a cara"),
    (2, "sesion-2/materiales-didacticos-sesion-2/comparativa-ia-gratis-v6.png", "s2-que-dan-gratis-las-ia.png", "¿Qué te deja hacer gratis cada IA?"),
    (2, "sesion-2-impartida/materiales-impartidos-sesion-2/herramientas-colaborativas-google.png", "s2-herramientas-colaborativas.png", "Herramientas colaborativas: tres familias"),
    (2, "sesion-2/materiales-didacticos-sesion-2/encabezado-documento-versionado-v1.png", "s2-encabezado-versionado.png", "Encabezado de control de un documento que se versiona"),
]


def main() -> None:
    (RAIZ / "img").mkdir(exist_ok=True)
    for n, origen, nombre, titulo in ELEGIDAS:
        info = PngImagePlugin.PngInfo()
        info.add_itxt("Title", titulo)
        info.add_itxt("Author", AUTOR)
        info.add_itxt("Description", f"{CURSO} — sesión {n}")
        info.add_itxt("Keywords", f"{CURSO}; Diputación de Badajoz; sesión {n}; {titulo}")
        info.add_itxt("Copyright", "Juan Antonio Agudo García")
        Image.open(MATERIAL / origen).save(RAIZ / "img" / nombre, pnginfo=info, optimize=True)
        print("ok", nombre)


if __name__ == "__main__":
    main()
