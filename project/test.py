largo = int(input("Ingrese el largo: "))
ancho = int(input("Ingrese el ancho: "))

print("*" * largo)

for i in range(ancho - 2):
    print("*" + " " * (largo - 2) + "*")

print("*" * largo)



def fibonacci_recursivo(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)

# Ejemplo de uso:
n = 10
secuencia = [fibonacci_recursivo(i) for i in range(n)]
print(secuencia)
print(fibonacci_recursivo(9))