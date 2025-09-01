# import os
# import re
# from flask import Flask, url_for, render_template, request

# app = Flask(__name__)

# @app.route("/", methods=["POST", "GET"])
# def nova_pagina():
#     if request.method == "POST":
#         texto_input = request.form.get("arquivo-texto")
#         print(texto_input)

#     else:
#         texto_input = "post_1973.html"
#         # Ajusta o path para buscar na pasta extraidos
#         file_path = os.path.join("extraidos", texto_input)
        
#         with open(file_path, "r", encoding="utf-8") as file:
#             conteudo = file.read()
            
#             # Captura o texto do título H1
#             h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', conteudo, re.IGNORECASE | re.DOTALL)
#             titulo = h1_match.group(1).strip() if h1_match else "Título não encontrado"
            
#             # Renderiza o template passando conteudo e titulo_h1
#             html_renderizado = render_template("index.html", conteudo=conteudo, titulo=titulo)
            
#             # Executa a criação do arquivo estático durante o GET
#             converte_estatico(html_renderizado, "pagina_estatica.html")
            
#             return html_renderizado

# # FUNCAO PARA EXTRAIR O HTML ESTATICO
# def converte_estatico(renderizado, nova_pagina):
#     output_dir = 'estaticos'
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     file_path = os.path.join(output_dir, nova_pagina)
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(renderizado)

# if __name__ == "__main__":
#     app.run(debug=True)

# import os
# import json
# from flask import Flask, url_for, render_template, request
# from datetime import datetime

# app = Flask(__name__)

# def formatar_data(data_string):
#     """Converte string ISO para formato brasileiro"""
#     try:
#         data = datetime.fromisoformat(data_string.replace('Z', '+00:00'))
#         # return data.strftime('%d/%m/%Y às %H:%M')
#         return data.strftime('%d/%m/%Y')
#     except:
#         return data_string

# def formatar_conteudo(conteudo):
#     """Formata o conteúdo em parágrafos"""
#     import re

#         # Ajustar URLs das imagens para caminhos relativos
#     conteudo = re.sub(
#         r'src="http://www\.casodepolicia\.com/wp-content/uploads/',
#         'src="uploads/',
#         conteudo
#     )

#     blocos = re.split(r'\n\s*\n', conteudo.strip())
    
#     conteudo_formatado = []
    
#     for bloco in blocos:
#         bloco = bloco.strip()
#         if not bloco:
#             continue
            
#         # Se contém HTML, manter como está
#         if re.match(r'^\s*<(img|iframe|div|h[1-6])', bloco, re.IGNORECASE):
#             conteudo_formatado.append(bloco)
#         else:
#             conteudo_formatado.append(f"<p>{bloco}</p>")
    
#     return '\n'.join(conteudo_formatado)

# @app.route("/", methods=["POST", "GET"])
# def nova_pagina():
#     if request.method == "POST":
#         arquivo_selecionado = request.form.get("arquivo-texto")
#         if not arquivo_selecionado.endswith('.json'):
#             arquivo_selecionado += '.json'
#     else:
#         arquivo_selecionado = "post_1973.json"
    
#     # Carregar dados JSON
#     file_path = os.path.join("dados", arquivo_selecionado)
    
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             dados_post = json.load(file)
        
#         # Formatar dados para o template
#         dados_formatados = {
#             'id': dados_post['id'],
#             'titulo': dados_post['titulo'],
#             'data_formatada': formatar_data(dados_post['data']),
#             'conteudo_formatado': formatar_conteudo(dados_post['conteudo']),
#             'autor_id': dados_post['autor_id'],
#             'comentarios': [
#                 {
#                     'autor': comentario['autor'],
#                     'data_formatada': formatar_data(comentario['data']),
#                     'conteudo': comentario['conteudo']
#                 }
#                 for comentario in dados_post.get('comentarios', [])
#             ],
#             'total_comentarios': len(dados_post.get('comentarios', []))
#         }
        
#         # Renderizar template
#         html_renderizado = render_template("index.html", post=dados_formatados)
        
#         # Criar arquivo estático
#         # converte_estatico(html_renderizado, f"post_{dados_post['id']}_estatico.html")
#         converte_estatico(html_renderizado, f"{dados_post['titulo']}_estatico.html")
        

        
#         return html_renderizado
        
