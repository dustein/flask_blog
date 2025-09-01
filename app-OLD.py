# # 
# # GERADOR DAS PAGINA ESTATICAS ATENCAO TEM QUE MUDAR O NOME DO ARQUIVO
# # 
# # 
# import os
# import markdown
# from flask import Flask, url_for, render_template, request
# # import re
# from bs4 import BeautifulSoup

# app = Flask(__name__)

# @app.route("/", methods=["POST", "GET"])
# def nova_pagina():
#     if request.method == "POST":
#         texto_input = request.form.get("arquivo-texto")
#         print(texto_input)

#     else:
#         texto_input = "19-Cotidiano Policial.html"
#         with open(texto_input, "r", encoding="utf-8") as file:

#             # titulo, data, conteudo, comentarios = extrai_info_markdown(texto_input)
#             titulo, data, conteudo, comentarios = extrai_info_html(texto_input)

            
#             # Agora você pode passar essas variáveis separadamente para o render_template:
#             return render_template(
#                 "index.html",
#                 titulo=titulo,
#                 data=data,
#                 conteudo=conteudo,
#                 comentarios=comentarios
#             )


#             # MEU CODIGO ANTERIOR DAQUI PRA BAIXO
#             # conteudo = markdown.markdown(file.read())
#             # site_estatico = render_template("index.html", conteudo=conteudo)
#             # converte_estatico(site_estatico, "inicio-projeto-blog.html")
#             # return render_template("index.html", conteudo=conteudo)



# # FUNCAO PARA EXTRAIR O HTML ESTATICO
# def converte_estatico(renderizado, nova_pagina):
#     output_dir = 'estaticos'
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     file_path = os.path.join(output_dir, nova_pagina)
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(renderizado)



# def extrai_info_markdown(path_arquivo):
#     with open(path_arquivo, "r", encoding="utf-8") as f:
#         md = f.read()

#     # Extrair o título (primeira linha começando com #)
#     match_titulo = re.search(r'^# (.+)', md, re.MULTILINE)
#     titulo = match_titulo.group(1).strip() if match_titulo else ""

#     # Extrair a data (linha com '*Publicado em:* ...')
#     match_data = re.search(r'\*Publicado em:\* (.+)', md)
#     data_publicacao = match_data.group(1).strip() if match_data else ""

#     # Separar conteúdo (entre o título, data e "## Comentários")
#     match_conteudo = re.search(r'\*Publicado em:\* .+\n+([\s\S]+?)\n+## Comentários', md)
#     conteudo = match_conteudo.group(1).strip() if match_conteudo else ""

#     # Extrair comentários (após ## Comentários)
#     comentarios = []
#     match_comentarios = re.split(r'## Comentários\s*\n', md)
#     if len(match_comentarios) > 1:
#         blocos = re.split(r'^### ', match_comentarios[1], flags=re.MULTILINE)
#         for bloco in blocos:
#             if bloco.strip():
#                 match = re.match(r'(.+?) em ([\d\-:\s]+)\n\n([\s\S]+)', bloco)
#                 if match:
#                     autor = match.group(1).strip()
#                     data_comentario = match.group(2).strip()
#                     conteudo_comentario = match.group(3).strip()
#                     comentarios.append({
#                         "autor": autor,
#                         "data": data_comentario,
#                         "conteudo": conteudo_comentario
#                     })

#     return titulo, data_publicacao, conteudo, comentarios

# def extrai_info_html(path_arquivo):
#     with open(path_arquivo, "r", encoding="utf-8") as f:
#         html = f.read()

#     soup = BeautifulSoup(html, 'html.parser')

#     # Extrair título - assumindo dentro da primeira tag <h1>
#     titulo_tag = soup.find('h1')
#     titulo = titulo_tag.get_text(strip=True) if titulo_tag else ''

#     # Extrair data - assumindo está dentro de um <p> com texto "*Publicado em:*"
#     data = ''
#     for p in soup.find_all('p'):
#         if p.text.startswith('Publicado em:') or p.text.startswith('*Publicado em:*'):
#             data = p.get_text(strip=True).replace('*Publicado em:*', '').replace('Publicado em:', '').strip()
#             break

#     # Extrair conteúdo - tudo depois do bloco do título e data até a seção comentários
#     # Supondo que comentários começam com <h2>Comentários</h2>
#     conteudo = ''
#     comentarios = []

#     # Encontrar a tag <h2> com texto Comentários
#     comentarios_h2 = soup.find('h2', string=lambda s: 'Comentários' in s if s else False)

