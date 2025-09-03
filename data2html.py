# # # import os
# # # import mysql.connector
# # # import re

# # # def acessar_wordpress_mysql(host, usuario, senha, banco, limite=None):
# # #     conn = mysql.connector.connect(
# # #         host=host,
# # #         user=usuario,
# # #         password=senha,
# # #         database=banco
# # #     )
# # #     cursor = conn.cursor()
    
# # #     query = """
# # #     SELECT ID, post_title, post_content, post_date, post_author
# # #     FROM wp_posts 
# # #     WHERE post_type = 'post' 
# # #     AND post_status = 'publish'
# # #     ORDER BY post_date DESC
# # #     """
    
# # #     if limite:
# # #         query += f" LIMIT {limite}"
    
# # #     cursor.execute(query)
# # #     posts = cursor.fetchall()
    
# # #     cursor.close()
# # #     conn.close()
    
# # #     return posts

# # # def formatar_conteudo_com_paragrafos(conteudo):
# # #     """
# # #     Formata o conteúdo dividindo em parágrafos separados por linhas em branco,
# # #     mas preservando imagens e outros elementos HTML
# # #     """
# # #     # Dividir por quebras de linha duplas ou mais
# # #     blocos = re.split(r'\n\s*\n', conteudo.strip())
    
# # #     conteudo_formatado = ""
    
# # #     for bloco in blocos:
# # #         bloco = bloco.strip()
# # #         if not bloco:
# # #             continue
            
# # #         # Se o bloco contém apenas uma tag HTML (como img), não envolver em <p>
# # #         if re.match(r'^\s*<(img|iframe|div|h[1-6])', bloco, re.IGNORECASE):
# # #             conteudo_formatado += f"    {bloco}\n\n"
# # #         else:
# # #             # Envolver em <p> e adicionar indentação
# # #             conteudo_formatado += f"    <p>{bloco}</p>\n\n"
    
# # #     return conteudo_formatado.rstrip()

# # # def salvar_posts_html(posts, pasta_destino='./extraidos'):
# # #     # Criar a pasta se não existir
# # #     if not os.path.exists(pasta_destino):
# # #         os.makedirs(pasta_destino)
# # #         print(f"Pasta '{pasta_destino}' criada.")
    
# # #     arquivos_salvos = []
    
# # #     for post in posts:
# # #         id_post = post[0]
# # #         titulo = post[1]
# # #         conteudo_raw = post[2]
# # #         data = post[3]
# # #         autor = post[4]
        
# # #         # Formatar conteúdo com parágrafos separados
# # #         conteudo_formatado = formatar_conteudo_com_paragrafos(conteudo_raw)
        
# # #         # Nome do arquivo usando ID do post
# # #         nome_arquivo = f"post_{id_post}.html"
# # #         caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
# # #         # Conteúdo HTML apenas do body
# # #         html_content = f"""<h1>{titulo}</h1>
# # # <div class="meta">
# # #     <strong>ID do Post:</strong> {id_post} | 
# # #     <strong>Data:</strong> {data} | 
# # #     <strong>Autor ID:</strong> {autor}
# # # </div>
# # # <div class="content">
# # # {conteudo_formatado}
# # # </div>"""
        
# # #         # Salvar o arquivo HTML
# # #         try:
# # #             with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
# # #                 arquivo.write(html_content)
# # #             arquivos_salvos.append(nome_arquivo)
# # #             print(f"✓ Salvo: {nome_arquivo}")
# # #         except Exception as e:
# # #             print(f"✗ Erro ao salvar {nome_arquivo}: {e}")
    
# # #     return arquivos_salvos

# # # # Exemplo de uso
# # # if __name__ == "__main__":
# # #     try:
# # #         # Extrair posts do WordPress
# # #         posts = acessar_wordpress_mysql(
# # #             host='localhost',
# # #             usuario='root',
# # #             senha='casodepolicia',
# # #             banco='local_casodepolicia',
# # #             limite=20
# # #         )
        
# # #         print(f"Encontrados {len(posts)} posts no banco de dados.")
        
# # #         # Salvar posts em arquivos HTML
# # #         arquivos = salvar_posts_html(posts, './extraidos')
        
# # #         print(f"\n{len(arquivos)} arquivos HTML criados na pasta './extraidos':")
# # #         for arquivo in arquivos:
# # #             print(f"  - {arquivo}")
            
# # #     except mysql.connector.Error as e:
# # #         print(f"Erro MySQL: {e}")
# # #     except Exception as e:
# # #         print(f"Erro geral: {e}")

# # import os
# # import mysql.connector
# # import re


# # def acessar_wordpress_mysql(host, usuario, senha, banco, limite=None):
# #     conn = mysql.connector.connect(
# #         host=host,
# #         user=usuario,
# #         password=senha,
# #         database=banco
# #     )
# #     cursor = conn.cursor()
    
