"""Prepara los ficheros de una sesión para la web pública del curso.

Convierte las presentaciones (.pptx) en PDF con LibreOffice y en una imagen PNG por
diapositiva, y copia los PDF que se repartieron. Todo fichero que sale lleva sus
metadatos (Autor, Título, Asunto, Palabras clave), por la regla de la bóveda.

Uso:  python herramientas/preparar_sesion.py 1
La lista de ficheros de cada sesión está en SESIONES, más abajo.

⚠️ Solo material de aula, sin datos del alumnado: lo que entra aquí se publica.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, PngImagePlugin
from pypdf import PdfReader, PdfWriter

RAIZ = Path(__file__).resolve().parent.parent
MATERIAL = Path(r"B:\ProyectoTestbuk\Boveda_Juan\08-Formacion\impartida"
                r"\curso-efli-herramientas-colaborativas\material-didactico-juan")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

CURSO = "Coordinación interadministrativa y herramientas colaborativas en la gestión pública"
AUTOR = "Juan Antonio Agudo García · juanantonioagudo@gmail.com"
CLAVES_BASE = f"{CURSO}; Diputación de Badajoz; inteligencia artificial; herramientas colaborativas"

# (origen relativo a MATERIAL, nombre publicado, título, palabras clave propias)
SESIONES = {
    1: {
        "presentaciones": [
            ("sesion-1/materiales-didacticos-sesion-1/Sesion-1-v6-Tu-modelo-de-trabajo-con-IA.pptx",
             "presentacion-sesion-1", "Sesión 1 · Tu modelo de trabajo con IA",
             "cuenta de Google; Chrome; asistentes de IA; prompt; token; contexto; privacidad; Gemini Notebook; formas de organizarse"),
        ],
        "pdf": [
            ("sesion-1/materiales-didacticos-sesion-1/chuleta-sesion-1-v6.pdf", "chuleta-sesion-1.pdf"),
            ("sesion-1/materiales-didacticos-sesion-1/ficha-formas-de-organizarse-v6.pdf", "ficha-formas-de-organizarse.pdf"),
            ("sesion-1/materiales-didacticos-sesion-1/ficha-herramientas-colaborativas-v6.pdf", "ficha-herramientas-colaborativas.pdf"),
        ],
        "imagenes": [
            ("sesion-1/materiales-didacticos-sesion-1/mapamundi-ia-v6.png", "mapamundi-ia.png",
             "Mapa de las IA", "asistentes de IA; ChatGPT; Claude; Gemini; Mistral; DeepSeek; Qwen"),
            ("sesion-1/materiales-didacticos-sesion-1/comparativa-ia-gratis-v6.png", "comparativa-ia-gratis.png",
             "Qué dan gratis las IA", "asistentes de IA; cuenta gratuita; comparativa"),
        ],
    },
}


def meta_png(img: Image.Image, destino: Path, titulo: str, claves: str, asunto: str) -> None:
    info = PngImagePlugin.PngInfo()
    info.add_itxt("Title", titulo)
    info.add_itxt("Author", AUTOR)
    info.add_itxt("Description", asunto)
    info.add_itxt("Keywords", f"{CLAVES_BASE}; {claves}")
    info.add_itxt("Copyright", "Juan Antonio Agudo García")
    img.save(destino, pnginfo=info, optimize=True)


def meta_pdf(origen: Path, destino: Path, titulo: str, asunto: str, claves: str) -> None:
    w = PdfWriter(clone_from=PdfReader(origen))
    w.add_metadata({"/Title": titulo, "/Author": AUTOR, "/Subject": asunto,
                    "/Keywords": f"{CLAVES_BASE}; {claves}"})
    with open(destino, "wb") as f:
        w.write(f)


def main(n: int) -> None:
    conf = SESIONES[n]
    salida = RAIZ / f"sesion-{n}"
    salida.mkdir(parents=True, exist_ok=True)
    asunto = f"{CURSO} — sesión {n}"
    with tempfile.TemporaryDirectory() as tmp:
        for origen, nombre, titulo, claves in conf["presentaciones"]:
            subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", tmp,
                            str(MATERIAL / origen)], check=True, capture_output=True)
            pdf_tmp = Path(tmp) / (Path(origen).stem + ".pdf")
            meta_pdf(pdf_tmp, salida / f"{nombre}.pdf", titulo, asunto, claves)
            carpeta = salida / "diapositivas"
            carpeta.mkdir(parents=True, exist_ok=True)
            doc = pdfium.PdfDocument(pdf_tmp)
            for i, pag in enumerate(doc, 1):
                img = pag.render(scale=1600 / pag.get_width()).to_pil()
                meta_png(img, carpeta / f"{i:02d}.png", f"{titulo} — diapositiva {i}", claves, asunto)
            print(f"{nombre}: {len(doc)} diapositivas")
            doc.close()
    for origen, nombre in conf["pdf"]:
        shutil.copy2(MATERIAL / origen, salida / nombre)  # ya llevan metadatos completos
    for origen, nombre, titulo, claves in conf.get("imagenes", []):
        meta_png(Image.open(MATERIAL / origen), salida / nombre, titulo, claves, asunto)
    print("hecho:", salida)


if __name__ == "__main__":
    main(int(sys.argv[1]))
