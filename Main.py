import sqlite3
from datetime import datetime
from utils import LimparTela, InputStr, InputStrUpper, InputInt, InputData, InputEmail, VerificaCPF, Confirmacao, Pausar
from utils import Funcionario, Cargo, Pagamento, Departamento


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
        print( '7 - Desligar funcionário' )
        print( '8 - Sair' )

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
            DesligarFuncionario( cursor, conexaoinformacaoRH )

        elif opcao == 8:
            break

        else:
            Pausar( 'Opção inválida. Tente novamente.' )

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
                print( f'{ dadoCargo[ Cargo.ID ] } - { dadoCargo[ Cargo.NOME ] }' )

        print()
        while True:
            LimparTela()

            cargo = InputStrUpper( 'Digite o cargo: ', 20 )
            if any( cargo.upper() == dadoCargo[ Cargo.NOME ] for dadoCargo in dadosCargo ):
                Pausar( 'Cargo já registrado' )

                continuar = InputStrUpper( 'Deseja cadastrar outro cargo(S/N)? ', 1 )
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
                cadastrar_dep = Confirmacao( 'Departamento não cadastrado, deseja cadastrar um novo departamento(S/N)? ' )

                if cadastrar_dep:
                    CadastrarDepartamento( cursor, conexaoinformacaoRH )

                    tentarDeNovo = Confirmacao( 'Deseja tentar outro ID(S/N)? ' )
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

        salario       = float( InputInt( 'Digite o salário: ' ) )
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
                print( f'{ dadoDepartamento[ Departamento.ID ] } - { dadoDepartamento[ Departamento.NOME ] }' )
            print()
        
        while True:
            departamento = InputStrUpper( 'Departamento: ', 20 )
            if any( departamento == dadoDepartamento[ Departamento.NOME ] for dadoDepartamento in listas ):
                print( 'Departamento já registrado' )

                continuar = Confirmacao( 'Deseja cadastrar outro cargo(S/N)? ' )
                if continuar:
                    continue 
            
            if departamento == '0':
                return

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

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( selecaoCargo[ Cargo.ID_DEP ], )
        )
        selecaoDep = cursor.fetchone()

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
        funcionario = InputInt( 'Digite o ID do funcionário: ' )
        cursor.execute(
            "SELECT * FROM Funcionarios WHERE id = ?",
            ( funcionario, )
        )
        selecaoFuncionario = cursor.fetchone()
        if not selecaoFuncionario:
            print( 'Digite um ID existente' )
            continue

        selecaoCargo = BuscarCargo( cursor, selecaoFuncionario[ Funcionario.CARGO ] )

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( selecaoCargo[ Cargo.ID_DEP ], )
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
        Pausar( 'Não há Cargos registrado' )
        return
    
    print( '--- Lista de Cargos ---' )
    print()
    print( f'{ '{:30.30}'.format( 'CARGO' ) } | { '{:40.40}'.format( 'DEPARTAMENTO' ) } | { '{:10.10}'.format( 'SALARIO' ) } | { '{:3.3}'.format( 'CNH' ) } | { '{:3.3}'.format( 'MAX' ) }' )

    for cargo in selecaoCargos:

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( cargo[ Cargo.ID_DEP ], )
        )
        selecaoDep = cursor.fetchone()

        descricaoCargo = f'{ cargo[ Cargo.ID ] } { cargo[ Cargo.NOME ] }'
        descricaoDep   = f'{ selecaoDep[ Departamento.ID ] } { selecaoDep[ Departamento.NOME ] }'
        print( f'{ descricaoCargo[ :30 ].ljust( 30 ) } | { descricaoDep[ :40 ].ljust( 40 ) } | { '{:>10.10}'.format( '{:.2f}'.format( cargo[ Cargo.SALARIO ] ) ) } | { '{:>3.3}'.format( cargo[ Cargo.NECESSARIO_CNH ] ) } | { '{:>3.3}'.format( str( cargo[ Cargo.NUMERO_MAXIMO ] ) ) }' )

    Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )


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
    print( '--- Departamentos da Empresa ---' )
    print()
    for departamento in selecaoDep:
        descricaoDep   = f'{ departamento[ Departamento.ID ] } { departamento[ Departamento.NOME ] }'
        print( f'{ descricaoDep }' )
    
    Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )


