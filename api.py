import requests
import json
import argparse
#Acima estamos importando as bibliotecas de comandos prontos que vamos utilizar no codigo abaixo

#abaixo criei a variavel url, para que não precisamos ter que ficar repetindo a url dentro das requests, e tambem deixar a linha menos comprida.
url = 'https://api.us-2.crowdstrike.com'

##Função para Gerar o Token de sessão -----------------------------
def TokenAuth():
    #cabeçalho da requisição web:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    #body da requisição web:
    data = {
        'client_id': 'id da api',
        'client_secret': 'secret da api',
    }

    #realiza a rquisição web com o metodo post, passando os parametros necessarios:
    response = requests.post(url+'/oauth2/token', headers=headers, data=data)

    #converte a resposta recebida para variavel response:
    response = response.json()

    #dentro da resposta obtida, filtrar somente pelo campo acess_token, pois só queremos o token e nada mais:
    token_auth = response['access_token']

    #return serve para entregar o valor da variavel token_auth quando alguem solicitar a função TokenAuth():
    return(token_auth)

#Estou trazendo o resultado da função TokenAuth() para dentro da variavel token_auth, dessa forma, posso utilizar o token de sessão nas urls de forma encurtada, sem precisar ficar uma linha gigante:
#Essa variavesl será utilizada em todas as funções que precisar do cabeçalho 'authorization'
token_auth = TokenAuth()

#Função para Buscar todos os hosts que existem na console pelo Device_ID:  -----------------------------
def listaDeHosts():
    headers = {
    'accept': 'application/json',
    'authorization': 'Bearer ' + token_auth,
    }
    #Nessa request. estou solicitando todos os hosts que existem na console:
    resposta1 = requests.get(url+"/devices/queries/devices/v1", headers=headers)
    resposta2 = resposta1.json()
    host_ID = resposta2["resources"]

    #abaixo estou transformando a resposta no formato de apresentação do JSON e jogando para variavel saida_json
    saida_json = json.dumps(host_ID, indent=2)

    #apresentando o resultado na tela:
    print(saida_json)

    #return serve para entregar o valor da variavel host_ID quando alguem solicitar a função listaDeHosts():
    return(host_ID)

#Busca todos os hosts que existem na console pelo Device_ID utilizando filtro de busca:  -----------------------------
def listaDeWorkstation():
    Header = {
        'accept': 'application/json',
        'authorization': 'Bearer ' + token_auth,
        'Content-Type': 'application/json',
    }
    #Nessa request. estou solicitando todos os workstations que existem na console:
    #Perceba que na URL estou passando o parametro "filter=product_type_desc:'Workstation'"
    RespostaHostsDetalhados = requests.get(url+"/devices/queries/devices/v1?filter=product_type_desc:'Workstation'", headers=Header)

    #as linhas abaixo são os tratamentos de dados igual as funções que passamos a cima:
    ConvertHostDetalhado = RespostaHostsDetalhados.json()
    RespostaHostsDetalhadosJson = ConvertHostDetalhado['resources']
    saida_json = json.dumps(RespostaHostsDetalhadosJson, indent=2)
    print(saida_json)
    return(saida_json)

#Trás o detalhe de cada device_ID pesquisado na função anterior(listaDeHosts ou listaDeHostsComFiltro ) ----------------------------------------------------------
def listaDeHostsDetalhado():
    detalhesHeader = {
        'accept': 'application/json',
        'authorization': 'Bearer ' + token_auth,
        'Content-Type': 'application/json',
    }

    #Nessa request, é necessario passar no body da requisição a listas de hostsID para que ele possa trazer o detalhes dela.
    #Nessa variavel abaixo, estou preenchendo o body da requisição com a lista de maquinas que eu obtive através da função listaDeHosts() que no inicio do codigo. 
    #Isso faz com que eu reaproveite uma função que já está pronta, para economizar linhas de codigos! o deixando mais leve.
    detalhesBody = {
        'ids': listaDeHosts()
    }

    #Perceba que estou passando a variavel na requisição aqui -------------------------------------------------------V
    RespostaHostsDetalhados = requests.post(url+"/devices/entities/devices/v2", headers=detalhesHeader, json=detalhesBody)

    #abaixo segue o tratamento de dados igual aos demais
    ConvertHostDetalhado = RespostaHostsDetalhados.json()
    RespostaHostsDetalhadosJson = ConvertHostDetalhado['resources']
    saida_json = json.dumps(RespostaHostsDetalhadosJson, indent=2)
    print(saida_json)
    return(saida_json)

