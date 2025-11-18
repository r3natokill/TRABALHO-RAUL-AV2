# Importa o módulo socket
from socket import *
import sys # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverPort = 6789 # Define a porta
serverSocket.bind(('', serverPort)) # Associa o socket ao endereço e porta
serverSocket.listen(1) # Começa a escutar por conexões (máximo de 1 na fila)

while True:
    #Estabelece a conexão
    print('Ready to serve...')
    # Esta é a linha que estava com erro (agora corrigida)
    connectionSocket, addr = serverSocket.accept() # Aceita a conexão do cliente
    
    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode() # Recebe até 1024 bytes e decodifica
        
        # Se a mensagem estiver vazia (ex: conexão fechada pelo cliente), ignora
        if not message:
            connectionSocket.close()
            continue
            
        filename = message.split()[1]
        f = open(filename[1:]) # Abre o arquivo requisitado (remove a barra '/')
        
        outputdata = f.read() # Lê o conteúdo completo do arquivo
        
        # Envia a linha de status do cabeçalho HTTP
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode()) # Linha em branco essencial
        
        # Envia o conteúdo do arquivo ao cliente
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        #Fecha a conexão com o cliente
        connectionSocket.close()
        
    except IOError:
        # Envia mensagem de erro 404 se o arquivo não for encontrado
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        
        #Fecha o socket do cliente
        connectionSocket.close()

    except IndexError:
        # Lida com requisições vazias ou malformadas
        print("Recebida requisição malformada.")
        connectionSocket.close()


serverSocket.close()
sys.exit() # Encerra o programa