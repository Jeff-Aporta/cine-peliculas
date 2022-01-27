import random
import requests
import os
import json


def myfunc(e):
    return e["nombre"]


def ordenar_peliculas_alfabeticamente():
    with open('lista.json', encoding='utf8') as f:
        txt = "\n".join(f.readlines())
        js = json.loads(txt)
        js.sort(key=myfunc)
        arr = []
        for j in js:
            if j.get("descargaMega") or j.get("descargaTorrent"):
                arr.append(j)
        js = arr
        g = open("peliculas-a-z.json", "w", encoding='utf-8')
        g.write(json.dumps(js, ensure_ascii=False))
        g.close()

# ordenar_peliculas_alfabeticamente()


def obtenerLinks():
    links = ""
    peliculas_a_z = open('peliculas-a-z.json', encoding='utf8')
    txt = "\n".join(peliculas_a_z.readlines())
    js = json.loads(txt)
    for j in js:
        if j.get("descargaMega"):
            links += j.get("descargaMega")+"\n"
    g = open("links.txt", "w", encoding='utf-8')
    g.write(links)
    g.close()
    peliculas_a_z.close()

# obtenerLinks()


def intercambiarLinks():
    peliculas_a_z = open('peliculas-a-z.json', encoding='utf8')
    links = open('links.txt', encoding='utf8')
    arr_links = links.readlines()
    links_acortados = open('links-acortados.txt', encoding='utf8')
    arr_links_acortados = links_acortados.readlines()
    txt = "".join(peliculas_a_z.readlines())
    for i in range(len(arr_links)):
        txt = txt.replace(arr_links[i].strip(),
                          arr_links_acortados[i].strip(), 1)
    g = open("peliculas-acortadas.json", "w", encoding='utf-8')
    g.write(txt)
    g.close()
    peliculas_a_z.close()
    links.close()
    links_acortados.close()

# intercambiarLinks()


def crearRandom(texto_peliculas_json):
    random = open('#random.html', encoding='utf8')
    txt_random = "".join(random.readlines())
    txt_random = txt_random.replace("#json_peliculas",texto_peliculas_json)
    random_out = open('random.html', "w", encoding="utf-8")
    random_out.write(txt_random)
    random_out.close()
    random.close()


def crearPelicula(e, peliculas_json, txt_encabezadoPelicula):
    _pelicula = open('#pelicula.html', encoding='utf8')
    texto_out_pelicula = "".join(_pelicula.readlines())
    _pelicula.close()

    texto_out_pelicula = texto_out_pelicula.replace("#title", e["nombre"])
    texto_out_pelicula = texto_out_pelicula.replace("#nombre", e["nombre"])
    texto_out_pelicula = texto_out_pelicula.replace(
        "#descargaTorrent",
        e.get("descargaTorrent") if e.get("descargaTorrent") else ""
    )
    texto_out_pelicula = texto_out_pelicula.replace(
        "#dTorrent", "" if e.get("descargaTorrent") else "display:none;"
    )
    texto_out_pelicula = texto_out_pelicula.replace(
        "#encabezado_pelicula", txt_encabezadoPelicula)
    texto_out_pelicula = texto_out_pelicula.replace("#img", e["img"])
    texto_out_pelicula = texto_out_pelicula.replace(
        "#descargaMega",
        e.get("descargaMega") if e.get("descargaMega") else ""
    )
    texto_out_pelicula = texto_out_pelicula.replace(
        "#dMega", "" if e.get("descargaMega") else "display:none;"
    )
    texto_out_pelicula = texto_out_pelicula.replace(
        "#descripción", e["descripción"]
    )

    _recomendacion = "<div style=text-align:center;''>"

    for r in range(28):
        e2 = random.choice(peliculas_json)
        lbl = e2["nombre"].replace("(", "").replace(")", "").replace("-", "").replace("!", "").replace("?", "").replace(
            ".", " ").replace("¡", "").replace("¿", "").replace("#", "").replace("$", "").replace(":", "").replace("|", "").replace(" ", "")
        _recomendacion += f'''
            <div class="contenedor">
                <a href="{lbl}.html">
                <img src="{e2["img"]}">
                </a>
                <br>
                <span style="height:140px">{e2["nombre"]}</span>
                {f'<a  class="btn btn-light" href="{e2.get("descargaMega")}">Descargar <img src="https://i.ibb.co/SQs7sRx/Mega-logo.png" style="width: 25px;"></a>' if e2.get("descargaMega") else ""}
            </div>
            '''

    _recomendacion += "</div>"
    texto_out_pelicula = texto_out_pelicula.replace(
        "#recomendaciones",
        _recomendacion
    )
    lbl = e["nombre"].replace("(", "").replace(")", "").replace("-", "").replace("!", "").replace("?", "").replace(".", " ").replace(
        "¡", "").replace("¿", "").replace("#", "").replace("$", "").replace(":", "").replace("|", "").replace(" ", "").replace("/", "")
    pelicula_out = open(f'pelicula\\{lbl}.html', "w", encoding="utf-8")
    pelicula_out.write(texto_out_pelicula)
    pelicula_out.close()


def crearIndex():
    index = open('#index.html', encoding='utf8')
    encabezado = open('#encabezado.html', encoding='utf8')
    texto_index = "".join(index.readlines())
    texto_encabezado = "".join(encabezado.readlines())

    texto_index = texto_index.replace("#encabezado", texto_encabezado)
    file_json = open('peliculas-acortadas.json', encoding='utf8')

    texto_peliculas_json = "".join(file_json.readlines())
    peliculas_json = json.loads(texto_peliculas_json)

    peliculas_json_random = json.loads(texto_peliculas_json)
    for e in peliculas_json_random:
        del e["img"]
        del e["descripción"]
        if e.get("generos"):
            del e["generos"]
        if e.get("descargaTorrent"):
            del e["descargaTorrent"]
        if e.get("descargaMega"):
            del e["descargaMega"]
    crearRandom(json.dumps(peliculas_json_random,ensure_ascii=False))

    _contenido = "<div class='peliculas' id='peliculas'>"
    encabezado_pelicula = open('#encabezado_pelicula.html', encoding='utf8')
    txt_encabezadoPelicula = "".join(encabezado_pelicula.readlines())
    encabezado_pelicula.close()
    for e in peliculas_json:
        lbl = e["nombre"].replace("(", "").replace(")", "").replace("-", "").replace("!", "").replace("?", "").replace(".", " ").replace(
            "¡", "").replace("¿", "").replace("#", "").replace("$", "").replace(":", "").replace("|", "").replace(" ", "").replace("/", "")

        crearPelicula(e, peliculas_json, txt_encabezadoPelicula)

        _contenido += f'''
        <div class="contenedor" id="{lbl}">
            <a href="pelicula/{lbl}.html">
            <img src="{e["img"]}">
            </a>
            <br>
            <span style="height:140px">{e["nombre"]}</span>
            { f'<a  class="btn btn-light" href="{e.get("descargaMega")}">Descargar <img src="https://i.ibb.co/SQs7sRx/Mega-logo.png" style="width: 25px;"></a>' if e.get("descargaMega") else ""}
        </div>
        '''
    _contenido += "</div>"
    texto_index = texto_index.replace("#contenido", _contenido)

    index_out = open('index.html', "w", encoding="utf-8")
    index_out.write(texto_index)
    file_json.close()
    index_out.close()
    index.close()
    encabezado.close()


crearIndex()
