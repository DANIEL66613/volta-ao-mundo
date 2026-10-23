import random
import unicodedata

from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = "volta-ao-mundo-teste-local"


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )


def reiniciar():
    session["posicao"] = 0
    session["erros"] = 0
    session["limite_erros"] = random.randint(3, 8)


PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Volta ao Mundo</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            background: #101827;
            color: #f3f4f6;
            font-family: Arial, sans-serif;
            padding: 24px;
        }

        main {
            width: 100%;
            max-width: 480px;
            background: #1e293b;
            padding: 32px;
            border-radius: 20px;
        }

        h1 {
            margin-top: 0;
        }

        p {
            line-height: 1.6;
        }

        label {
            display: block;
            margin: 20px 0 8px;
        }

        input, button {
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            font-size: 16px;
        }

        input {
            border: 1px solid #64748b;
            background: #0f172a;
            color: white;
        }

        button {
            margin-top: 24px;
            border: 0;
            background: #38bdf8;
            color: #082f49;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #7dd3fc;
        }

        .resposta {
            margin-top: 24px;
            padding: 16px;
            background: #0f172a;
            border-radius: 10px;
        }

        .reinicio {
            color: #fcd34d;
        }
    </style>
</head>

<body>
    <main>
        <h1>🌎 Volta ao Mundo</h1>

        <p>
            Escreva seu destino e um meio de transporte.
            Eu vou decidir se você chega ou não.
            Consegue descobrir a regra?
        </p>

        <form method="post">
            <label for="destino">Para onde você vai?</label>
            <input
                id="destino"
                name="destino"
                placeholder="Digite um destino"
                required
                autofocus
            >

            <label for="transporte">Como você vai?</label>
            <input
                id="transporte"
                name="transporte"
                placeholder="Digite um meio de transporte"
                required
            >

            <button type="submit">Viajar ✈️</button>
        </form>

        {% if mensagem %}
            <div class="resposta" role="status">
                {{ mensagem }}
            </div>
        {% endif %}

        {% if aviso %}
            <p class="reinicio">{{ aviso }}</p>
        {% endif %}
    </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def jogar():
    if "posicao" not in session:
        reiniciar()

    mensagem = ""
    aviso = ""

    if request.method == "POST":
        destino = request.form.get("destino", "").strip()
        transporte = request.form.get("transporte", "").strip()
        destino_normalizado = normalizar(destino)

        if not destino_normalizado or not transporte:
            mensagem = "Preencha o destino e o meio de transporte."
        else:
            sequencia = "voltaaomundo"
            posicao = session["posicao"]

            if destino_normalizado[0] == sequencia[posicao]:
                mensagem = (
                    f"✅ Pode ir para {destino} de {transporte}!"
                )

                session["posicao"] += 1

                if session["posicao"] == len(sequencia):
                    aviso = (
                        "🎉 Você completou a volta ao mundo! "
                        "Vamos começar outra viagem?"
                    )
                    reiniciar()
            else:
                mensagem = "❌ Essa viagem não vale!"
                session["erros"] += 1

                if session["erros"] >= session["limite_erros"]:
                    aviso = (
                        "Oh, vamos tentar de novo! "
                        "🌎 O nome do jogo é VOLTA AO MUNDO."
                    )
                    reiniciar()

    return render_template_string(
        PAGINA,
        mensagem=mensagem,
        aviso=aviso
    )


if __name__ == "__main__":
    app.run()