#     # Conteúdo será tudo entre data e Comentários
#     if comentarios_h2:
#         tags_entre = []
#         # Percorrer os irmãos anteriores de comentarios_h2 para pegar conteúdo entre data e comentários
#         for el in comentarios_h2.find_all_previous():
#             # Ignorando títulos e data
#             if el == titulo_tag:
#                 break
#             tags_entre.append(el)
#         tags_entre.reverse()
#         conteudo = ''.join(str(tag) for tag in tags_entre).strip()
#     else:
#         # Se não encontrar comentários, pegar tudo após data
#         conteudo = ''
#         after_data = False
#         container = soup.body if soup.body else soup
#         for tag in container.children:
#             if after_data:
#                 conteudo += str(tag)
#             elif data and data in tag.text:
#                 after_data = True

#     # Extrair comentários - supondo estrutura: <h3>Autor em Data</h3> seguido de <p>Conteúdo</p>
#     if comentarios_h2:
#         # Ir pegando os elementos irmãos logo após <h2>Comentarios
#         current = comentarios_h2.find_next_sibling()
#         while current:
#             if current.name == 'h3':
#                 # Extrair autor e data da string h3
#                 texto = current.get_text(strip=True)
#                 parts = texto.split(' em ')
#                 autor = parts[0] if len(parts) > 0 else ''
#                 data_comentario = parts[1] if len(parts) > 1 else ''
#                 # Conteúdo esperado no próximo <p>
#                 p = current.find_next_sibling()
#                 conteudo_comentario = p.get_text(strip=True) if p and p.name == 'p' else ''
#                 comentarios.append({
#                     'autor': autor,
#                     'data': data_comentario,
#                     'conteudo': conteudo_comentario
#                 })
#                 current = p.find_next_sibling() if p else None
#             else:
#                 current = current.find_next_sibling()

#     return titulo, data, conteudo, comentarios

# app.run(debug=True)


# 
# GERADOR DAS PAGINA ESTATICAS ATENCAO TEM QUE MUDAR O NOME DO ARQUIVO
# 
# 
import os
from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def nova_pagina():
    if request.method == "POST":
        texto_input = request.form.get("arquivo-texto")
        print(texto_input)

    else:
        texto_input = "nome_do_arquivo.html"
        with open(texto_input, "r", encoding="utf-8") as file:

            return render_template("nome_do arquivo_ID.html", conteudo=file)




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

def extrai_info_html(path_arquivo):
    with open(path_arquivo, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Extrair título - assumindo dentro da primeira tag <h1>
    titulo_tag = soup.find('h1')
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else ''

    # Extrair data - assumindo está dentro de um <p> com texto "*Publicado em:*"
    data = ''
    for p in soup.find_all('p'):
        if p.text.startswith('Publicado em:') or p.text.startswith('*Publicado em:*'):
            data = p.get_text(strip=True).replace('*Publicado em:*', '').replace('Publicado em:', '').strip()
            break

    # Extrair conteúdo - tudo depois do bloco do título e data até a seção comentários
    # Supondo que comentários começam com <h2>Comentários</h2>
    conteudo = ''
    comentarios = []

    # Encontrar a tag <h2> com texto Comentários
    comentarios_h2 = soup.find('h2', string=lambda s: 'Comentários' in s if s else False)

    # Conteúdo será tudo entre data e Comentários
    if comentarios_h2:
        tags_entre = []
        # Percorrer os irmãos anteriores de comentarios_h2 para pegar conteúdo entre data e comentários
        for el in comentarios_h2.find_all_previous():
            # Ignorando títulos e data
            if el == titulo_tag:
                break
            tags_entre.append(el)
        tags_entre.reverse()
        conteudo = ''.join(str(tag) for tag in tags_entre).strip()
    else:
        # Se não encontrar comentários, pegar tudo após data
        conteudo = ''
        after_data = False
        container = soup.body if soup.body else soup
        for tag in container.children:
            if after_data:
                conteudo += str(tag)
            elif data and data in tag.text:
                after_data = True

    # Extrair comentários - supondo estrutura: <h3>Autor em Data</h3> seguido de <p>Conteúdo</p>
    if comentarios_h2:
        # Ir pegando os elementos irmãos logo após <h2>Comentarios
        current = comentarios_h2.find_next_sibling()
        while current:
            if current.name == 'h3':
                # Extrair autor e data da string h3
                texto = current.get_text(strip=True)
                parts = texto.split(' em ')
                autor = parts[0] if len(parts) > 0 else ''
                data_comentario = parts[1] if len(parts) > 1 else ''
                # Conteúdo esperado no próximo <p>
                p = current.find_next_sibling()
                conteudo_comentario = p.get_text(strip=True) if p and p.name == 'p' else ''
                comentarios.append({
                    'autor': autor,
                    'data': data_comentario,
                    'conteudo': conteudo_comentario
                })
                current = p.find_next_sibling() if p else None
            else:
                current = current.find_next_sibling()

    return titulo, data, conteudo, comentarios

app.run(debug=True)