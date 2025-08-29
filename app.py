# 
# GERADOR DAS PAGINA ESTATICAS ATENCAO TEM QUE MUDAR O NOME DO ARQUIVO
# 
# 
import os
import markdown
from flask import Flask, url_for, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def nova_pagina():
    if request.method == "POST":
        texto_input = request.form.get("arquivo-texto")
        print(texto_input)

    else:
        texto_input = "19-Cotidiano Policial.md"
        with open(texto_input, "r", encoding="utf-8") as file:

            titulo, data, conteudo, comentarios = extrai_info_markdown(texto_input)
            
            # Agora você pode passar essas variáveis separadamente para o render_template:
            return render_template(
                "index.html",
                titulo=titulo,
                data=data,
                conteudo=conteudo,
                comentarios=comentarios
            )


            # MEU CODIGO ANTERIOR DAQUI PRA BAIXO
            # conteudo = markdown.markdown(file.read())
            # site_estatico = render_template("index.html", conteudo=conteudo)
            # converte_estatico(site_estatico, "inicio-projeto-blog.html")
            # return render_template("index.html", conteudo=conteudo)



# FUNCAO PARA EXTRAIR O HTML ESTATICO
def converte_estatico(renderizado, nova_pagina):
    output_dir = 'estaticos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, nova_pagina)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(renderizado)



def extrai_info_markdown(path_arquivo):
    with open(path_arquivo, "r", encoding="utf-8") as f:
        md = f.read()

    # Extrair o título (primeira linha começando com #)
    match_titulo = re.search(r'^# (.+)', md, re.MULTILINE)
    titulo = match_titulo.group(1).strip() if match_titulo else ""

    # Extrair a data (linha com '*Publicado em:* ...')
    match_data = re.search(r'\*Publicado em:\* (.+)', md)
    data_publicacao = match_data.group(1).strip() if match_data else ""

    # Separar conteúdo (entre o título, data e "## Comentários")
    match_conteudo = re.search(r'\*Publicado em:\* .+\n+([\s\S]+?)\n+## Comentários', md)
    conteudo = match_conteudo.group(1).strip() if match_conteudo else ""

    # Extrair comentários (após ## Comentários)
    comentarios = []
    match_comentarios = re.split(r'## Comentários\s*\n', md)
    if len(match_comentarios) > 1:
        blocos = re.split(r'^### ', match_comentarios[1], flags=re.MULTILINE)
        for bloco in blocos:
            if bloco.strip():
                match = re.match(r'(.+?) em ([\d\-:\s]+)\n\n([\s\S]+)', bloco)
                if match:
                    autor = match.group(1).strip()
                    data_comentario = match.group(2).strip()
                    conteudo_comentario = match.group(3).strip()
                    comentarios.append({
                        "autor": autor,
                        "data": data_comentario,
                        "conteudo": conteudo_comentario
                    })

    return titulo, data_publicacao, conteudo, comentarios

app.run(debug=True)