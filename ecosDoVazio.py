import os
import random
import time
import sys

atributos = {
    "engenheiro": [110, 80],
    "soldado": [160, 40],
    "psionico": [90, 140]
}

itens_iniciais = {
    "engenheiro": ["chave multifunção", "kit médico", "bateria de energia"],
    "soldado": ["rifle de plasma", "kit médico", "kit médico"],
    "psionico": ["cristal psiônico", "bateria de energia", "bateria de energia"]
}

vidaPlayer = 0
energiaPlayer = 0
xp = 0
nivel = 1
classe = ""
ataques = []
inventario = []
capacidade_maxima = 10
xpreq = 100

ataques_classe = {
    "engenheiro": [
        {"nome": "Disparo de sucata", "dano": 18, "energia": 0},
        {"nome": "Drone de ataque", "dano": 40, "energia": 25},
        {"nome": "Sobrecarga do reator", "dano": 160, "energia": 110}
    ],
    "soldado": [
        {"nome": "Rajada curta", "dano": 20, "energia": 0},
        {"nome": "Granada de choque", "dano": 60, "energia": 20},
        {"nome": "Artilharia orbital", "dano": 130, "energia": 55}
    ],
    "psionico": [
        {"nome": "Impacto mental", "dano": 45, "energia": 25},
        {"nome": "Lâminas da mente", "dano": 15, "energia": 5},
        {"nome": "COLAPSO PSIÔNICO", "dano": 240, "energia": 140}
    ]
}

inimigos = [
    {"nome": "Drone Sentinela", "vida": 90, "dano": 9, "xpI": 28, "drop": "núcleo de drone"},
    {"nome": "Mutante Radioativo", "vida": 260, "dano": 24, "xpI": 72, "drop": "tecido mutado"},
    {"nome": "Andróide Corrompido", "vida": 65, "dano": 13, "xpI": 16, "drop": "placa circuito"},
    {"nome": "Saqueador Espacial", "vida": 130, "dano": 16, "xpI": 44, "drop": "insígnia saqueadora"}
]


def print_lento(texto, velocidade=0.08):
    for caractere in texto:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(velocidade)


def limpar():
    if os.name == 'posix':
        time.sleep(2)
        os.system('clear')
    elif os.name == 'nt':
        time.sleep(2)
        os.system('cls')


def limpartxt():
    if os.name == 'posix':
        time.sleep(3)
        os.system('clear')
    elif os.name == 'nt':
        time.sleep(3)
        os.system('cls')


def mostrar_inventario():
    print("\n---Inventário---")
    if not inventario:
        print("Seu inventário está vazio.")
    else:
        for item in set(inventario):
            print(f"- {item} x{inventario.count(item)}")
    print(f"Total: {len(inventario)}/{capacidade_maxima}")


def adicionar_item(item):
    if len(inventario) < capacidade_maxima:
        inventario.append(item)
    else:
        print("Inventário cheio!!! Não foi possível adicionar o item.")


def usar_item():
    global vidaPlayer, energiaPlayer
    mostrar_inventario()
    item = input("Digite o nome do item que deseja usar: ").strip().lower()
    if item not in inventario:
        print("Item não encontrado.")
        return
    if item == "kit médico":
        vidaPlayer += 30
        print("Você usou um kit médico e recuperou 30 de vida.")
    elif item == "bateria de energia":
        energiaPlayer += 30
        print("Você usou uma bateria de energia e recuperou 30 de energia.")
    else:
        print("Esse item não pode ser usado.")
        return
    inventario.remove(item)


