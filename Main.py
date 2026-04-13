import sqlite3

from utils                   import *
from CalculaFolha            import *
from InformacaoCargos        import *
from InformacaoDepartamentos import *
from InformacaoFuncionarios  import *
from InformacaoDesligados    import *


def Main():
    conexaoinformacaoRH = sqlite3.connect( 'informacaoRH.db' )
    cursor              = conexaoinformacaoRH.cursor()

    AbreBiblioteca( cursor, conexaoinformacaoRH )

    while True:
        LimparTela()

        print( 'SISTEMA DE FOLHA' )
        print()
        print( '1 - FUNCIONARIO' )
        print( '2 - CARGO' )
        print( '3 - DEPARTAMENTO' )
        print( '4 - CALCULA FOLHA' )
        print( '5 - SAIR' )

        print()
        opcao = InputInt( 'Digite a opção desejada: ' )

        if opcao == 1:
            MenuFuncionario( cursor, conexaoinformacaoRH )

        elif opcao == 2:
            MenuCargo( cursor, conexaoinformacaoRH )

        elif opcao == 3:
            MenuDepartamento( cursor, conexaoinformacaoRH )

        elif opcao == 4:
            MenuCalculaFolha( cursor, conexaoinformacaoRH )

        elif opcao == 5:
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
            nome TEXT NOT NULL
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


def MenuFuncionario( cursor, conexaoinformacaoRH ):

    while True:
        LimparTela()

        print( '--- Menu Funcionario ---' )
        print( '1 - Cadastrar' )
        print( '2 - Listar' )
        print( '3 - Alterar Informação' )
        print( '4 - Desligar' )
        print( '0 - Sair' )

        print()
        opcaoListagem = InputInt( 'Escolher opção: ' )

        if opcaoListagem == 1:
            CadastrarNovoFuncionario( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 2:
            Listar( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 3:
            AlterarCadastroFuncionarios( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 4:
            DesligarFuncionario( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 0:
            break
        
        else:
            Pausar( 'Digite somente as opções acima!' )


def MenuCargo( cursor, conexaoinformacaoRH ):

    while True:
        LimparTela()

        print( '--- Menu Cargo ---' )
        print( '1 - Cadastrar' )
        print( '2 - Listar' )
        print( '3 - Alterar Informação' )
        print( '0 - Sair' )

        print()
        opcaoListagem = InputInt( 'Escolher opção: ' )

        if opcaoListagem == 1:
            CadastrarCargo( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 2:
            ListarCargos( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 3:
            AlterarCadastroCargos( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 0:
            break
        
        else:
            Pausar( 'Digite somente as opções acima!' )


def MenuDepartamento( cursor, conexaoinformacaoRH ):

    while True:
        LimparTela()

        print( '--- Menu Departamento ---' )
        print( '1 - Cadastrar' )
        print( '2 - Listar' )
        print( '3 - Alterar Informação' )
        print( '0 - Sair' )

        print()
        opcaoListagem = InputInt( 'Escolher opção: ' )

        if opcaoListagem == 1:
            CadastrarDepartamento( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 2:
            ListarDepartamentos( cursor, conexaoinformacaoRH )
            Pausar( 'Tecle algum teclado para sair voltar ao Menu...' )

        elif opcaoListagem == 3:
            AlterarCadastroDepartamentos( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 0:
            break
        
        else:
            Pausar( 'Digite somente as opções acima!' )


def MenuCalculaFolha( cursor, conexaoinformacaoRH ):

    while True:
        LimparTela()

        print( '--- Menu Calculo Folha ---' )
        print( '1 - Rodar Folha' )
        print( '2 - Relatorio' )
        print( '0 - Sair' )

        print()
        opcaoListagem = InputInt( 'Escolher opção: ' )

        if opcaoListagem == 1:
            RodarFolhaMes( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 2:
            RelatorioFolha( cursor, conexaoinformacaoRH )

        elif opcaoListagem == 0:
            break

        else:
            Pausar( 'Digite somente as opções acima!' )


if __name__ == "__main__":
    Main()

