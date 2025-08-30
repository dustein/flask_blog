# import mysql.connector

# config = {
#     'user': 'root',
#     'password': 'casodepolicia',
#     'host': 'localhost',
#     'database': 'local_casodepolicia',
#     'port': 3306
# }

# try:
#     conn = mysql.connector.connect(**config)
#     cursor = conn.cursor(dictionary=True)
    
#     query = "SELECT post_title, post_date, post_content FROM wp_posts WHERE post_status = 'publish' AND post_type = 'post';"
    
#     cursor.execute(query)
#     posts = cursor.fetchall()
    
#     print(f"Foram encontrados {len(posts)} posts publicados:\n")


# except mysql.connector.Error as err:
#     print(f"Erro ao executar a consulta: {err}")

# finally:
#     if cursor:
#         cursor.close()
#     if conn:
#         conn.close()

import mysql.connector
import os

config = {
    'user': 'root',
    'password': 'casodepolicia',
    'host': 'localhost',
    'database': 'local_casodepolicia',
    'port': 3306
}

def sanitize_filename(name):
    # Remove caracteres inválidos para nomes de arquivos
    import re
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip()

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    # Buscar posts publicados
    query_posts = """
        SELECT ID, post_title, post_date, post_content 
        FROM wp_posts 
        WHERE post_status = 'publish' AND post_type = 'post'
        LIMIT 2;
    """
    cursor.execute(query_posts)
    posts = cursor.fetchall()

    print(f"Foram encontrados {len(posts)} posts publicados.")

    # Para cada post, buscar comentários e gerar arquivo markdown
    for post in posts:
        post_id = post['ID']
        title = post['post_title']
        date = post['post_date']
        content = post['post_content']

        # Buscar comentários do post
        query_comments = """
            SELECT comment_author, comment_date, comment_content
            FROM wp_comments
            WHERE comment_post_ID = %s
            ORDER BY comment_date ASC;
        """
        cursor.execute(query_comments, (post_id,))
        comments = cursor.fetchall()

        # Criar nome de arquivo seguro para salvar
        # filename = sanitize_filename(f"{post_id}-{title}.md")
        filename = sanitize_filename(f"{post_id}-{title}.html")

        def make_paragraphs(text):
            # Divide nos parágrafos usando linhas em branco
            partes = [p.strip() for p in text.split('\n\n') if p.strip()]

            # Cria uma nova lista com as quebras de linha substituídas
            paragrafos_formatados = [p.replace('\n', ' ') for p in partes]

            # Encapsula cada parte em <p>
            return '\n'.join([f"<p>{p}</p>" for p in paragrafos_formatados])


        # Construir conteúdo markdown
        md_content = f"<h1 class='script_titulo'>{title}</h1>\n\n"
        md_content += f"<p class='script_publicado'>Publicado em: {date}</p>\n\n"
        corpo_html = make_paragraphs(content)
        md_content += corpo_html + "\n"
        md_content += "## Comentários\n\n"

        if comments:
            for c in comments:
                md_content += f"### {c['comment_author']} em {c['comment_date']}\n\n"
                md_content += f"{c['comment_content']}\n\n"
        else:
            md_content += "_Nenhum comentário encontrado._\n"

        # Salvar o arquivo markdown
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Arquivo gerado: {filename}")

except mysql.connector.Error as err:
    print(f"Erro ao executar a consulta: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

