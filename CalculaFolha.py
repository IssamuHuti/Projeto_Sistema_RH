from utils            import *
from InformacaoCargos import *
from datetime         import datetime


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