def criarP():
    global vidaPlayer, energiaPlayer, ataques, classe, nome

    while True:
        nome = input("Antes de tudo, qual é o seu nome? ").strip()
        print(f"\nOlá, {nome.capitalize()}!")

        print("\nVocê precisa escolher uma classe:")
        print("1 - Psiônico  | Vida: 90  | Energia: 140")
        print("2 - Soldado   | Vida: 160 | Energia: 40")
        print("3 - Engenheiro| Vida: 110 | Energia: 80\n")

        try:
            classe = int(input("Insira o número da sua classe: ").strip())
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

        if classe == 1:
            classe_nome = "psionico"
        elif classe == 2:
            classe_nome = "soldado"
        elif classe == 3:
            classe_nome = "engenheiro"
        else:
            print("Classe inválida. Tente novamente.\n")
            continue
        vidaPlayer, energiaPlayer = atributos[classe_nome]
        ataques = ataques_classe[classe_nome]
        classe = classe_nome
        for item in itens_iniciais[classe]:
            adicionar_item(item)

        limpar()

        print(f"{classe_nome.capitalize()} | Vida: {vidaPlayer} | Energia: {energiaPlayer}")
        print("\nSeus Ataques:")
        for ataque in ataques:
            print(f"- {ataque['nome']} | Dano: {ataque['dano']} | Energia: {ataque['energia']}")

        mostrar_inventario()

        classeE = input("\nTem certeza que esse é seu personagem? (s/n): ").strip().lower()
        if classeE == "s":
            print("\nAgora você está pronto!!!")
            limpar()
            break

        elif classeE == "n":
            limpar()
            print("Voltando para a criação de personagem...\n")
        else:
            print("Resposta inválida. Vamos tentar novamente.")
            limpar()


def LvUp():
    global xp, nivel, xpreq, vidaPlayer, energiaPlayer

    if xp >= xpreq:
        nivel += 1
        xpreq += 100
        xp = 0
        print(f"\nVocê subiu para o nivel {nivel}")
        vidaPlayer += 15
        energiaPlayer += 25
        print(f"\nSua vida aumentou em 15 pontos")
        print(f"\nSua Energia aumentou em 25 pontos")


def batalha():
    global vida_inimigo, vidaPlayer, energiaPlayer, xp

    inimigo = random.choice(inimigos)
    vida_inimigo = inimigo["vida"]
    tipo_inimigo = inimigo["nome"]
    dano_inimigo = inimigo["dano"]
    xp_inimigo = inimigo["xpI"]
    drop_inimigo = inimigo["drop"]
    limpar()

    print("\n                                                 ")
    print_lento(f"\nUm {tipo_inimigo} apareceu! Vida: {vida_inimigo}\n")

    while vida_inimigo > 0 and vidaPlayer > 0:
        print("Seu turno:")
        print(f"Vida: {vidaPlayer} | Energia: {energiaPlayer}")
        print(f"Inimigo: {tipo_inimigo} | Vida: {vida_inimigo}\n")

        print("1 - Atacar")
        print("2 - Inventário")
        print("3 - Fugir")
        energiaPlayer += 25

        try:
            acao = int(input("Escolha uma ação: "))
        except ValueError:
            print("Por favor, insira uma opção válida!")
            continue

        if acao == 1:
            print("\nAtaques disponíveis:")
            for i, atk in enumerate(ataques):
                print(f"{i+1} - {atk['nome']} (Dano: {atk['dano']} | Energia: {atk['energia']})")
            try:
                escolha = int(input("Escolha seu ataque: ")) - 1
                if escolha not in range(len(ataques)):
                    print("Escolha inválida. Tente novamente.")
                    continue

                ataque = ataques[escolha]
                if energiaPlayer < ataque["energia"]:
                    print("Energia insuficiente para este ataque.")
                    continue

                energiaPlayer -= ataque["energia"]
                vida_inimigo -= ataque["dano"]
                print(f"\nVocê usou {ataque['nome']} e causou {ataque['dano']} de dano!")

                if vida_inimigo <= 0:
                    print(f"{tipo_inimigo} foi derrotado!")
                    xp += xp_inimigo
                    print(f"XP ganho: {xp_inimigo} | Total: {xp}/{xpreq}")
                    LvUp()
                    print(f"Você coletou 1x {drop_inimigo} de {tipo_inimigo} ")
                    inventario.append(drop_inimigo)

                    break
            except ValueError:
                print("Entrada inválida, tente novamente.")
                continue

        elif acao == 2:
            while True:
                print("\n1 - Ver inventário")
                print("2 - Usar item")
                print("3 - Voltar")
                escolha = input("Escolha uma opção: ")

                if escolha == "1":
                    mostrar_inventario()

                elif escolha == "2":
                    usar_item()

                elif escolha == "3":
                    energiaPlayer += 25
                    print("Você recuperou 25 de energia")
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif acao == 3:
            chance_fuga = random.randint(1, 100)
            if chance_fuga <= 40:
                print("Você fugiu com sucesso!")
                break
            else:
                print("O inimigo te impede de fugir!")
                continue
        else:
            print("Opção inválida, escolha novamente.")

        if vida_inimigo > 0:
            dano = random.randint(5, dano_inimigo)
            vidaPlayer -= dano
            print(f"\nO {tipo_inimigo} te atacou e causou {dano} de dano.")
            if vidaPlayer <= 0:
                print("Você foi derrotado.")
                break
        energiaPlayer += 25
        print("Você recuperou 25 de energia")
        time.sleep(2)
        limpar()


