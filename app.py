# 
# GERADOR DAS PAGINA ESTATICAS ATENCAO AO TEM QUE MUDAR O NOME DO ARQUIVO
# 
# 
import os
import markdown
from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def nova_pagina():
    if request.method == "POST":
        texto_input = request.form.get("arquivo-texto")
        print(texto_input)

    else:
        texto_input = "texto.md"
        with open(texto_input, "r", encoding="utf-8") as file:
            conteudo = markdown.markdown(file.read())
            site_estatico = render_template("index.html", conteudo=conteudo)
            converte_estatico(site_estatico, "inicio-projeto-blog.html")
            return render_template("index.html", conteudo=conteudo)



# FUNCAO PARA EXTRAIR O HML ESTATICO
def converte_estatico(renderizado, nova_pagina):
    output_dir = 'estaticos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, nova_pagina)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(renderizado)

app.run(debug=True)