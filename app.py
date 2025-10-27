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

    flash(f"✅ Interesse registrado com sucesso no projeto ID {projeto_id}!", "success")
    return redirect(url_for('projeto_detalhes', projeto_id=projeto_id))


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


# =========================
# Login com níveis de acesso (admin / user)
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')

        # Carrega usuários do arquivo JSON
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)

        # Busca usuário correspondente
        usuario = next((u for u in users if u['username'] == user and u['password'] == password), None)

        if usuario:
            session['logged_in'] = True
            session['user'] = usuario['username']
            session['role'] = usuario['role']

            if usuario['role'] == 'admin':
                flash(f"👑 Bem-vindo, administrador {usuario['username']}!", "success")
                return redirect(url_for('admin_dashboard'))
            else:
                flash(f"✅ Login realizado com sucesso, {usuario['username']}!", "success")
                return redirect(url_for('index'))
        else:
            flash("❌ Usuário ou senha incorretos!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    users_file = "users.json"

    # Garante que o arquivo existe
    if not os.path.exists(users_file):
        with open(users_file, "w", encoding="utf-8") as f:
            json.dump([], f)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # Validações básicas
        if password != confirm:
            flash("❌ As senhas não coincidem.", "error")
            return redirect(url_for('cadastro'))

        with open(users_file, "r", encoding="utf-8") as f:
            users = json.load(f)

        # Verifica se o usuário já existe
        if any(u["username"] == username for u in users):
            flash("⚠️ Este nome de usuário já está em uso.", "error")
            return redirect(url_for('cadastro'))

        # Cria novo usuário padrão (role = user)
        novo_usuario = {
            "username": username,
            "password": password,
            "role": "user"
        }

        users.append(novo_usuario)
        with open(users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

        flash("✅ Cadastro realizado com sucesso! Faça login para continuar.", "success")
        return redirect(url_for('login'))

    return render_template('cadastro.html')


# =========================
# Área administrativa (CRUD)
# =========================

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("Acesso restrito. Faça login como administrador.", "error")
        return redirect(url_for('login'))

    projetos = carregar_projetos()
    return render_template('admin_dashboard.html', projetos=projetos)


@app.route('/admin/novo', methods=['GET', 'POST'])
def novo_projeto():
    if session.get('role') != 'admin':
        flash("Acesso restrito a administradores.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        projetos = carregar_projetos()
        novo = {
            "id": len(projetos) + 1,
            "titulo": request.form['titulo'],
            "categoria": request.form['categoria'],
            "status": request.form['status'],
            "professor": request.form['professor'],
            "descricao_curta": request.form['descricao_curta'],
            "detalhes": [request.form['detalhes']],
            "imagem": "img/default.png",
            "links": {}
        }
        projetos.append(novo)
        with open("projects_data.json", "w", encoding="utf-8") as f:
            json.dump(projetos, f, indent=4, ensure_ascii=False)
        flash("✅ Projeto criado com sucesso!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_form.html', projeto=None)


@app.route('/admin/editar/<int:projeto_id>', methods=['GET', 'POST'])
def editar_projeto(projeto_id):
    if session.get('role') != 'admin':
        flash("Acesso restrito a administradores.", "error")
        return redirect(url_for('index'))

    projetos = carregar_projetos()
    projeto = next((p for p in projetos if p["id"] == projeto_id), None)
    if not projeto:
        abort(404)

    if request.method == 'POST':
        projeto["titulo"] = request.form['titulo']
        projeto["categoria"] = request.form['categoria']
        projeto["status"] = request.form['status']
        projeto["professor"] = request.form['professor']
        projeto["descricao_curta"] = request.form['descricao_curta']
        projeto["detalhes"] = [request.form['detalhes']]

        with open("projects_data.json", "w", encoding="utf-8") as f:
            json.dump(projetos, f, indent=4, ensure_ascii=False)

        flash("✅ Projeto atualizado com sucesso!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_form.html', projeto=projeto)


@app.route('/admin/excluir/<int:projeto_id>')
def excluir_projeto(projeto_id):
    if session.get('role') != 'admin':
        flash("Acesso restrito a administradores.", "error")
        return redirect(url_for('index'))

    projetos = carregar_projetos()
    projetos = [p for p in projetos if p["id"] != projeto_id]

    with open("projects_data.json", "w", encoding="utf-8") as f:
        json.dump(projetos, f, indent=4, ensure_ascii=False)

    flash("🗑️ Projeto excluído com sucesso!", "success")
    return redirect(url_for('admin_dashboard'))


# =========================
# Logout
# =========================
@app.route('/logout')
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for('index'))


# =========================
# Submissão de projetos (restrita a logados)
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
