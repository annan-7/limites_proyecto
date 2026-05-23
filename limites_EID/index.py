from sympy import limit, sin, Symbol

Valor_de_a= int(input("Ingrese el valor de a: "))
fxis = input("Ingrese la función f(x): ")

x = Symbol('x')


def Limite_finito(Y, Valor_de_a):
    limite = limit(Y, x, Valor_de_a)
    if limite.is_finite:
        return limite
    else:
        return "El límite no es finito" 
    
def limite_infinito(Y, Valor_de_a):
    limite = limit(Y, x, Valor_de_a)
    if limite.is_infinite:
        return limite
    else:
        return "El límite no es infinito"

def limite_no_existe(Y, Valor_de_a):
    limite = limit(Y, x, Valor_de_a)
    if limite.is_infinite or limite.is_finite:
        return "El límite existe"
    else:
        return "El límite no existe"
    
def limites_Laterales(Y,Valor_de_a):
    limit_izquierda= limit(Y,x,Valor_de_a,"-")
    limit_derecha = limit(Y,x,Valor_de_a, "+")
    if(limit_derecha==limit_izquierda):
        return limit_izquierda
    else:
        print(f"No existe, de izquierda tiende a:{limit_izquierda} y de derecha tiende a :{limit_derecha}")
        return limit_izquierda,limit_derecha;



lim1= limites_Laterales(fxis, Valor_de_a)
print(f"El limite tiende a {lim1} ")