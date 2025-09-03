# import re
# import os
# import json
# from flask import Flask, url_for, render_template, request
# from datetime import datetime


# app = Flask(__name__)


# def formatar_data(data_string):
#     """Converte string ISO para formato brasileiro"""
#     try:
#         data = datetime.fromisoformat(data_string.replace('Z', '+00:00'))
#         return data.strftime('%d/%m/%Y')
#     except:
#         return data_string


# def formatar_conteudo(conteudo):
#     """Formata o conteúdo em parágrafos e ajusta URLs das imagens"""
    
#     # PRIMEIRO: Substituir TODAS as ocorrências de http: por https:
#     conteudo = re.sub(r'http:', 'https:', conteudo)
    
#     # Ajustar URLs das imagens para caminhos relativos
#     conteudo = re.sub(
#         r'src="https://www\.casodepolicia\.com/wp-content/uploads/',
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


# def limpar_nome_arquivo(nome):
#     """Converte título para um nome de arquivo válido com hífens"""
#     import re
#     # Remove caracteres especiais e substitui espaços por hífens
#     nome_limpo = re.sub(r'[^\w\s-]', '', nome)  # Remove caracteres especiais
#     nome_limpo = re.sub(r'\s+', '-', nome_limpo)  # Substitui espaços por hífens
#     nome_limpo = re.sub(r'-+', '-', nome_limpo)  # Remove hífens duplicados
#     nome_limpo = nome_limpo.strip('-')  # Remove hífens do início/fim
#     return nome_limpo.lower()  # Converte para minúsculas


# @app.route("/", methods=["POST", "GET"])
# def nova_pagina():
#     pasta_dados = "dados"
    
#     # Listar todos os arquivos JSON na pasta dados
#     arquivos_json = [f for f in os.listdir(pasta_dados) if f.endswith('.json')]
    
#     print(f"📊 Encontrados {len(arquivos_json)} arquivos para processar...")
    
#     # Percorrer todos os arquivos
#     for arquivo_nome in arquivos_json:
#         file_path = os.path.join(pasta_dados, arquivo_nome)
        
#         print(f"🔄 Processando: {arquivo_nome}")
        
#         try:
#             # Carregar dados JSON
#             with open(file_path, "r", encoding="utf-8") as file:
#                 dados_post = json.load(file)
            
#             # Formatar dados para o template
#             dados_formatados = {
#                 'id': dados_post['id'],
#                 'titulo': dados_post['titulo'],
#                 'data_formatada': formatar_data(dados_post['data']),
#                 'conteudo_formatado': formatar_conteudo(dados_post['conteudo']),
#                 'autor_id': dados_post['autor_id'],
#                 'comentarios': [
#                     {
#                         'autor': comentario['autor'],
#                         'data_formatada': formatar_data(comentario['data']),
#                         'conteudo': comentario['conteudo']
#                     }
#                     for comentario in dados_post.get('comentarios', [])
#                 ],
#                 'total_comentarios': len(dados_post.get('comentarios', []))
#             }
            
#             # Renderizar template
#             html_renderizado = render_template("index.html", post=dados_formatados)
            
#             # Criar arquivo estático com nome limpo
#             titulo_limpo = limpar_nome_arquivo(dados_post['titulo'])
#             nome_arquivo_html = f"{titulo_limpo}-post-{dados_post['id']}.html"
            
#             # Salvar arquivo HTML
#             converte_estatico(html_renderizado, nome_arquivo_html)
            
#             print(f"✅ HTML criado: {nome_arquivo_html}")
            
#         except Exception as e:
#             print(f"❌ Erro ao processar {arquivo_nome}: {e}")
    
#     print(f"\n🎉 Processamento concluído!")
    
#     # Retornar mensagem de sucesso
#     return f"<h1>Processamento Concluído!</h1><p>{len(arquivos_json)} arquivos processados. Verifique a pasta 'estaticos'.</p>"


# def converte_estatico(renderizado, nova_pagina):
#     output_dir = 'estaticos'
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)


#     file_path = os.path.join(output_dir, nova_pagina)
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(renderizado)


# if __name__ == "__main__":
#     app.run(debug=True)

