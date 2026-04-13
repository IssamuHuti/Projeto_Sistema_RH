from utils            import *
from InformacaoCargos import *


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
        selecaoDep   = BuscarDepartamento( cursor, selecaoCargo[ Cargo.ID_DEP ] )

        descricaoFuncionario = f'{ funcionario[ Funcionario.ID ] } { funcionario[ Funcionario.NOME ] }'
        descricaoCargo       = f'{ selecaoCargo[ Cargo.ID ] } { selecaoCargo[ Cargo.NOME ] }'
        descricaoDep         = f'{ selecaoDep[ Departamento.ID ] } { selecaoDep[ Departamento.NOME ] }'

        print( f'{ descricaoFuncionario[ :40 ].ljust( 40 ) } | { descricaoCargo[ :30 ].ljust( 30 ) } | { descricaoDep[ :40 ].ljust( 40 ) } | { '{:>10.10}'.format('{:.2f}'.format( selecaoCargo[ Cargo.SALARIO ] )) }' )

    Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )

