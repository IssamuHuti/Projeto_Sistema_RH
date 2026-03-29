import os
import re
import sqlite3
from datetime import datetime, timedelta


# CONSTANTES

FUNCIONARIO_ID              = 0
FUNCIONARIO_NOME            = 1
FUNCIONARIO_CPF             = 2
FUNCIONARIO_CARGO           = 3
FUNCIONARIO_DATA_ADMISSAO   = 4
FUNCIONARIO_DATA_DEMISSAO   = 5
FUNCIONARIO_ADVERTENCIA     = 6
FUNCIONARIO_VALE_TRANSPORTE = 7
FUNCIONARIO_DEPENDENTE      = 8
FUNCIONARIO_NIVEL_ENSINO    = 9
FUNCIONARIO_CNH             = 10
FUNCIONARIO_EMAIL           = 11

CARGO_ID             = 0
CARGO_NOME           = 1
CARGO_ID_DEP         = 2
CARGO_SALARIO        = 3
CARGO_NUMERO_MAXIMO  = 4
CARGO_NECESSARIO_CNH = 5

PAGAMENTO_ID             = 0
PAGAMENTO_MES            = 1
PAGAMENTO_ANO            = 2
PAGAMENTO_ID_FUNCIONARIO = 3
PAGAMENTO_CARGO          = 4
PAGAMENTO_DEPARTAMENTO   = 5
PAGAMENTO_FALTAS         = 6
PAGAMENTO_SALARIO_PAGO   = 7

DEPARTAMENTO_ID   = 0
DEPARTAMENTO_NOME = 1

def LimparTela():
    os.system( 'cls' if os.name == 'nt' else 'clear' )

def InputInt( descricao ):
    while True:
        try:
            valor = input( descricao ) 
            if not valor.isnumeric():
                print( "Digite somente números" )
                continue

            return int( valor )
        
        except:
            print( 'Digite somente números inteiros' )

def InputStr( descricao, nTamanho ):
    while True:
        try:
            usuario = input( descricao )
            if not usuario:
                print( 'Digite um valor' )
                continue

            elif len(usuario) <= nTamanho:
                return usuario
            
            else:
                print( f'Digite até {nTamanho} de caracteres')
                input()
                continue

        except:
            print( 'O campo está limitado até ' + str( nTamanho ) + ' caracterer(s)')

def InputStrUpper( descricao, nTamanho ):
    while True:
        try:
            usuario = input( descricao )
            if not usuario:
                print( 'Digite um valor' )
                input()
                continue

            elif len(usuario) <= nTamanho:
                return usuario.upper()
            
            else:
                print( f'Digite até {nTamanho} de caracteres')
                input()
                continue

        except:
            print( 'O campo está limitado até ' + str( nTamanho ) + 'de caracteres')

def InputData( descricao ):
    while True:
        captura_data = input( descricao )
        try:
            data = datetime.strptime( captura_data, "%d%m%Y" ).date()

        except ValueError:
            print( 'Data inválida. Use o formato DDMMAAAA' )
            continue

        return data

def InputEmail( descricao ):
    while True:
        capturaEmail = input( descricao )

        if '@' not in capturaEmail or '.' not in capturaEmail.split('@')[-1]:
            print( 'Email inválido tente novamente\nO email deve posuir "@" e ".com"' )
            continue
        
        return capturaEmail

def VerificaCPF():
    while True:
        cpf = InputStr( 'CPF..:', 11 )
    
        if not len( cpf ) == 11:
            print( 'O CPF precisa conter 11 digitos' )
            input()
            continue

        if not cpf.isnumeric():
            print( 'Digite somente números' )
            input()
            continue
        
        return cpf 

def Confirmacao( texto ):
    while True:
        opcao = InputStrUpper( texto, 1 )
        if opcao == 'S':
            return True
        
        elif opcao == 'N':
            return False
        
        else:
            print( 'Digite somente [S]im ou [N]ao' )


