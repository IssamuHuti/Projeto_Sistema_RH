from utils import *
from prompt_toolkit import prompt

def CadastrarDepartamento( cursor, conexaoinformacaoRH ):
    

    while True:

        cursor.execute(
            "SELECT * FROM Departamento"
        )
        listas = cursor.fetchall()

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
            "INSERT INTO Departamento ( nome ) VALUES ( ? )",
            ( departamento, )
        )
        conexaoinformacaoRH.commit()

        print( 'Departamento cadastrado' )
        cadastrarNovamente = Confirmacao( 'Deseja cadastrar outro departamento(S/N)? ' )
        if not cadastrarNovamente:
            break


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


def AlterarCadastroDepartamentos( cursor, conexaoinformacaoRH ):

    while True:

        ListarDepartamentos( cursor, conexaoinformacaoRH )

        print()
        selecaoDep = InputInt( 'Selecione o item a alterar informação: ' )

        if selecaoDep == 0:
            break

        depSelecionada = BuscarDepartamento( cursor, selecaoDep )

        if not depSelecionada:
            Pausar( 'O ID informado não está cadastrado' )

        id_dep   = depSelecionada[ Departamento.ID   ]
        nome_dep = depSelecionada[ Departamento.NOME ]

        print()
        print( f'ID..: { id_dep }' )

        novo_nome = prompt( 'Nome: ', default=nome_dep ).upper()

        cursor.execute(
            "UPDATE Departamento SET nome = ? WHERE id = ?",
            ( novo_nome, id_dep )
        )
        conexaoinformacaoRH.commit()

        Pausar( 'Alteração realizada com sucesso!' )


def BuscarDepartamento( cursor, id ):
    cursor.execute(
        "SELECT * FROM Departamento WHERE id = ?",
        ( id, )
    )
    return cursor.fetchone()