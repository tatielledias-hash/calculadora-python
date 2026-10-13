print("Calculadora simples")

numero1 = float(input("Digite o primeiro número: "))
operacao = input("Escolha a operação (+, -, *, /): ")
numero2 = float(input("Digite o segundo número: "))

if operacao == "+":
    resultado = numero1 + numero2
elif operacao == "-":
    resultado = numero1 - numero2
elif operacao == "*":
    resultado = numero1 * numero2
elif operacao == "/":
    if numero2 == 0:
        resultado = "Não é possível dividir por zero."
    else:
        resultado = numero1 / numero2
else:
    resultado = "Operação inválida."

print("Resultado:", resultado)