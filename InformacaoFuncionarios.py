from utils                import *
from InformacaoCargos     import *
from InformacaoDesligados import *


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

        colaborador = InputStrUpper( 'Nome.: ', 40 )
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
                Pausar( 'CPF já cadastrado, tente outro CPF ou digite 00000000000 para sair' )
                continue
            
            break

        while True:

            id_cargo = InputInt( 'Cargo: ' )
            if not id_cargo:
                return

            cargoCadastrado = BuscarCargo( cursor, id_cargo )
            if not cargoCadastrado:
                Pausar( 'Digite um cargo cadastrado ou 0 para sair' )
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
            if cargoCadastrado[ Cargo.NECESSARIO_CNH ] == 'S':
                if cnh not in 'ABCD':
                    Pausar( 'Necessário possuir CNH válida (A/B/C/D)' )
                    continue
                break
            else:
                if cnh not in 'ABCDN':
                    Pausar( 'Digite o tipo de carteira (A/B/C/D/N)' )
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
        

def Listar( cursor, conexaoinformacaoRH ):
    
    while True:

        LimparTela()

        print( '--- Listar Funcionários ---' )
        print( '1 - Ativos' )
        print( '2 - Inativos' )
        print( '0 - Sair' )

        opcaoLista = InputInt( 'Listar: ' )

        if opcaoLista == 1:
            ListarFuncionarios( cursor, conexaoinformacaoRH )

        if opcaoLista == 2:
            ListarDesligados( cursor, conexaoinformacaoRH )

        elif opcaoLista == 0:
            break
        
        else:
            Pausar( 'Digite somente as opções acima!' )


def ListarFuncionarios( cursor, conexaoinformacaoRH ):

    LimparTela()
    cursor.execute(
        "SELECT * FROM Funcionarios WHERE status != ?",
        ( 'D', )
    )
    selecaoFuncionarios = cursor.fetchall()
    if not selecaoFuncionarios:
        print( 'Nenhum funcionário cadastrado' )

        cadastrarFuncionario = Confirmacao( 'Cadastrar um novo funcionário(S/N)? ' )
        if cadastrarFuncionario:
            CadastrarNovoFuncionario( cursor, conexaoinformacaoRH )
        else:
            return
        
    print( '--- Lista de Funcionarios Ativos ---' )
    print()
    print( f'{ '{:40.40}'.format( 'FUNCIONARIO' ) } | { '{:30.30}'.format( 'CARGO' ) } | { '{:40.40}'.format( 'DEPARTAMENTO' ) } | { '{:10.10}'.format( 'SALARIO' ) }' )

    for funcionario in selecaoFuncionarios:
        
        selecaoCargo = BuscarCargo( cursor, funcionario[ Funcionario.CARGO ] )
        selecaoDep   = BuscarDepartamento( cursor, selecaoCargo[ Cargo.ID_DEP ] )

        descricaoFuncionario = f'{ funcionario[ Funcionario.ID ] } { funcionario[ Funcionario.NOME ] }'
        descricaoCargo       = f'{ selecaoCargo[ Cargo.ID ] } { selecaoCargo[ Cargo.NOME ] }'
        descricaoDep         = f'{ selecaoDep[ Departamento.ID ] } { selecaoDep[ Departamento.NOME ] }'
        print( f'{ descricaoFuncionario[ :40 ].ljust( 40 ) } | { descricaoCargo[ :30 ].ljust( 30 ) } | { descricaoDep[ :40 ].ljust( 40 ) } | { '{:>10.10}'.format('{:.2f}'.format( selecaoCargo[ Cargo.SALARIO ] )) }' )

    print()
    detalharFuncionario = Confirmacao( 'Deseja consultar algum funcionário(S/N)? ' )
    if not detalharFuncionario:
        return
    
    print()
    while True:
        LimparTela()

        funcionario        = InputInt( 'Digite o ID do funcionário: ' )
        selecaoFuncionario = BuscarFuncionario( cursor, funcionario, 'A' )

        if not selecaoFuncionario:
            print( 'Digite um ID existente' )
            continue

        selecaoCargo = BuscarCargo( cursor, selecaoFuncionario[ Funcionario.CARGO ] )
        selecaoDep   = BuscarDepartamento( cursor, selecaoCargo[ Cargo.ID_DEP ] )

        ImprimeInformacaoFuncionario( selecaoFuncionario, selecaoCargo, selecaoDep, cursor, conexaoinformacaoRH )

        if Confirmacao( 'Deseja alterar informacao cadastrado(S/N)? ' ):
            AlterarCadastroFuncionarios( cursor, conexaoinformacaoRH )

        Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )

        return
    

def ImprimeInformacaoFuncionario( selecaoFuncionario, selecaoCargo, selecaoDep, cursor, conexaoinformacaoRH ):
    print( f'Nome...........: { selecaoFuncionario[ Funcionario.NOME ] }' )
    print( f'CPF............: { selecaoFuncionario[ Funcionario.CPF ] }' )
    print( f'Cargo..........: { selecaoFuncionario[ Funcionario.CARGO ] } - { selecaoCargo[ Cargo.NOME ] }' )
    print( f'Departamento...: { selecaoCargo[ Cargo.ID_DEP ] } - { selecaoDep[ Departamento.NOME ] }' )
    print( f'CNH............: { selecaoFuncionario[ Funcionario.CNH ] }' )
    print( f'Advertencia....: { selecaoFuncionario[ Funcionario.ADVERTENCIA ] }' )
    print( f'Dependentes....: { selecaoFuncionario[ Funcionario.DEPENDENTE ] }' )
    print( f'Nivel Ensino...: { selecaoFuncionario[ Funcionario.NIVEL_ENSINO ] }' )
    print( f'Vale Transporte: { selecaoFuncionario[ Funcionario.VALE_TRANSPORTE ] }' )
    print( f'Data admissão..: { selecaoFuncionario[ Funcionario.DATA_ADMISSAO ] }' )
    print( f'Data demissão..: { selecaoFuncionario[ Funcionario.DATA_DEMISSAO ] }' )
    print( f'E-mail.........: { selecaoFuncionario[ Funcionario.EMAIL ] }' )


def AlterarCadastroFuncionarios( cursor, conexaoinformacaoRH ):
    ...


def BuscarFuncionario( cursor, id, status ):
    cursor.execute(
        "SELECT * FROM Funcionarios WHERE id = ? AND status = ?",
        ( id, status )
    )
    return cursor.fetchone()

