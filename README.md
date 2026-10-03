# RSL – IA Generativa Multimodal en HRI para Robótica Social (ATI2)

| Archivo | Contenido |
|---|---|
| `Avance3.Seminario-Ordaya.pdf` | Artículo compilado (metodología de la RSL, formato Springer LNCS) |
| `Overleaf_ATI2.Seminario-Ordaya.zip` | Proyecto LaTeX listo para subir a Overleaf (New Project → Upload Project) |
| `articulo/` | Fuentes LaTeX (`main.tex`, tabla y referencias de estudios incluidos) |
| `Base_de_datos.Seminario-Ordaya.xlsx` | Ecuaciones, 942 registros con decisión PRISMA y motivo, incluidos y conteos |
| `Formulario.Seminario-Ordaya.xlsx` | Formulario de extracción con datos de los 22 estudios incluidos (lectura a texto completo) |
| `scripts/`, `data/` | Búsqueda reproducible (Semantic Scholar y Crossref), cribado y generación de archivos |

Reproducir: `cd scripts && python3 s2.py && python3 cr.py && python3 proc.py && python3 screen.py && python3 build.py && python3 tex_parts.py`
Textos completos: `fetch_ft.py`, `fetch_ft2.py`, `fetch_browser.js` (los PDF no se versionan). Datos extraídos: `data/extraccion.py`.
