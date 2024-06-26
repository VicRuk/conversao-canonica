import sympy as sp
from sympy.logic.boolalg import *

def transformar_expressao(expressao):
    # Avaliar a expressão usando sympy
    expr_sympy = sp.sympify(expressao, evaluate=False)
    
    # Função para eliminar implicações e bicondicionais
    def eliminar_condicionais(expr):
        if expr.is_Atom:
            return expr
        if isinstance(expr, Implies):
            a, b = expr.args
            return Or(Not(eliminar_condicionais(a)), eliminar_condicionais(b))
        if isinstance(expr, sp.Eq):
            a, b = expr.args
            return And(Or(Not(eliminar_condicionais(a)), eliminar_condicionais(b)),
                       Or(Not(eliminar_condicionais(b)), eliminar_condicionais(a)))
        # Aplicar a transformação recursivamente para subexpressões
        return expr.func(*map(eliminar_condicionais, expr.args))
    
    # Eliminar implicações e bicondicionais
    expr_transformada = eliminar_condicionais(expr_sympy)
    
    return expr_transformada

def main():
    expressao_entrada = input("Digite uma expressão lógica: ")
    
    # Substituir operadores lógicos pela sintaxe reconhecida pelo SymPy
    expressao_entrada = expressao_entrada.replace("<->", "==").replace("->", ">>").replace("V", "|").replace("or", "|").replace("and", "&").replace("∧", "&")
    
    try:
        expressao_transformada = transformar_expressao(expressao_entrada)
        expressao_saida = str(expressao_transformada).replace(">>", "->").replace("<<>>", "<->").replace("|", "V").replace("&", "∧")
        print("Expressão transformada:", expressao_saida)
    except Exception as e:
        print("Erro ao processar a expressão:", e)

if __name__ == "__main__":
    main()