def ListarDesligados( cursor, conexaoinformacaoRH ):
    LimparTela()
    cursor.execute(
        "SELECT * FROM Funcionarios WHERE status = ?",
        ( 'D', )
    )
    selecaoFuncionarios = cursor.fetchall()
    if not selecaoFuncionarios:
        print( 'Nenhum funcionário desligado' )
        return
        
    print( '--- Lista de Funcionarios Desligado ---' )

    print( f'{ '{:40.40}'.format( 'FUNCIONARIO' ) } | { '{:30.30}'.format( 'CARGO' ) } | { '{:40.40}'.format( 'DEPARTAMENTO' ) } | { '{:10.10}'.format( 'SALARIO' ) }' )
    for funcionario in selecaoFuncionarios:
    
        selecaoCargo = BuscarCargo( cursor, funcionario[ Funcionario.CARGO ] )

        cursor.execute(
            "SELECT * FROM Departamento WHERE id = ?",
            ( selecaoCargo[ Cargo.ID_DEP ], )
        )
        selecaoDep = cursor.fetchone()

        descricaoFuncionario = f'{ funcionario[ Funcionario.ID ] } { funcionario[ Funcionario.NOME ] }'
        descricaoCargo       = f'{ selecaoCargo[ Cargo.ID ] } { selecaoCargo[ Cargo.NOME ] }'
        descricaoDep         = f'{ selecaoDep[ Departamento.ID ] } { selecaoDep[ Departamento.NOME ] }'

        print( f'{ descricaoFuncionario[ :40 ].ljust( 40 ) } | { descricaoCargo[ :30 ].ljust( 30 ) } | { descricaoDep[ :40 ].ljust( 40 ) } | { '{:>10.10}'.format('{:.2f}'.format( selecaoCargo[ Cargo.SALARIO ] )) }' )

    Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )


def Listar( cursor, conexaoinformacaoRH ):

    while True:
        LimparTela()
        print( '--- Tipo de listagem ---' )
        print( '1 - Funcionários Ativos' )
        print( '2 - Cargos' )
        print( '3 - Departamentos' )
        print( '4 - Funcionários Desligados' )
        print( '0 - Sair' )
        opcaoListagem = InputInt( 'Listar por: ' )

        if opcaoListagem == 1:
            ListarFuncionarios( cursor, conexaoinformacaoRH )
        elif opcaoListagem == 2:
            ListarCargos( cursor, conexaoinformacaoRH )
        elif opcaoListagem == 3:
            ListarDepartamentos( cursor, conexaoinformacaoRH )
        elif opcaoListagem == 4:
            ListarDesligados( cursor, conexaoinformacaoRH )
        elif opcaoListagem == 0:
            return
        else:
            Pausar( 'Digite somente as opções acima!' )


def RodarFolhaMes( cursor, conexaoinformacaoRH ):

    while True:

        while True:
            LimparTela()
            print( 'Fechamento de folha' )
            mes = InputInt( 'Mês: ' )
            if not mes:
                return
            
            elif mes > 12:
                Pausar( 'Digite somente de 1 a 12' )
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
            Pausar( f'{ mes }/{ ano } já está fechado' )
            continue

        cursor.execute(
            "SELECT * FROM Funcionarios WHERE status != ?",
            ( 'D', )
        )
        selecaoFuncionarios = cursor.fetchall()
        if not selecaoFuncionarios:
            Pausar( 'Nenhum funcionário cadastrado' )
            return

        print('PAGAMENTO DE FOLHA' )
        for funcionario in selecaoFuncionarios:
            
            selecaoCargo = BuscarCargo( cursor, funcionario[ Funcionario.CARGO ] )

            print( f'Colaborador: { funcionario[ Funcionario.ID ] }-{ funcionario[ Funcionario.NOME ] }' )
            print( f'Cargo......: { funcionario[ Funcionario.CARGO ] }-{ selecaoCargo[ Cargo.NOME ] }' )
            print( f'Salario....: { selecaoCargo[ Cargo.SALARIO ] }' )
            print()

            salarioFuncionario = selecaoCargo[ Cargo.SALARIO ]

            teveFalta = Confirmacao( 'Teve falta(S/N)? ' )
            if not teveFalta:
                cursor.execute(
                    "INSERT INTO Pagamentos ( mes, ano, id_funcionario, id_cargo, faltas, salario_pago ) VALUES ( ?, ?, ?, ?, ?, ? )",
                    ( mes, ano, funcionario[ Funcionario.ID ], funcionario[ Funcionario.CARGO ], 0, salarioFuncionario )
                )
                continue
            descontoVT          = 0
            descontoFalta       = 0
            acrescimoDependente = 0

            faltas = InputInt( 'Faltas: ' )
            if faltas > 0:
                descontoFalta = salarioFuncionario / 30 * faltas 

            if funcionario[ Funcionario.VALE_TRANSPORTE ] == 'S':
                descontoVT = salarioFuncionario * 0.05
            
            if funcionario[ Funcionario.DEPENDENTE ] >= 3:
                acrescimoDependente = salarioFuncionario * 3 / 100

            elif funcionario[ Funcionario.DEPENDENTE ] > 0:
                acrescimoDependente = salarioFuncionario * funcionario[ Funcionario.DEPENDENTE ] / 100

            dataAdmissao = datetime.strptime( funcionario[ Funcionario.DATA_ADMISSAO ], '%Y-%m-%d' )
            tempoDeServico = ( datetime.now() - dataAdmissao ).days // 364.25 // 5
            acrescimoPorTempo = salarioFuncionario * ( 0.05 * tempoDeServico )

            salarioPagar = salarioFuncionario - descontoVT - descontoFalta + acrescimoDependente + acrescimoPorTempo

            cursor.execute(
                "INSERT INTO Pagamentos ( mes, ano, id_funcionario, id_cargo, faltas, salario_pago ) VALUES ( ?, ?, ?, ?, ?, ? )",
                ( mes, ano, funcionario[ Funcionario.ID ], funcionario[ Funcionario.CARGO ], faltas, salarioPagar )
            )

        conexaoinformacaoRH.commit()

        Pausar( 'Fechamento de folha realizada com sucesso' )
        break