#     except FileNotFoundError:
#         return render_template("erro.html", mensagem=f"Arquivo {arquivo_selecionado} não encontrado")
#     except json.JSONDecodeError:
#         return render_template("erro.html", mensagem="Erro ao ler arquivo JSON")

# def converte_estatico(renderizado, nova_pagina):
#     output_dir = 'estaticos'
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     file_path = os.path.join(output_dir, nova_pagina)
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(renderizado)

# if __name__ == "__main__":
#     app.run(debug=True)

import os
import json
from flask import Flask, url_for, render_template, request
from datetime import datetime

app = Flask(__name__)

def formatar_data(data_string):
    """Converte string ISO para formato brasileiro"""
    try:
        data = datetime.fromisoformat(data_string.replace('Z', '+00:00'))
        return data.strftime('%d/%m/%Y')
    except:
        return data_string

def formatar_conteudo(conteudo):
    """Formata o conteúdo em parágrafos e ajusta URLs das imagens"""
    import re
    
    # Ajustar URLs das imagens para caminhos relativos
    conteudo = re.sub(
        r'src="http://www\.casodepolicia\.com/wp-content/uploads/',
        'src="/uploads/',
        conteudo
    )
    
    blocos = re.split(r'\n\s*\n', conteudo.strip())
    
    conteudo_formatado = []
    
    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco:
            continue
            
        # Se contém HTML, manter como está
        if re.match(r'^\s*<(img|iframe|div|h[1-6])', bloco, re.IGNORECASE):
            conteudo_formatado.append(bloco)
        else:
            conteudo_formatado.append(f"<p>{bloco}</p>")
    
    return '\n'.join(conteudo_formatado)

def limpar_nome_arquivo(nome):
    """Converte título para um nome de arquivo válido com hífens"""
    import re
    # Remove caracteres especiais e substitui espaços por hífens
    nome_limpo = re.sub(r'[^\w\s-]', '', nome)  # Remove caracteres especiais
    nome_limpo = re.sub(r'\s+', '-', nome_limpo)  # Substitui espaços por hífens
    nome_limpo = re.sub(r'-+', '-', nome_limpo)  # Remove hífens duplicados
    nome_limpo = nome_limpo.strip('-')  # Remove hífens do início/fim
    return nome_limpo.lower()  # Converte para minúsculas

@app.route("/", methods=["POST", "GET"])
def nova_pagina():
    if request.method == "POST":
        arquivo_selecionado = request.form.get("arquivo-texto")
        if not arquivo_selecionado.endswith('.json'):
            arquivo_selecionado += '.json'
    else:
        arquivo_selecionado = "post_1973.json"
    
    # Carregar dados JSON
    file_path = os.path.join("dados", arquivo_selecionado)
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            dados_post = json.load(file)
        
        # Formatar dados para o template
        dados_formatados = {
            'id': dados_post['id'],
            'titulo': dados_post['titulo'],
            'data_formatada': formatar_data(dados_post['data']),
            'conteudo_formatado': formatar_conteudo(dados_post['conteudo']),
            'autor_id': dados_post['autor_id'],
            'comentarios': [
                {
                    'autor': comentario['autor'],
                    'data_formatada': formatar_data(comentario['data']),
                    'conteudo': comentario['conteudo']
                }
                for comentario in dados_post.get('comentarios', [])
            ],
            'total_comentarios': len(dados_post.get('comentarios', []))
        }
        
        # Renderizar template
        html_renderizado = render_template("index.html", post=dados_formatados)
        
        # Criar arquivo estático com nome limpo
        titulo_limpo = limpar_nome_arquivo(dados_post['titulo'])
        converte_estatico(html_renderizado, f"{titulo_limpo}-post-{dados_post['id']}.html")
        
        return html_renderizado
        
    except FileNotFoundError:
        return render_template("erro.html", mensagem=f"Arquivo {arquivo_selecionado} não encontrado")
    except json.JSONDecodeError:
        return render_template("erro.html", mensagem="Erro ao ler arquivo JSON")

def converte_estatico(renderizado, nova_pagina):
    output_dir = 'estaticos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, nova_pagina)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(renderizado)

if __name__ == "__main__":
    app.run(debug=True)