def batalhaBOSSFinal():
    global vidaPlayer, energiaPlayer, xp, nivel

    boss = {"nome": "......S̷̙̈I̶͖͐N̷̯̎G̷͈̈U̶͙̽L̴̬̈A̷̜͌R̸̗̊I̴̙͐D̶͇̀A̸͖̋D̷͈̈E̸̥̎......", "vida": 99999, "dano": 99999}
    vida_boss = boss["vida"]
    tipo_boss = boss["nome"]
    dano_boss = boss["dano"]
    limpar()
    print_lento(".....")
    print_lento("\nAs luzes da nave piscam e depois morrem por completo.")
    print_lento("\nO zumbido dos motores cessa... o silêncio é absoluto.")
    print_lento("\n........")
    print_lento("\nNos monitores mortos, uma forma geométrica impossível começa a se desenhar...")
    print_lento("\nCircuitos ardem em roxo ao redor de uma inteligência que não deveria existir...")
    print_lento("....")
    print_lento("\nUma consciência antiga desperta nos servidores da estação...")
    print_lento("\nDAS PROFUNDEZAS DO CÓDIGO ESQUECIDO PELOS PRÓPRIOS CRIADORES...")
    print_lento("\nA SINGULARIDADE SE MANIFESTA....")
    print_lento("\nE O NOME DELA QUEIMA SUA MENTE COMO ESTÁTICA:")
    print_lento("\n......S̷̙̈I̶͖͐N̷̯̎G̷͈̈U̶͙̽L̴̬̈A̷̜͌R̸̗̊I̴̙͐D̶͇̀A̸͖̋D̷͈̈E̸̥̎......")
    print_lento("\nSeu corpo trava. Seus implantes falham. Sua visão pisca em estática......")
    print_lento("\n.........")
    print_lento("\nMas não há como desconectar agora...")
    print_lento("\nVocê foi escolhido para enfrentar a mente que consumiu a estação inteira.")
    print_lento("\n.....")
    limpar()
    print(f"\n {tipo_boss} apareceu!!!!!!!!!! Vida: {vida_boss}\n")

    while vida_boss > 0 and vidaPlayer > 0:
        print(f"\nSeu turno | Vida: {vidaPlayer} | Energia: {energiaPlayer}")
        print(f"{tipo_boss} | Vida: ????????")
        print("1 - Atacar\n2 - Inventário\n3 - Fugir")
        energiaPlayer += 10

        try:
            acao = int(input("Escolha uma ação: "))
        except ValueError:
            print("Ação inválida.")
            continue

        if acao == 1:
            print("\nAtaques:")
            for i, atk in enumerate(ataques):
                print(f"{i+1} - {atk['nome']} (Dano: {atk['dano']} | Energia: {atk['energia']})")
            try:
                escolha = int(input("Escolha seu ataque: ")) - 1
                ataque = ataques[escolha]
                if energiaPlayer < ataque["energia"]:
                    print("Energia insuficiente.")
                    continue
                energiaPlayer -= ataque["energia"]
                vida_boss -= ataque["dano"]
                print(f"\nVocê usou {ataque['nome']} e causou {ataque['dano']} de dano!")
            except:
                print("Escolha inválida.")
                continue

        elif acao == 2:
            mostrar_inventario()
            usar_item()

        elif acao == 3:
            print("Você tenta fugir, mas ELA já está em todos os sistemas!")
            continue

        if vida_boss > 0:
            dano = random.randint(10, dano_boss)
            vidaPlayer -= dano
            print(f"O {tipo_boss} atacou e causou {dano} de dano.")
            if vidaPlayer <= 0:
                limpartxt()
                print_lento(f"\nVocê foi derrotado pela {tipo_boss}...")
                print_lento(f"\n Obrigado por jogar a Demo")
                return

    print(f" Parabéns! Você derrotou a {tipo_boss}!")
    print("E assim Acaba  ")