def Main():
    conexaoinformacaoRH = sqlite3.connect( 'informacaoRH.db' )
    cursor              = conexaoinformacaoRH.cursor()

    AbreBiblioteca( cursor, conexaoinformacaoRH )

    while True:
        LimparTela()
        print( '1 - Cadastrar Funcionario' )
        print( '2 - Cadastrar Cargo' )
        print( '3 - Cadastrar Departamento' )
        print( '4 - Listar' )
        print( '5 - Rodar a folha do mês' )
        print( '6 - Relatório Folha' )
        print( '7 - Sair' )

        opcao = InputInt( 'Digite a opção desejada: ' )

        if opcao == 1:
            CadastrarNovoFuncionario( cursor, conexaoinformacaoRH )

        elif opcao == 2:
            CadastrarCargo( cursor, conexaoinformacaoRH )

        elif opcao == 3:
            CadastrarDepartamento( cursor, conexaoinformacaoRH )

        elif opcao == 4:
            Listar( cursor, conexaoinformacaoRH )

        elif opcao == 5:
            RodarFolhaMes( cursor, conexaoinformacaoRH )

        elif opcao == 6:
            RelatorioFolha( cursor, conexaoinformacaoRH )

        elif opcao == 7:
            break

        else:
            print( 'Opção inválida. Tente novamente.' )
            input()

    conexaoinformacaoRH.close()