# #     query = """
# #     SELECT ID, post_title, post_content, post_date, post_author
# #     FROM wp_posts 
# #     WHERE post_type = 'post' 
# #     AND post_status = 'publish'
# #     ORDER BY post_date DESC
# #     """
    
# #     if limite:
# #         query += f" LIMIT {limite}"
    
# #     cursor.execute(query)
# #     posts = cursor.fetchall()
    
# #     cursor.close()
# #     conn.close()
    
# #     return posts


# # def buscar_comentarios_post(host, usuario, senha, banco, post_id):
# #     conn = mysql.connector.connect(
# #         host=host,
# #         user=usuario,
# #         password=senha,
# #         database=banco
# #     )
# #     cursor = conn.cursor()
    
# #     query = """
# #     SELECT comment_author, comment_date, comment_content
# #     FROM wp_comments
# #     WHERE comment_post_ID = %s
# #     AND comment_approved = '1'
# #     ORDER BY comment_date ASC
# #     """
    
# #     cursor.execute(query, (post_id,))
# #     comentarios = cursor.fetchall()
    
# #     cursor.close()
# #     conn.close()
    
# #     return comentarios


# # def formatar_conteudo_com_paragrafos(conteudo):
# #     """
# #     Formata o conteúdo dividindo em parágrafos separados por linhas em branco,
# #     mas preservando imagens e outros elementos HTML
# #     """
# #     # Dividir por quebras de linha duplas ou mais
# #     blocos = re.split(r'\n\s*\n', conteudo.strip())
    
# #     conteudo_formatado = ""
    
# #     for bloco in blocos:
# #         bloco = bloco.strip()
# #         if not bloco:
# #             continue
            
# #         # Se o bloco contém apenas uma tag HTML (como img), não envolver em <p>
# #         if re.match(r'^\s*<(img|iframe|div|h[1-6])', bloco, re.IGNORECASE):
# #             conteudo_formatado += f"    {bloco}\n\n"
# #         else:
# #             # Envolver em <p> e adicionar indentação
# #             conteudo_formatado += f"    <p>{bloco}</p>\n\n"
    
# #     return conteudo_formatado.rstrip()


# # def salvar_posts_html(posts, host, usuario, senha, banco, pasta_destino='./extraidos'):
# #     # Criar a pasta se não existir
# #     if not os.path.exists(pasta_destino):
# #         os.makedirs(pasta_destino)
# #         print(f"Pasta '{pasta_destino}' criada.")
    
# #     arquivos_salvos = []
    
# #     for post in posts:
# #         id_post = post[0]
# #         titulo = post[1]
# #         conteudo_raw = post[2]
# #         data = post[3]
# #         autor = post[4]
        
# #         # Formatar conteúdo com parágrafos separados
# #         conteudo_formatado = formatar_conteudo_com_paragrafos(conteudo_raw)
        
# #         # Buscar comentários do post
# #         comentarios = buscar_comentarios_post(host, usuario, senha, banco, id_post)
        
# #         # Adicionar comentários ao HTML se existirem
# #         comentarios_html = ''
# #         if comentarios:
# #             comentarios_html += '\n<h3 class="comentarios">Comentários</h3>\n'
# #             for autor_coment, data_coment, texto_coment in comentarios:
# #                 comentarios_html += f'<p class="comentarios_autor">{autor_coment}</p>\n'
# #                 comentarios_html += f'<p class="comentarios_data">{data_coment}</p>\n'
# #                 comentarios_html += f'<p class="comentarios_texto">{texto_coment}</p>\n\n'
        
# #         # Nome do arquivo usando ID do post
# #         nome_arquivo = f"post_{id_post}.html"
# #         caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
# #         # Conteúdo HTML apenas do body
# #         html_content = f""" <h1 class="titulo">{titulo}</h1>
# #                             <p class="data-post">{data}</p>
# #                             <div class="content">{conteudo_formatado}{comentarios_html}</div>"""
        
# #         # Salvar o arquivo HTML
# #         try:
# #             with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
# #                 arquivo.write(html_content)
# #             arquivos_salvos.append(nome_arquivo)
# #             print(f"✓ Salvo: {nome_arquivo}")
# #         except Exception as e:
# #             print(f"✗ Erro ao salvar {nome_arquivo}: {e}")
    
# #     return arquivos_salvos


# # # Exemplo de uso
# # if __name__ == "__main__":
# #     try:
# #         # Extrair posts do WordPress
# #         posts = acessar_wordpress_mysql(
# #             host='localhost',
# #             usuario='root',
# #             senha='casodepolicia',
# #             banco='local_casodepolicia',
# #             limite=20
# #         )
        
# #         print(f"Encontrados {len(posts)} posts no banco de dados.")
        
