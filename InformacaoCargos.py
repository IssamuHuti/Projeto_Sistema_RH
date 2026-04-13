from utils                   import *
from InformacaoDepartamentos import *


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
            
            id_dep               = InputInt( 'Digite o ID do departamento: ' )
            verificaDepartamento = BuscarDepartamento( cursor, id_dep )

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


def AlterarCadastroCargos( cursor, conexaoinformacaoRH ):
    ...


def BuscarCargo( cursor, id ):
    cursor.execute(
        "SELECT * FROM Cargos WHERE id = ?",
        ( id, )
    )
    return cursor.fetchone()