#Trás o Status de conexão dos hosts, para saber se estão online ou offline ) ----------------------------------------------------------
def hostsOnline():
    #abaixo estou dizendo que a Variavel ID é igual ao resultado da função listaDeHosts() //novamente estamos economizando codigo, utilizando uma função que já existe.
    ID = listaDeHosts()

    #a formatação do resultando acima está em array, portando ele segue um padrão separado por virgula[342423424234, 234234234234, 2342342342, 2342342]
    #porem nessa request, ele pede que variavel esteja esm strings pois será passada como parametro da URL.
    #A URL deverá ficar assim : /devices/entities/online-state/v1?ids=342423424234&ids=234234234234" sempre passando os IDS com o parametro "&ids=" entro um HostID e o outro.
    #com o codigo abaixo, estou convertendo o Array para string, passando pra ele que o separador será '&ids=', sendo assim, agora o retorno ficará assim: 342423424234&ids=234234234234
    string_resultante = '&ids='.join(ID)
    #Porém eu preciso que no inicio da frase tambem tenha '&ids=' para que ele fique assim = ids=342423424234&ids=234234234234
    #Na linha abaixo estou criando uma variavel de formatação final, com o texto da forma que eu preciso.
    string_final = '&ids=' + string_resultante

    headers = {
    'accept': 'application/json',
    'authorization': 'Bearer ' + token_auth,
    }

    #Perceba que agora estou passando o resultado da variavel aqui ---------V 
    resposta1 = requests.get(url+"/devices/entities/online-state/v1?"+string_final, headers=headers)

    #abaixo segue a formatação de texto normal.
    resposta2 = resposta1.json()
    host_ID = resposta2["resources"] ##gera a lista de hosts
    saida_json = json.dumps(host_ID, indent=2)
    print(saida_json)
     
#Essa é a função principal, sempre que o script for executado, ele vai procurar pela função main. As demais funções que passamos acima, ela só vai ser executada se em algum momento  ) ----------------------------------------------------------
#a gente chamar ela dentro da função main!
def main():
    #Na função principal vamos criar um esquema de parse de argumentos, para que possamos interagir com o escript solicitando apenas o que precisamos.

    # Na linha abaixo vamos configurar a descrição do parse quando alguem precisar do help
    parser = argparse.ArgumentParser(description='Help do script')
    
    #Abaixo estou criando os argumentos --hosts, --hostDetalhado, etc....
    # Add o argumento "--detailed"
    parser.add_argument('--hosts', action='store_true', help='Buscar todos os HostsID na console')
    parser.add_argument('--hostsDetalhado', action='store_true', help='Buscar todos os HostsID na console com Detalhes')
    parser.add_argument('--hostsWorkstation', action='store_true', help='Buscar todos os HostsID dos Workstation')
    parser.add_argument('--hostsFiltro', help='Buscar todos os HostsID dos Workstation')
    parser.add_argument('--hostsOnline', action='store_true', help='Buscar todos os HostsID dos Workstation')

    # Parseando os argumentos da linha de comando
    args = parser.parse_args()

    # Abaixo vamos criar as condições para cada argumento que criamos, perceba que estou criando um args. para cada chamada que criamos a cima e dando uma ação pra elas.
    
    if args.hosts:
        #Nessa condição estou dizendo que: Se o argumento for --hosts, execute a função listaDeHosts() que está na linha 41 e escreva o resultado na tela
        print(listaDeHosts())
    elif args.hostsWorkstation:
        #Nessa condição estou dizendo que: Se o argumento for --hostsWorkstation, execute a função listaDeWorkstation() que está na linha 61 e escreva o resultado na tela
        print(listaDeWorkstation())
    elif args.hostsFiltro:
        #Nessa condição vamos criar uma função de busca, para que possamos realizar busca com parametros livre.
        #abaixo estou criando uma variavel que vá armazenar tudo que eu escrever após o parametro --hostsFiltro
        #exemplo: python3 script.py --hostFiltro "cambaxirra3D"
        filtro = args.hostsFiltro

        Header = {
        'accept': 'application/json',
        'authorization': 'Bearer ' + token_auth,
        'Content-Type': 'application/json',
    }
        #nessa request abaixo, estou escrevendo a URL o valor da variavel filtro após o parametro filter=. 
        #dessa forma se eu digitar: python3 script.py --hostFiltro "product_type_desc:'Server'"
        #ele vai completar a url com o texto digitado ("product_type_desc:'Server'")
        #nesse exemplo ele só iria me trazer o que é servidores
        RespostaHostsDetalhados = requests.get(url+"/devices/queries/devices/v1?filter="+filtro, headers=Header)
        ConvertHostDetalhado = RespostaHostsDetalhados.json()
        RespostaHostsDetalhadosJson = ConvertHostDetalhado['resources']
        saida_json = json.dumps(RespostaHostsDetalhadosJson, indent=2)
        print(saida_json)
    elif args.hostsDetalhado:
        #Nessa condição estou dizendo que: Se o argumento for --listaDeHostsDetalhado, execute a função listaDeHostsDetalhado() que está na linha 79 e escreva o resultado na tela
        print(listaDeHostsDetalhado())
    elif args.hostsOnline:
        #Nessa condição estou dizendo que: Se o argumento for --hostsOnline, execute a função hostsOnline() que está na linha 104 e escreva o resultado na tela
        hostsOnline()
    else:
        #Nessa função temos o else que significa o final das opções, então caso não seja selecionada nenhuma das opções validas acima, ele vai apresentar uma mensagem na tela informando que o parametro não existe 
        print('Parametro não existe, digite o arqumento --help para mais detalhes')

#abaixo estamos especificando no codigo que o script começa na função main()
if __name__ == "__main__":
    main()
