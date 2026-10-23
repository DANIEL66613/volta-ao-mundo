import random
import unicodedata
import time


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )


def jogar():
    sequencia = "voltaaomundo"
    posicao = 0
    erros = 0
    limite_erros = random.randint(3, 8)

    print("🌎o nome do jogo é VOLTA AO MUNDO")
    print("voçe precisa escrever seu destino e logo na sequencia um meio de transporte para chegar lá\n eu vou decidir se vc chega ou não, vamos lá?!")
    time.sleep(2)
    print("Diga para onde você vai e como vai chegar!")
    print("Digite 'sair' para encerrar.\n")

    while True:
        destino = input("Para onde você vai? ").strip()

        if normalizar(destino) == "sair":
            print("Até a próxima viagem!")
            break

        if not destino:
            print("Digite um destino.\n")
            continue

        transporte = input("Como você vai? ").strip()

        if normalizar(transporte) == "sair":
            print("Até a próxima viagem!")
            break

        if not transporte:
            print("Digite um meio de transporte.\n")
            continue

        if normalizar(destino)[0] == sequencia[posicao]:
            print(f"✅ Pode ir para {destino} de {transporte}!\n")
            posicao += 1

            if posicao == len(sequencia):
                print("🎉 Você completou a volta ao mundo!\n")
                posicao = 0
                erros = 0
                limite_erros = random.randint(3, 8)
        else:
            print("❌ Essa viagem não vale!\n")
            erros += 1

            if erros >= limite_erros:
                print("eu acho que vc não está se saindo muito bem, Oh, vamos tentar de novo!?\n")
                print("🌎o nome do jogo é VOLTA AO MUNDO")
                print("voçe precisa escrever seu destino e logo na sequencia um meio de transporte para chegar lá\n eu vou decidir se voçe chega ou não, vamos lá?!")
                time.sleep(2)
                posicao = 0
                erros = 0
                limite_erros = random.randint(3, 8)


jogar()