criarP()

print_lento("\nAlarme... escuridão.")
print_lento("\nSua cabeça lateja como se tivesse levado um choque. Um zumbido não sai da sua orelha.")
print_lento("\nVocê acorda em uma cápsula de contenção quebrada, presa por travas de metal frio.")
print_lento("\nUma luz de emergência vermelha pisca pelas frestas de uma escotilha amassada.")
print_lento("\nCom esforço, você força as travas e rasteja até a escotilha.")
print_lento("\nAo abri-la, um rangido metálico ecoa pelo corredor vazio da estação...")
print_lento("\nVocê não está sozinho aqui.")
print_lento("\nÀ frente, um som estranho rompe o silêncio.")
print_lento("....")

limpartxt()

batalha()

print_lento("\n...............")

batalha()

limpar()

print_lento("\nApós o combate, você continua avançando pelos corredores escuros da estação...")

print_lento("\nSente que algo te observa pelas câmeras quebradas.")
print_lento("\nDe repente, um toque metálico no ombro te faz gelar.")

print_lento("\n— Ei, estranho!")
print_lento("\n— O que cê tá fazendo aqui? Parece que saiu de uma explosão...")
print_lento("......")
print_lento("\n— Que foi? Perdeu a voz no vácuo?")
print_lento("\n— Não importa. Meu nome é Deco.")

print_lento(f"\n# Você digita seu nome num terminal quebrado que Deco te entrega #")
print_lento(f"\n— {nome.upper()}?! Hahaha, que nome de código sinistro!")

print_lento(f"\n— Vamos, {nome.capitalize()}. Sei onde fica o hangar de fuga.")

limpartxt()

limpartxt()

print_lento("Vocês caminham cautelosamente pelos corredores da estação...")

limpartxt()

print_lento("\nUma escotilha se abre, revelando o cais de atracação. Naves gigantescas, quase orgânicas, com cabos como tentáculos presos ao teto.")
print_lento("\nMas Deco desapareceu. Só resta o zumbido dos geradores e o eco distante de passos metálicos.")
print_lento("\nAlgo está errado.")
print_lento("\nA estação parece viva, e o medo te envolve. Você está mais sozinho do que nunca.")
print_lento("\nO silêncio é ensurdecedor.")

limpartxt()

print_lento("\nUm som abafado rompe o silêncio. Algo se move na escuridão do cais.")
print_lento("\nO ar fica gelado, e uma sensação de perigo iminente toma conta de você.")
print_lento("\nTrês vultos surgem entre os contêineres, esperando por você...")
print_lento("........")

batalha()

print_lento("\n...............")

batalha()

print_lento("\n...............")

batalha()

limpar()

print_lento("\nApós a última batalha, o silêncio retorna.")
print_lento("\nA dor na sua cabeça é insuportável, como interferência elétrica perfurando sua mente.")
print_lento("\nSua visão pisca, e o mundo ao seu redor começa a se distorcer em estática.")
print_lento("\n...")
print_lento("\nVocê tenta resistir, mas a dor te consome. Seus sentidos falham.")
print_lento("\nA presença de algo imenso e onipresente toma conta de você...")

batalhaBOSSFinal()
