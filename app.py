from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
import json, os

app = Flask(__name__)
app.secret_key = "sisCPTI_secret_key"

# =========================
# Função auxiliar para ler projetos
# =========================
def carregar_projetos():
    file_path = "projects_data.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# =========================
# Rotas principais
# =========================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/projetos')
def projetos():
    projetos = carregar_projetos()
    return render_template('projetos.html', projetos=projetos)


@app.route('/projeto/<int:projeto_id>')
def projeto_detalhes(projeto_id):
    projetos = carregar_projetos()
    projeto = next((p for p in projetos if p["id"] == projeto_id), None)
    if not projeto:
        abort(404)
    return render_template('projeto_detalhes.html', projeto=projeto)


@app.route('/projeto/<int:projeto_id>/interesse', methods=['POST'])
def registrar_interesse(projeto_id):
    if not session.get('logged_in'):
        flash("⚠️ Você precisa estar logado para demonstrar interesse em um projeto.", "error")
        return redirect(url_for('login'))

    # Simula o registro (poderia salvar em JSON ou banco de dados futuramente)
    flash(f"✅ Interesse registrado com sucesso no projeto ID {projeto_id}!", "success")
    return redirect(url_for('projeto_detalhes', projeto_id=projeto_id))



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


# =========================
# Login simples (simulado)
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        # Simulação simples de login
        if user == "admin" and password == "123":
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Usuário ou senha incorretos!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


# =========================
# Submissão de projetos (restrita)
# =========================
@app.route('/submissao', methods=['GET', 'POST'])
def submissao():
    if not session.get('logged_in'):
        flash("⚠️ Você precisa estar logado para acessar a submissão de projetos.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = {
            "nome_projeto": request.form.get("nome_projeto"),
            "categoria": request.form.get("categoria"),
            "descricao": request.form.get("descricao"),
            "proponente": request.form.get("proponente"),
            "email": request.form.get("email"),
            "status": request.form.get("status")
        }

        file_path = "submissoes.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                submissoes = json.load(f)
        else:
            submissoes = []

        submissoes.append(data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(submissoes, f, indent=4, ensure_ascii=False)

        flash("✅ Projeto submetido com sucesso!", "success")
        return redirect(url_for("submissao"))

    return render_template('submissao.html')


# =========================
# Execução
# =========================
if __name__ == '__main__':
    app.run(debug=True)
