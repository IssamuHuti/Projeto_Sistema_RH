class Funcionario:
    ID              = 0
    NOME            = 1
    CPF             = 2
    CARGO           = 3
    DATA_ADMISSAO   = 4
    DATA_DEMISSAO   = 5
    ADVERTENCIA     = 6
    VALE_TRANSPORTE = 7
    DEPENDENTE      = 8
    NIVEL_ENSINO    = 9
    CNH             = 10
    EMAIL           = 11

class Cargo:
    ID             = 0
    NOME           = 1
    ID_DEP         = 2
    SALARIO        = 3
    NUMERO_MAXIMO  = 4
    NECESSARIO_CNH = 5

class Pagamento:
    ID             = 0
    MES            = 1
    ANO            = 2
    ID_FUNCIONARIO = 3
    CARGO          = 4
    FALTAS         = 5
    SALARIO_PAGO   = 6

class Departamento:
    ID   = 0
    NOME = 1
    