def RelatorioFolha( cursor, conexaoinformacaoRH ):

    LimparTela()
    cursor.execute(
        "SELECT * FROM Pagamentos"
    )
    verificaPagamento = cursor.fetchall()

    if not verificaPagamento:
        Pausar( 'Não foi encontrado nenhum registro de pagamento realizado' )
        return

    print( '--- Relatorio de Folha mensal ---' )
    print()

    mes = InputInt( 'Digite o mês: ' )
    if not mes:
        return 

    ano = InputInt( 'Digite o ano: ' )
    if not ano:
        return 
    
    cursor.execute(
        "SELECT * FROM Pagamentos WHERE mes = ? and ano = ?",
        ( mes, ano )
    )
    verificaPagamentoRealizados = cursor.fetchall()

    if not verificaPagamentoRealizados:
        Pausar( 'Não foi encontrado nenhum pagamento realizado no filtro selecionado' )
        return
    
    print( f'Pagamento Folha - { mes }/{ ano }' )
    totalPagamento = 0

    print( 'PERIODO | ' + '{:41.41}'.format( 'COLABORADOR' ) + '| FALTAS |  PAGAMENTO' )
    for pagamento in verificaPagamentoRealizados:

        funcionario    = pagamento[ Pagamento.ID_FUNCIONARIO ]
        salario        = pagamento[ Pagamento.SALARIO_PAGO ]
        totalPagamento += pagamento[ Pagamento.SALARIO_PAGO ]

        cursor.execute(
            "SELECT * FROM Funcionarios WHERE id = ?",
            ( funcionario, )
        )
        verificaFuncionario = cursor.fetchone()
        if not verificaFuncionario:
            continue

        identificacaoFuncionario = f'{ str( funcionario ) }-{ verificaFuncionario[ Funcionario.NOME ] }'
        print( f'{ str( mes ).zfill( 2 ) }/{ str( ano ).zfill( 4 ) } | { identificacaoFuncionario[ :40 ].ljust( 40 ) } | { '{:>6.6}'.format( str( pagamento[ Pagamento.FALTAS ] ) ) } | { '{:>10.10}'.format( '{:.2f}'.format( salario ) ) } ' )

    print()
    Pausar( f'Total pago: { '{:.2f}'.format( totalPagamento ) }' )


def ImprimeInformacaoFuncionario( selecaoFuncionario, selecaoCargo, selecaoDep ):
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
    
    # Criar opção para alterar dados do funcinário
    Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )


def DesligarFuncionario( cursor, conexaoinformacaoRH ):
    

    while True:

        cursor.execute(
            "SELECT * FROM Funcionarios WHERE status != ?",
            ( 'D', )
        )
        verificaAtivos = cursor.fetchall()

        if not verificaAtivos:
            Pausar( 'Não há nenhum funcionário ativo para desligar' )
            return
        
        LimparTela()

        print( '--- Desligamento de Funcionário ---' )
        for funcionario in verificaAtivos:
            print( f'{ funcionario[ Funcionario.ID ] } - { funcionario[ Funcionario.NOME ] }' )

        print()
        selecaoDesligamento = InputInt( 'Digite o ID do Colaborador a desligar: ' )
        if not selecaoDesligamento:
            return
        
        dadosColaborador = next(
                                    ( colaborador for colaborador in verificaAtivos if colaborador[ Funcionario.ID ] == selecaoDesligamento ),
                                    None
                                )
        if not dadosColaborador:
            print( 'Não há nenhum colaborador com esse ID ativo' )

            opcao = Confirmacao( 'Deseja continuar o desligamento de algum colaborador(S/N)? ' )
            if not opcao:
                break
            else:
                continue
        
        dadosCargo = BuscarCargo( cursor, dadosColaborador[ Funcionario.CARGO ] )

        print( f'Colaborador..: { dadosColaborador[ Funcionario.NOME ] }' )
        print( f'Cargo........: { dadosColaborador[ Funcionario.CARGO ] } - { dadosCargo[ Cargo.NOME ] }' )
        print( f'Data admissão: { dadosColaborador[ Funcionario.DATA_ADMISSAO ] }' )
        print()
        
        confirmaDesligamento = Confirmacao( 'Deseja realmente desligar o colaborador(S/N)? ' )
        if not confirmaDesligamento:
            Pausar( 'Desligamento cancelado!' )
            continue

        cursor.execute(
            "UPDATE Funcionarios SET status = ? WHERE id = ?",
            ( 'D', selecaoDesligamento )
        )
        conexaoinformacaoRH.commit()


def BuscarCargo( cursor, id ):
    cursor.execute(
        "SELECT * FROM Cargos WHERE id = ?",
        ( id, )
    )
    return cursor.fetchone()


if __name__ == "__main__":
    Main()

