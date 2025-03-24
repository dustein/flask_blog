# 
# GERADOR DAS PAGINA ESTATICAS ATENCAO AO TEM QUE MUDAR O NOME DO ARQUIVO
# 
# 
import os
from flask import Flask, url_for, render_template

app = Flask(__name__)

# url_for('static', filename='style.css')

@app.route("/")
def nova_pagina():
    site_estatico = render_template("index.html")
    converte_estatico(site_estatico, "inicio-projeto-blog.html")
    return render_template("index.html")

def converte_estatico(renderizado, nova_pagina):
    output_dir = 'estaticos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, nova_pagina)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(renderizado)

app.run(debug=True)