def AbreBiblioteca( cursor, conexaoinformacaoRH ):
    cursor.execute( 
        """
        CREATE TABLE IF NOT EXISTS Funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador TEXT NOT NULL,
            cpf TEXT NOT NULL,
            id_cargo INTEGER NOT NULL,
            data_admissao DATE NOT NULL,
            data_demissao DATE,
            adivertencias INTEGER NOT NULL,
            vale_transporte TEXT NOT NULL,
            dependente INTEGER NOT NULL,
            nivel_ensino TEXT NOT NULL,
            cnh TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    cursor.execute( 
        """
        CREATE TABLE IF NOT EXISTS Cargos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo TEXT NOT NULL,
            id_departamento INTEGER NOT NULL,
            salario REAL NOT NULL,
            numero_maximo INTEGER NOT NULL,
            necessita_cnh TEXT NOT NULL
        )
        """
    )

    cursor.execute( 
        """
        CREATE TABLE IF NOT EXISTS Departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departamento TEXT NOT NULL
        )
        """
    )

    cursor.execute( 
        """
        CREATE TABLE IF NOT EXISTS Pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            id_funcionario INTEGER NOT NULL,
            id_cargo INTEGER NOT NULL,
            faltas INTEGER NOT NULL,
            salario_pago REAL NOT NULL
        )
        """
    )
    conexaoinformacaoRH.commit()


def CadastrarNovoFuncionario( cursor, conexaoinformacaoRH ):

    cursor.execute(
        "SELECT * FROM Cargos"
    )
    verificaCargo = cursor.fetchall()

    if not verificaCargo:
        print( 'Não é possível cadastrar um novo colaborar sem nenhum registro de nenhum cargo' )
        if Confirmacao( 'Deseja cadastrar um cargo(S/N)? ' ):
            CadastrarCargo( cursor, conexaoinformacaoRH )
        else:
            return 
    
    while True:
        LimparTela()
        print( '--- Cadastro de Funcionario ---' )

        colaborador = InputStr( 'Nome.: ', 40 )
        if colaborador == '0':
            return
        
        while True:
            cpf = VerificaCPF()

            if cpf == '00000000000':
                return

            cursor.execute(
                "SELECT * FROM Funcionarios WHERE cpf = ?",
                ( cpf, )
            )
            cpfCadastrado = cursor.fetchone()
            if cpfCadastrado:
                print( 'CPF já cadastrado, tente outro CPF ou digite 00000000000 para sair' )
                continue
            
            break

        while True:
            id_cargo = InputInt( 'Cargo: ' )
            if not id_cargo:
                return

            cargoCadastrado = BuscarCargo( cursor, id_cargo )
            if not cargoCadastrado:
                print( 'Digite um cargo cadastrado ou 0 para sair' )
                continue
            
            break

        data_admissao = InputData( 'Data de admissão (DDMMAAAA): ' )

        while True:
            vale_transporte = Confirmacao( 'Vale transporte(S/N): ' )
            if vale_transporte:
                vale_transporte = 'S'
            else:
                vale_transporte = 'N'

            break

        dependente   = InputInt( 'Dependentes(QTD): ' )
        nivel_ensino = InputStrUpper( 'Grau de escolaridade(F/M/S): ', 1 )

        while True:
            cnh = InputStrUpper( 'CNH: ', 1 )
            if cargoCadastrado[CARGO_NECESSARIO_CNH] == 'S':
                if cnh not in 'ABCD':
                    print('Necessário possuir CNH válida (A/B/C/D)')
                    continue
                break
            else:
                if cnh not in 'ABCDN':
                    print('Digite o tipo de carteira (A/B/C/D/N)')
                    continue
                break
        
        email = InputEmail( 'Email: ' )

        queryFuncionario = "INSERT INTO Funcionarios ( "
        queryFuncionario += "colaborador, cpf, id_cargo, data_admissao, data_demissao, adivertencias, vale_transporte, dependente, nivel_ensino, cnh, email, status"
        queryFuncionario += " ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"
        cursor.execute(
            queryFuncionario,
            ( colaborador, cpf, id_cargo, data_admissao, None, 0, vale_transporte, dependente, nivel_ensino, cnh, email, 'A' )
        )
        conexaoinformacaoRH.commit()

        if not Confirmacao( 'Deseja cadastrar novamente(S/N)? ' ):
            return


def CadastrarCargo( cursor, conexaoinformacaoRH ):

    cursor.execute(
        "SELECT * FROM Cargos"
    )
    dadosCargo = cursor.fetchall()

    while True:
        print( '--- Cadastro de Quadro de Salário ---' )

        if dadosCargo:
            print( 'Cargos da Empresa' )
            for dadoCargo in dadosCargo:
                print( f'{dadoCargo[ CARGO_ID ]} - {dadoCargo[ CARGO_NOME ]}' )

        print()
        while True:
            LimparTela()

            cargo = InputStr( 'Digite o cargo: ', 20 )
            if any( cargo.upper() == dadoCargo[ CARGO_NOME ] for dadoCargo in dadosCargo ):
                print( 'Cargo já registrado' )

                continuar = input( 'Deseja cadastrar outro cargo(S/N)? ' )
                if not continuar:
                    return
                
            elif cargo == '0':
                return
                
            else:
                break

        while True:
            id_dep  = InputInt( 'Digite o ID do departamento: ' )
            cursor.execute(
                "SELECT * FROM Departamento WHERE id = ?",
                ( id_dep, )
            )
            verificaDepartamento = cursor.fetchone()

            if not verificaDepartamento:
                cadastrar_dep = InputStr( 'Departamento não cadastrado, deseja cadastrar um novo departamento(S/N)? ', 1 )

                if cadastrar_dep:
                    CadastrarDepartamento( cursor, conexaoinformacaoRH )

                    tentarDeNovo = InputStr( 'Deseja tentar outro ID(S/N)? ', 1 )
                    if tentarDeNovo:
                        continue
                    else:
                        return

                else:
                    tentarDeNovo = InputStr( 'Deseja tentar outro ID(S/N)? ', 1 )
                    if tentarDeNovo:
                        continue
                    else:
                        return
                    
            break

        salario       = float( input( 'Digite o salário: ' ) )
        numero_maximo = InputInt( 'Digite o número máximo de funcionários para este cargo: ' )
        necessita_cnh = InputStrUpper( 'Necessita possuir CNH(S/N)? ', 1 )

        queryFuncionario = "INSERT INTO Cargos ( "
        queryFuncionario += "cargo, id_departamento, salario, numero_maximo, necessita_cnh"
        queryFuncionario += " ) VALUES ( ?, ?, ?, ?, ? )"
        cursor.execute(
            queryFuncionario,
            ( cargo, id_dep, salario, numero_maximo, necessita_cnh )
        )
        conexaoinformacaoRH.commit()

        cadastrarNovamente = Confirmacao( 'Deseja cadastrar outro cargo(S/N)? ' )
        if not cadastrarNovamente:
            break 


def CadastrarDepartamento( cursor, conexaoinformacaoRH ):
    
    cursor.execute(
        "SELECT * FROM Departamento"
    )
    listas = cursor.fetchall()

    while True:
        LimparTela()

        print( '--- Cadastro de Departamento ---' )

        if listas:
            print()
            print( 'Depatamentos da Empresa' )
            for dadoDepartamento in listas:
                print( f'{dadoDepartamento[ DEPARTAMENTO_ID ]} - {dadoDepartamento[ DEPARTAMENTO_NOME ]}' )
            print()
        
        while True:
            departamento = InputStrUpper( 'Departamento: ', 20 )
            if any( departamento == dadoDepartamento[ DEPARTAMENTO_NOME ] for dadoDepartamento in listas ):
                print( 'Departamento já registrado' )

                continuar = Confirmacao( 'Deseja cadastrar outro cargo(S/N)? ' )
                if continuar:
                    continue 
            
            break

        cursor.execute(
            "INSERT INTO Departamento ( departamento ) VALUES ( ? )",
            ( departamento, )
        )
        conexaoinformacaoRH.commit()

        print( 'Departamento cadastrado' )
        cadastrarNovamente = Confirmacao( 'Deseja cadastrar outro departamento(S/N)? ' )
        if not cadastrarNovamente:
            break


def ListarFuncionarios( cursor, conexaoinformacaoRH ):

    LimparTela()
    cursor.execute(
        "SELECT * FROM Funcionarios"
    )
    selecaoFuncionarios = cursor.fetchall()
    if not selecaoFuncionarios:
        print( 'Nenhum funcionário cadastrado' )

        cadastrarFuncionario = Confirmacao( 'Cadastrar um novo funcionário(S/N)? ' )
        if cadastrarFuncionario:
            CadastrarNovoFuncionario( cursor, conexaoinformacaoRH )
        else:
            return
        
    print( '--- Lista de Funcionarios ---' )

    for funcionario in selecaoFuncionarios:
        
        selecaoCargo = BuscarCargo( cursor, funcionario[ FUNCIONARIO_CARGO ] )

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( selecaoCargo[ CARGO_ID_DEP ], )
        )
        selecaoDep = cursor.fetchone()

        print( f'{funcionario[ FUNCIONARIO_ID ]} {funcionario[ FUNCIONARIO_NOME ]} {selecaoCargo[ CARGO_ID ]}-{selecaoCargo[ CARGO_NOME ] } {selecaoDep[ DEPARTAMENTO_ID ]}-{selecaoDep[ DEPARTAMENTO_NOME ] } {selecaoCargo[ CARGO_SALARIO ]}' )

    print()
    detalharFuncionario = Confirmacao( 'Deseja consultar algum funcionário?' )
    if not detalharFuncionario:
        return
    
    print()
    while True:
        LimparTela()
        funcionario = InputInt( 'Digite o ID do funcionário: ' )
        cursor.execute(
            "SELECT * FROM Funcionarios WHERE id = ?",
            ( funcionario, )
        )
        selecaoFuncionario = cursor.fetchone()
        if not selecaoFuncionario:
            print( 'Digite um ID existente' )
            continue

        selecaoCargo = BuscarCargo( cursor, selecaoFuncionario[ FUNCIONARIO_CARGO ] )

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( selecaoCargo[ CARGO_ID_DEP ], )
        )
        selecaoDep = cursor.fetchone()

        ImprimeInformacaoFuncionario( selecaoFuncionario, selecaoCargo, selecaoDep )
        return
    

def ListarCargos( cursor, conexaoinformacaoRH ):

    LimparTela()
    cursor.execute(
        "SELECT * FROM Cargos"
    )
    selecaoCargos = cursor.fetchall()
    if not selecaoCargos:
        print( 'Não há Cargos registrado' )
        input()
        return
    
    for cargo in selecaoCargos:

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( cargo[ CARGO_ID_DEP ], )
        )
        selecaoDep = cursor.fetchone()

        print( f'{cargo[ CARGO_ID ]}-{cargo[CARGO_NOME]} {selecaoDep[ DEPARTAMENTO_ID ]}-{selecaoDep[ DEPARTAMENTO_NOME ]} {cargo[ CARGO_SALARIO ]} {cargo[ CARGO_NECESSARIO_CNH ]} {cargo[ CARGO_NUMERO_MAXIMO ]}' )

    input()


def ListarDepartamentos( cursor, conexaoinformacaoRH ):

    cursor.execute(
        "SELECT * FROM Departamento"
    )
    selecaoDep = cursor.fetchall()
    if not selecaoDep:
        LimparTela()
        
        print( 'Não há Cargos registrado' )
        
        cadastrarDep = Confirmacao( 'Deseja cadastrar um novo Departamento(S/N)? ' )
        if cadastrarDep:
            CadastrarDepartamento( cursor, conexaoinformacaoRH )
        else:
            return
    
    LimparTela()
    print( 'Departamentos da empresa' )
    for departamento in selecaoDep:
        print( f'{departamento[ DEPARTAMENTO_ID ]} - {departamento[ DEPARTAMENTO_NOME ]}')
    
    input()


def Listar( cursor, conexaoinformacaoRH ):

    LimparTela()
    print( '--- Tipo de listagem ---' )
    print( '1 - Funcionários' )
    print( '2 - Cargos' )
    print( '3 - Departamentos' )
    opcaoListagem = InputInt( 'Listar por: ' )

    if opcaoListagem == 1:
        ListarFuncionarios( cursor, conexaoinformacaoRH )
    elif opcaoListagem == 2:
        ListarCargos( cursor, conexaoinformacaoRH )
    elif opcaoListagem == 3:
        ListarDepartamentos( cursor, conexaoinformacaoRH )
    else:
        return


def RodarFolhaMes( cursor, conexaoinformacaoRH ):

    while True:

        while True:
            LimparTela()
            print( 'Fechamento de folha' )
            mes = InputInt( 'Mês: ' )
            if mes == 0:
                return
            
            elif mes > 12:
                print( 'Digite somente de 1 a 12' )
                input()
                continue

            break
        
        ano = InputInt( 'Ano: ' )
        if not ano:
            return
        
        cursor.execute(
            "SELECT * FROM Pagamentos WHERE mes = ? AND ano = ?",
            ( mes, ano )
        )
        selecaoFechamento = cursor.fetchone()
        if selecaoFechamento:
            print( f'{mes}/{ano} já está fechado' )
            continue

        cursor.execute(
            "SELECT * FROM Funcionarios WHERE status != ?",
            ( 'D', )
        )
        selecaoFuncionarios = cursor.fetchall()
        if not selecaoFuncionarios:
            print( 'Nenhum funcionário cadastrado' )
            input()

        print('PAGAMENTO DE FOLHA' )
        for funcionario in selecaoFuncionarios:
            
            selecaoCargo = BuscarCargo( cursor, funcionario[ FUNCIONARIO_CARGO ] )

            print( f'Colaborador: {funcionario[ FUNCIONARIO_ID ]}-{funcionario[ FUNCIONARIO_NOME ]}' )
            print( f'Cargo......: {funcionario[ FUNCIONARIO_CARGO ]}-{selecaoCargo[ CARGO_NOME ]}' )
            print( f'Salario....: {selecaoCargo[ CARGO_SALARIO ]}' )
            print()

            salarioFuncionario = selecaoCargo[ CARGO_SALARIO ]

            teveFalta = Confirmacao( 'Teve falta(S/N)? ' )
            if not teveFalta:
                cursor.execute(
                    "INSERT INTO Pagamentos ( mes, ano, id_funcionario, id_cargo, faltas, salario_pago ) VALUES ( ?, ?, ?, ?, ?, ? )",
                    ( mes, ano, funcionario[ FUNCIONARIO_ID ], funcionario[ FUNCIONARIO_CARGO ], 0, salarioFuncionario )
                )
                continue

            descontoVT          = 0
            descontoFalta       = 0
            acrescimoDependente = 0

            faltas = InputInt( 'Faltas: ' )
            if faltas > 0:
                descontoFalta = salarioFuncionario / 30 * faltas 

            if funcionario[ FUNCIONARIO_VALE_TRANSPORTE ] == 'S':
                descontoVT = salarioFuncionario * 0.05
            
            if funcionario[ FUNCIONARIO_DEPENDENTE ] >= 3:
                acrescimoDependente = salarioFuncionario * 3 / 100

            elif funcionario[ FUNCIONARIO_DEPENDENTE ] > 0:
                acrescimoDependente = salarioFuncionario * funcionario[ FUNCIONARIO_DEPENDENTE ] / 100

            salarioPagar = salarioFuncionario - descontoVT - descontoFalta + acrescimoDependente

            cursor.execute(
                "INSERT INTO Pagamentos ( mes, ano, id_funcionario, id_cargo, faltas, salario_pago ) VALUES ( ?, ?, ?, ?, ?, ? )",
                ( mes, ano, funcionario[ FUNCIONARIO_ID ], funcionario[ FUNCIONARIO_CARGO ], faltas, salarioPagar )
            )

        conexaoinformacaoRH.commit()

        print( 'Fechamento de folha realizada com sucesso' )
        break


def RelatorioFolha( cursor, conexaoinformacaoRH ):

    print()


def ImprimeInformacaoFuncionario( selecaoFuncionario, selecaoCargo, selecaoDep ):
    print( f'Nome...........: {selecaoFuncionario[ FUNCIONARIO_NOME ]}' )
    print( f'CPF............: {selecaoFuncionario[ FUNCIONARIO_CPF ]}' )
    print( f'Cargo..........: {selecaoFuncionario[ FUNCIONARIO_CARGO ]} - {selecaoCargo[CARGO_NOME]}' )
    print( f'Departamento...: {selecaoCargo[ CARGO_ID_DEP ]} - {selecaoDep[DEPARTAMENTO_NOME]}' )
    print( f'CNH............: {selecaoFuncionario[ FUNCIONARIO_CNH ]}' )
    print( f'Advertencia....: {selecaoFuncionario[ FUNCIONARIO_ADVERTENCIA ]}' )
    print( f'Dependentes....: {selecaoFuncionario[ FUNCIONARIO_DEPENDENTE ]}' )
    print( f'Nivel Ensino...: {selecaoFuncionario[ FUNCIONARIO_NIVEL_ENSINO ]}' )
    print( f'Vale Transporte: {selecaoFuncionario[ FUNCIONARIO_VALE_TRANSPORTE ]}' )
    print( f'Data admissão..: {selecaoFuncionario[ FUNCIONARIO_DATA_ADMISSAO ]}' )
    print( f'Data demissão..: {selecaoFuncionario[ FUNCIONARIO_DATA_DEMISSAO ]}' )
    print( f'E-mail.........: {selecaoFuncionario[ FUNCIONARIO_EMAIL ]}' )
    input()


def BuscarCargo( cursor, id ):
    cursor.execute(
        "SELECT * FROM Cargos WHERE id = ?",
        ( id )
    )
    return cursor.fetchone()


if __name__ == "__main__":
    Main()