# #         # Salvar posts em arquivos HTML com comentários
# #         arquivos = salvar_posts_html(
# #             posts,
# #             host='localhost',
# #             usuario='root',
# #             senha='casodepolicia',
# #             banco='local_casodepolicia',
# #             pasta_destino='./extraidos'
# #         )
        
# #         print(f"\n{len(arquivos)} arquivos HTML criados na pasta './extraidos':")
# #         for arquivo in arquivos:
# #             print(f"  - {arquivo}")
            
# #     except mysql.connector.Error as e:
# #         print(f"Erro MySQL: {e}")
# #     except Exception as e:
# #         print(f"Erro geral: {e}")

# import os
# import mysql.connector
# import json
# from datetime import datetime

# def acessar_wordpress_mysql(host, usuario, senha, banco, limite=None):
#     conn = mysql.connector.connect(
#         host=host,
#         user=usuario,
#         password=senha,
#         database=banco
#     )
#     cursor = conn.cursor()
    
#     query = """
#     SELECT ID, post_title, post_content, post_date, post_author
#     FROM wp_posts 
#     WHERE post_type = 'post' 
#     AND post_status = 'publish'
#     ORDER BY post_date DESC
#     """
    
#     if limite:
#         query += f" LIMIT {limite}"
    
#     cursor.execute(query)
#     posts = cursor.fetchall()
    
#     cursor.close()
#     conn.close()
    
#     return posts

# def buscar_comentarios_post(host, usuario, senha, banco, post_id):
#     conn = mysql.connector.connect(
#         host=host,
#         user=usuario,
#         password=senha,
#         database=banco
#     )
#     cursor = conn.cursor()
    
#     query = """
#     SELECT comment_author, comment_date, comment_content
#     FROM wp_comments
#     WHERE comment_post_ID = %s
#     AND comment_approved = '1'
#     ORDER BY comment_date ASC
#     """
    
#     cursor.execute(query, (post_id,))
#     comentarios = cursor.fetchall()
    
#     cursor.close()
#     conn.close()
    
#     return comentarios

# def salvar_posts_json(posts, host, usuario, senha, banco, pasta_destino='./dados'):
#     """
#     Esta função cria a pasta 'dados' e salva os JSONs lá
#     """
#     # Criar a pasta 'dados' se não existir
#     if not os.path.exists(pasta_destino):
#         os.makedirs(pasta_destino)
#         print(f"📁 Pasta '{pasta_destino}' criada.")
    
#     arquivos_salvos = []
    
#     for post in posts:
#         id_post = post[0]
#         titulo = post[1] 
#         conteudo_raw = post[2]
#         data = post[3]
#         autor = post[4]
        
#         # Buscar comentários do post
#         comentarios = buscar_comentarios_post(host, usuario, senha, banco, id_post)
        
#         # Estruturar dados em formato JSON
#         dados_post = {
#             'id': id_post,
#             'titulo': titulo,
#             'conteudo': conteudo_raw,
#             'data': data.isoformat() if isinstance(data, datetime) else str(data),
#             'autor_id': autor,
#             'comentarios': [
#                 {
#                     'autor': autor_coment,
#                     'data': data_coment.isoformat() if isinstance(data_coment, datetime) else str(data_coment),
#                     'conteudo': texto_coment
#                 }
#                 for autor_coment, data_coment, texto_coment in comentarios
#             ]
#         }
        
#         # Nome do arquivo JSON
#         nome_arquivo = f"post_{id_post}.json"
#         caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
#         # Salvar o arquivo JSON
#         try:
#             with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
#                 json.dump(dados_post, arquivo, ensure_ascii=False, indent=2)
#             arquivos_salvos.append(nome_arquivo)
#             print(f"✅ JSON salvo: {nome_arquivo}")
#         except Exception as e:
#             print(f"❌ Erro ao salvar {nome_arquivo}: {e}")
    
#     return arquivos_salvos

# # Exemplo de uso
# if __name__ == "__main__":
#     try:
#         # Extrair posts do WordPress
#         posts = acessar_wordpress_mysql(
#             host='localhost',
#             usuario='root',
#             senha='casodepolicia',
#             banco='local_casodepolicia',
#             limite=999999
#         )
        
#         print(f"📊 Encontrados {len(posts)} posts no banco de dados.")
        
#         # Salvar posts como arquivos JSON na pasta 'dados'
#         arquivos = salvar_posts_json(
#             posts,
#             host='localhost',
#             usuario='root',
#             senha='casodepolicia',
#             banco='local_casodepolicia',
#             pasta_destino='./dados'  # ← AQUI define onde salvar
#         )
        
#         print(f"\n🎉 {len(arquivos)} arquivos JSON criados na pasta './dados':")
#         for arquivo in arquivos:
#             print(f"  📄 {arquivo}")
            
