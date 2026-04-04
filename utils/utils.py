import os
import re
from datetime import datetime

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
        
        except ValueError:
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
                input( f'Digite até {nTamanho} de caracteres' )
                continue

        except ValueError:
            print( 'O campo está limitado até ' + str( nTamanho ) + ' caracterer(s)')

def InputStrUpper( descricao, nTamanho ):
    while True:
        try:
            usuario = input( descricao )
            if not usuario:
                input( 'Digite um valor' )
                continue

            elif len(usuario) <= nTamanho:
                return usuario.upper()
            
            else:
                input( f'Digite até { nTamanho } de caracteres' )
                continue

        except ValueError:
            print( 'O campo está limitado até ' + str( nTamanho ) + 'de caracteres')

def InputData( descricao ):
    while True:
        captura_data = InputStr( descricao, 10 )
        try:
            data = datetime.strptime( captura_data, "%d%m%Y" ).date()
            return data.strftime('%Y-%m-%d')

        except ValueError:
            print( 'Data inválida. Use o formato DDMMAAAA' )
            continue

def InputEmail( descricao ):
    while True:
        capturaEmail = InputStr( descricao, 40 )

        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', capturaEmail) or '.com' not in capturaEmail.split('@')[-1]:
            print( 'Email inválido tente novamente\nO email deve posuir "@" e ".com"' )
            continue
        
        return capturaEmail

def VerificaCPF():
    while True:
        cpf = InputStr( 'CPF..:', 11 )
    
        if not len( cpf ) == 11:
            input( 'O CPF precisa conter 11 digitos' )
            continue

        if not cpf.isnumeric():
            input( 'Digite somente números' )
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

def Pausar( texto ):
    print()
    input( texto )
    return 
