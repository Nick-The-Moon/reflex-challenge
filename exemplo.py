
# Importa bibliotecas para controlar o tempo e gerar valores aleatórios
import time
import random

print("Prepare-se para testar seu tempo de reação!")
print("Quando você vir a mensagem '>>> AGORA! <<<', pressione ENTER o mais rápido possível.")
print("Aguarde...")
time.sleep(2)  # Pausa a execução por 2 segundos para dar tempo de leitura

# Gera uma espera aleatória entre 1 e 10 segundos
# uniform() sorteia um número decimal dentro do intervalo informado
espera = random.uniform(1, 10)

# sleep() pausa a execução do programa pelo tempo sorteado
time.sleep(espera)

# perf_counter() registra o tempo com alta precisão
# É ideal para medir intervalos curtos, como o tempo de reação
inicio = time.perf_counter()

# input() exibe o estímulo e aguarda o jogador pressionar ENTER
input(">>> AGORA! <<<")

# Registra o instante em que o jogador respondeu
fim = time.perf_counter()

# Calcula a diferença entre o tempo final e o inicial
# Multiplica por 1000 para converter segundos em milissegundos
tempo = (fim - inicio) * 1000

# Exibe o resultado com duas casas decimais
# :.2f formata o número para apresentar duas casas após a vírgula
print(f"Seu tempo de reação: {tempo:.2f} ms")