import re
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
    
    # PRIMEIRO: Substituir TODAS as ocorrências de http: por https:
    conteudo = re.sub(r'http:', 'https:', conteudo)
    
    # Ajustar URLs das imagens para caminhos relativos
    conteudo = re.sub(
        r'src="https://www\.casodepolicia\.com/wp-content/uploads/',
        'src="uploads/',
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

def gerar_pagina_indice(posts_dados):
    """Gera uma página índice com links organizados por categoria"""
    posts_por_categoria = {}
    posts_sem_categoria = []
    
    # Organizar posts por categoria
    for dados_post in posts_dados:
        titulo = dados_post.get('titulo')
        post_id = dados_post.get('id')
        data = dados_post.get('data')
        categorias = dados_post.get('categorias', [])
        
        # Criar nome do arquivo HTML
        titulo_limpo = limpar_nome_arquivo(titulo)
        nome_arquivo_html = f"{titulo_limpo}-post-{post_id}.html"
        
        post_info = {
            'titulo': titulo,
            'id': post_id,
            'arquivo': nome_arquivo_html,
            'data': formatar_data(data) if data else ''
        }
        
        # Se o post tem categorias
        if categorias:
            for categoria in categorias:
                nome_categoria = categoria.get('nome', 'Sem Categoria')
                
                if nome_categoria not in posts_por_categoria:
                    posts_por_categoria[nome_categoria] = []
                    
                posts_por_categoria[nome_categoria].append(post_info)
        else:
            # Posts sem categoria
            posts_sem_categoria.append(post_info)
    
    # Se há posts sem categoria, adicionar à estrutura
    if posts_sem_categoria:
        posts_por_categoria['Sem Categoria'] = posts_sem_categoria
    
    # Gerar HTML do índice
    html_indice = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice de Posts por Categoria - Caso de Polícia</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #007bff;
            margin-top: 30px;
            border-left: 4px solid #007bff;
            padding-left: 15px;
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 8px 0;
            padding: 12px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #007bff;
            transition: background-color 0.3s;
        }
        li:hover {
            background-color: #e9ecef;
        }
        a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        a:hover {
            color: #007bff;
        }
        .data {
            color: #666;
            font-size: 0.9em;
            margin-left: 10px;
        }
        .total {
            background-color: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }
        .categoria-stats {
            background-color: #fff3cd;
            padding: 8px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            color: #856404;
            display: inline-block;
            margin-left: 10px;
        }
        .post-id {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Índice de Posts por Categoria</h1>
'''
    
    total_posts = sum(len(posts) for posts in posts_por_categoria.values())
    html_indice += f'<div class="total">Total de posts: {total_posts} | Categorias: {len(posts_por_categoria)}</div>'
    
    # Ordenar categorias alfabeticamente (mas colocar "Sem Categoria" por último)
    categorias_ordenadas = sorted([cat for cat in posts_por_categoria.keys() if cat != 'Sem Categoria'])
    if 'Sem Categoria' in posts_por_categoria:
        categorias_ordenadas.append('Sem Categoria')
    
    for categoria in categorias_ordenadas:
        posts = posts_por_categoria[categoria]
        
        # Emoji específico para categoria
        emoji = "📂" if categoria != "Sem Categoria" else "📄"
        
        html_indice += f'<h2>{emoji} {categoria}<span class="categoria-stats">{len(posts)} posts</span></h2>'
        html_indice += '<ul>'
        
        # Ordenar posts por ID (mais recente primeiro)
        posts_ordenados = sorted(posts, key=lambda x: x['id'], reverse=True)
        
        for post in posts_ordenados:
            html_indice += f'''
            <li>
                <a href="{post['arquivo']}">{post['titulo']}</a>
                <span class="post-id">ID: {post['id']}</span>
                <span class="data">{post['data']}</span>
            </li>'''
            
        html_indice += '</ul>'
    
    html_indice += '''
    </div>
</body>
</html>'''
    
    return html_indice

@app.route("/", methods=["POST", "GET"])
def nova_pagina():
    pasta_dados = "dados"
    
    # Listar todos os arquivos JSON na pasta dados
    arquivos_json = [f for f in os.listdir(pasta_dados) if f.endswith('.json')]
    
    print(f"📊 Encontrados {len(arquivos_json)} arquivos para processar...")
    
    # Lista para armazenar dados de todos os posts
    todos_posts = []
    
    # Percorrer todos os arquivos
    for arquivo_nome in arquivos_json:
        file_path = os.path.join(pasta_dados, arquivo_nome)
        
        print(f"🔄 Processando: {arquivo_nome}")
        
        try:
            # Carregar dados JSON
            with open(file_path, "r", encoding="utf-8") as file:
                dados_post = json.load(file)
            
            # Adicionar à lista de todos os posts para o índice
            todos_posts.append(dados_post)
            
            # Formatar dados para o template
            dados_formatados = {
                'id': dados_post['id'],
                'titulo': dados_post['titulo'],
                'data_formatada': formatar_data(dados_post['data']),
                'conteudo_formatado': formatar_conteudo(dados_post['conteudo']),
                'autor_id': dados_post['autor_id'],
                'categorias': dados_post.get('categorias', []),  # Adicionar categorias aos dados formatados
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
            nome_arquivo_html = f"{titulo_limpo}-post-{dados_post['id']}.html"
            
            # Salvar arquivo HTML
            converte_estatico(html_renderizado, nome_arquivo_html)
            
            print(f"✅ HTML criado: {nome_arquivo_html}")
            
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo_nome}: {e}")
    
    # Gerar página índice organizada por categorias
    print(f"📋 Gerando página índice por categorias...")
    html_indice = gerar_pagina_indice(todos_posts)
    converte_estatico(html_indice, "indice.html")
    print(f"✅ Página índice criada: indice.html")
    
    print(f"\n🎉 Processamento concluído!")
    
    # Retornar mensagem de sucesso
    return f"""<h1>Processamento Concluído!</h1>
    <p>{len(arquivos_json)} arquivos processados.</p>
    <p>✅ Arquivos criados na pasta 'estaticos'</p>
    <p>📋 <strong>Página índice:</strong> <a href="estaticos/indice.html">indice.html</a></p>
    <p>🏷️ Posts organizados por categoria</p>
    <p>Verifique a pasta 'estaticos' para todos os arquivos.</p>"""

def converte_estatico(renderizado, nova_pagina):
    output_dir = 'estaticos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, nova_pagina)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(renderizado)

if __name__ == "__main__":
    app.run(debug=True)