#     except mysql.connector.Error as e:
#         print(f"❌ Erro MySQL: {e}")
#     except Exception as e:
#         print(f"❌ Erro geral: {e}")

import os
import mysql.connector
import json
from datetime import datetime


def acessar_wordpress_mysql(host, usuario, senha, banco, limite=None):
    conn = mysql.connector.connect(
        host=host,
        user=usuario,
        password=senha,
        database=banco
    )
    cursor = conn.cursor()
    
    query = """
    SELECT ID, post_title, post_content, post_date, post_author
    FROM wp_posts 
    WHERE post_type = 'post' 
    AND post_status = 'publish'
    ORDER BY post_date DESC
    """
    
    if limite:
        query += f" LIMIT {limite}"
    
    cursor.execute(query)
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return posts


def buscar_comentarios_post(host, usuario, senha, banco, post_id):
    conn = mysql.connector.connect(
        host=host,
        user=usuario,
        password=senha,
        database=banco
    )
    cursor = conn.cursor()
    
    query = """
    SELECT comment_author, comment_date, comment_content
    FROM wp_comments
    WHERE comment_post_ID = %s
    AND comment_approved = '1'
    ORDER BY comment_date ASC
    """
    
    cursor.execute(query, (post_id,))
    comentarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return comentarios


def buscar_categorias_post(host, usuario, senha, banco, post_id):
    """
    Busca todas as categorias associadas a um post específico
    """
    conn = mysql.connector.connect(
        host=host,
        user=usuario,
        password=senha,
        database=banco
    )
    cursor = conn.cursor()
    
    query = """
    SELECT t.name, t.term_id, t.slug
    FROM wp_terms t
    INNER JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id
    INNER JOIN wp_term_relationships tr ON tt.term_taxonomy_id = tr.term_taxonomy_id
    WHERE tr.object_id = %s 
    AND tt.taxonomy = 'category'
    ORDER BY t.name
    """
    
    cursor.execute(query, (post_id,))
    categorias = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return categorias


def salvar_posts_json(posts, host, usuario, senha, banco, pasta_destino='./dados'):
    """
    Esta função cria a pasta 'dados' e salva os JSONs lá
    """
    # Criar a pasta 'dados' se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"📁 Pasta '{pasta_destino}' criada.")
    
    arquivos_salvos = []
    
    for post in posts:
        id_post = post[0]
        titulo = post[1] 
        conteudo_raw = post[2]
        data = post[3]
        autor = post[4]
        
        # Buscar comentários do post
        comentarios = buscar_comentarios_post(host, usuario, senha, banco, id_post)
        
        # Buscar categorias do post
        categorias = buscar_categorias_post(host, usuario, senha, banco, id_post)
        
        # Estruturar dados em formato JSON
        dados_post = {
            'id': id_post,
            'titulo': titulo,
            'conteudo': conteudo_raw,
            'data': data.isoformat() if isinstance(data, datetime) else str(data),
            'autor_id': autor,
            'categorias': [
                {
                    'nome': nome_cat,
                    'id': id_cat,
                    'slug': slug_cat
                }
                for nome_cat, id_cat, slug_cat in categorias
            ],
            'comentarios': [
                {
                    'autor': autor_coment,
                    'data': data_coment.isoformat() if isinstance(data_coment, datetime) else str(data_coment),
                    'conteudo': texto_coment
                }
                for autor_coment, data_coment, texto_coment in comentarios
            ]
        }
        
        # Nome do arquivo JSON
        nome_arquivo = f"post_{id_post}.json"
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
        # Salvar o arquivo JSON
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(dados_post, arquivo, ensure_ascii=False, indent=2)
            arquivos_salvos.append(nome_arquivo)
            print(f"✅ JSON salvo: {nome_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao salvar {nome_arquivo}: {e}")
    
    return arquivos_salvos


# Exemplo de uso
if __name__ == "__main__":
    try:
        # Extrair posts do WordPress
        posts = acessar_wordpress_mysql(
            host='localhost',
            usuario='root',
            senha='casodepolicia',
            banco='local_casodepolicia',
            limite=999999
        )
        
        print(f"📊 Encontrados {len(posts)} posts no banco de dados.")
        
        # Salvar posts como arquivos JSON na pasta 'dados'
        arquivos = salvar_posts_json(
            posts,
            host='localhost',
            usuario='root',
            senha='casodepolicia',
            banco='local_casodepolicia',
            pasta_destino='./dados'
        )
        
        print(f"\n🎉 {len(arquivos)} arquivos JSON criados na pasta './dados':")
        for arquivo in arquivos:
            print(f"  📄 {arquivo}")
            
    except mysql.connector.Error as e:
        print(f"❌ Erro MySQL: {e}")
    except Exception as e:
        print(f"❌ Erro geral: {e}")
