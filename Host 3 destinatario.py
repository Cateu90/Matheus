import os


def criar_pasta(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"Pasta '{caminho}' criada.")
    else:
        print(f"Pasta '{caminho}' já existe.")


def criar_arquivo_configuracoes(caminho):
    filename = os.path.join(caminho, 'netsettings.host.txt')
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("ipv4\n")
            f.write("address 192.168.5.100\n")
            f.write("netmask 255.255.255.0\n")
            f.write("gateway 192.168.5.254\n")
        print(f"Arquivo '{filename}' criado com configurações padrão.")
    else:
        print(f"Arquivo '{filename}' já existe.")


def solicitar_informacoes_usuario(caminho):
    filename = os.path.join(caminho, 'netsettings.host.txt')
    print("Por favor, insira as informações de rede:")
    ipv4_address = input("Endereço IPv4: ")
    netmask = input("Máscara de sub-rede: ")
    gateway = input("Gateway: ")

    with open(filename, 'w') as f:
        f.write("ipv4\n")
        f.write(f"address {ipv4_address}\n")
        f.write(f"netmask {netmask}\n")
        f.write(f"gateway {gateway}\n")
    print(f"Informações de rede salvas em '{filename}'.")


def solicitar_cabecalho_pacote():
    print("Por favor, insira o cabeçalho do pacote em hexadecimal:")
    cabecalho_hex = input("Cabeçalho do pacote: ")
    filename = 'rpacket.txt'
    with open(filename, 'w') as f:
        f.write(f"O cabeçalho do pacote em hexadecimal é: {cabecalho_hex}\n")

    return bytes.fromhex(cabecalho_hex)

def ler_configuracoes(caminho):
    print("Lendo configurações do arquivo 'netsettings.host.txt'...")
    config = {}
    filename = os.path.join(caminho, 'netsettings.host.txt')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith('ipv4') or line.startswith('ipv6') or line.startswith('mac'):
                    current_section = line.strip()
                    config[current_section] = {}
                elif line.startswith('address') or line.startswith('netmask') or line.startswith('gateway'):
                    key, value = line.split()[0], line.split()[1]
                    config[current_section][key] = value
        print("Configurações lidas com sucesso.")
        return config
    else:
        print(f"O arquivo {filename} não foi encontrado. Fornecendo automaticamente as informações.")
        return None


def verificar_versao(ip_packet):
    print("Verificando versão do IP...")
    version = ip_packet[0] >> 4  
    if version == 4:
        print("Versão do IP: IPv4")
        return 'IPv4'
    elif version == 6:
        print("Versão do IP: IPv6")
        return 'IPv6'
    else:
        print("Versão do IP inválida. Descartando pacote.")
        return None


def calcular_checksum(header):
    print("Calculando checksum do cabeçalho IPv4...")
    checksum = 0
    for i in range(0, len(header), 2):
        word = (header[i] << 8) + header[i + 1]
        checksum += word
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    resultado = (~checksum) & 0xffff
    print(f"Checksum calculado: {resultado}")
    return resultado


def verificar_integridade(header):
    print("Verificando integridade do cabeçalho IPv4...")
    checksum_received = (header[10] << 8) + header[11]
    checksum_calculated = calcular_checksum(header)
    if checksum_received == checksum_calculated:
        print("Verificação de integridade: Cabeçalho IPv4 íntegro.")
        return True
    else:
        print("Verificação de integridade: Cabeçalho IPv4 corrompido. Descartando pacote.")
        return False


def verificar_ip_destino(ip_packet, host_ipv4):
    print("Verificando IP de destino...")
    ip_destino = ip_packet[16:20]
    ip_destino_str = '.'.join(map(str, ip_destino))
    if ip_destino_str == host_ipv4:
        print("Endereço de destino válido.")
        return True
    else:
        print(f"Endereço de destino inválido ({ip_destino_str}). Descartando pacote.")
        return False


def identificar_protocolo_entregar_carga(ip_packet):
    print("Identificando protocolo...")
    protocolo = ip_packet[9]
    if protocolo == 1:
        print("Protocolo identificado: ICMP. Entregando carga útil como 'message.txt'.")
        return 'ICMP'
    elif protocolo == 6:
        print("Protocolo identificado: TCP. Entregando carga útil como 'segment.txt'.")
        return 'TCP'
    elif protocolo == 17:
        print("Protocolo identificado: UDP. Entregando carga útil como 'segment.txt'.")
        return 'UDP'
    else:
        print(f"Protocolo desconhecido ({protocolo}). Não é possível entregar carga útil.")
        return None


def processar_pacote(ip_packet, host_ipv4):
    print("Processando pacote de rede...")
    versao = verificar_versao(ip_packet)
    if versao == 'IPv6':
        print("Pacote IPv6 detectado. Descartando pacote...")
        os.remove('rpacket.txt')
        print("Pacote descartado.")
        return

    elif versao == 'IPv4':
        header = ip_packet[:20]  
        integridade = verificar_integridade(header)
        if not integridade:
            os.remove('rpacket.txt')
            print("PDU descartada devido à integridade comprometida.")
            return

        ip_valido = verificar_ip_destino(ip_packet, host_ipv4)
        if not ip_valido:
            os.remove('rpacket.txt')
            print("PDU descartada devido ao endereço de destino inválido.")
            return

        protocolo = identificar_protocolo_entregar_carga(ip_packet)
        if protocolo:
            caminho_pasta = 'IP'
            criar_pasta(caminho_pasta)
            with open(f'{caminho_pasta}/rpacket.txt', 'w') as f:
                f.write(f"Endereço IPv4: {host_ipv4}\n")
                f.write(f"Máscara de sub-rede: {ip_packet[1]}.{ip_packet[2]}.{ip_packet[3]}.{ip_packet[4]}\n")
                f.write(f"Gateway: {ip_packet[5]}.{ip_packet[6]}.{ip_packet[7]}.{ip_packet[8]}\n")
            print(f"Informações de rede armazenadas em '{caminho_pasta}/rpacket.txt'.")

            with open(f'{caminho_pasta}/{protocolo.lower()}_payload.txt', 'wb') as f:
                f.write(ip_packet[20:])  
            print(f"Carga útil entregue como '{caminho_pasta}/{protocolo.lower()}_payload.txt'.")

    print("\nPDU Processada!\n\n")
    resposta = input("Há mais alguma PDU a ser processada? (s/n): ")
    if resposta.lower() == 's':
        os.system('clear')
        main()


def main():
    caminho_pasta = 'IP'
    criar_pasta(caminho_pasta)
    criar_arquivo_configuracoes(caminho_pasta)
    solicitar_informacoes_usuario(caminho_pasta)
    config = ler_configuracoes(caminho_pasta)
    if config and 'ipv4' in config and 'address' in config['ipv4']:
        host_ipv4 = config['ipv4']['address']
        
        ip_packet = solicitar_cabecalho_pacote()
        processar_pacote(ip_packet, host_ipv4)

if __name__ == "__main__":
    main()
