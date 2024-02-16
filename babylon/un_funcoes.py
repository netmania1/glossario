#Adiciona os módulos
import un_bancodados
import os

import pandas as pd

#Função para retornar a lista de categorias
def retornaListaCategorias(obConexao):

  #Abre o cursor
  curListasCategorias = obConexao.cursor()

  #SQL para obter a lista de categorias
  stSqlListaDiretorio  = "SELECT id_categoria, nm_categoria FROM babylon_glossario_categoria ORDER BY nm_categoria";

  #Obtem os dados
  curListasCategorias = un_bancodados.retornaDados  (
                                                      obConexao,
                                                      stSqlListaDiretorio
                                                    )

  #Coloca os dados em uma lista
  lstDados = curListasCategorias.fetchall()

  #Retorno da função
  return lstDados

#Função para retornar a quantidade de linhas de um determinado glossário
def retornaTotalLinhasArquvo  (
                                obConexao,
                                intIdCategoria,
                                stNomeArquivo
                              ):

  #SQL para obter a lista de categorias
  stQtdTotalTermos  = "SELECT qt_totalregistros FROM babylon_glossario WHERE id_categoria = ? AND nm_arquivo = ?"

  #Lista de valores
  lstValores =  [
                  intIdCategoria, #ID da categoria
                  stNomeArquivo   #Nome do arquivo

                ]

  #Obtem os dados
  curTotalTermos = un_bancodados.retornaDadosViaParametros  (
                                                                obConexao,
                                                                stQtdTotalTermos,
                                                                lstValores
                                                            )

  #Executa consulta
  lstDados = curTotalTermos.fetchall()

  #Fecha o cursor
  curTotalTermos.close()

  #Retorno da função
  return lstDados

#Função para adicionar os dados dos glossário
def adicionarDadosGlossario (
                              obConexao,
                              stNomeArquivo,
                              stDescricaoGlossario,
                              intIdSituacao,
                              intIdCategoria,
                              intQtdTempoExtracao,
                              intQtdRegistros,
                              intIdIdomaOrigem,
                              intIdIdomaDestino,
                              intIdAutor,
                              stNomeGlossario,
                              intQtdLinhasIgnorar,
                              intQtdArquivos,
                              dtCriacaoGlossario,
                              dtUltimaAtualizacaoGlosasrio,
                              intQtdTempoConversao
                            ):

  #Monta o SQL para carregar os dados no banco
  stSqlInsereDados  = "INSERT INTO babylon_glossario (\n"
  stSqlInsereDados += "	nm_glossario,\n"
  stSqlInsereDados += "	nm_arquivo,\n"
  stSqlInsereDados += "	id_situacao,\n"
  stSqlInsereDados += "	id_categoria,\n"
  stSqlInsereDados += "	qt_tempoextracao,\n"
  stSqlInsereDados += "	qt_totalregistros,\n"
  stSqlInsereDados += "	qt_totalregistrosignorar,\n"
  stSqlInsereDados += "	id_idiomaorigem,\n"
  stSqlInsereDados += "	id_idiomadestino,\n"
  stSqlInsereDados += "	id_autor,\n"
  stSqlInsereDados += "	qt_totalarquivos,\n"
  stSqlInsereDados += "	ds_glossario,\n"
  stSqlInsereDados += " qt_totalregistrosignorar,\n"
  stSqlInsereDados += " qt_totalarquivos,\n"
  stSqlInsereDados += " dt_criacao,\n"
  stSqlInsereDados += " dt_atualizacao,\n"
  stSqlInsereDados += "	qt_tempoconversao\n"
  stSqlInsereDados += ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

  #Lista de valores
  lstValores =  [
                  stNomeGlossario,              #Nome do glosário
                  stNomeArquivo,                #Nome do arquivo
                  intIdSituacao,                #Situação da conversão
                  intIdCategoria,               #ID de categoria
                  intQtdTempoExtracao,          #Tempo gasto para extrair os dados do arquivo
                  intQtdRegistros,              #Quantidade de termos
                  intQtdLinhasIgnorar,          #Quantidade de registros a ser ignorado
                  intIdIdomaOrigem,             #ID do idioma de origem
                  intIdIdomaDestino,            #ID do idioma de destino
                  intIdAutor,                   #ID do autor
                  0,                            #Total de arquivos
                  stDescricaoGlossario,         #Descrição do glossário
                  intQtdLinhasIgnorar,          #Quantidade de linhas a serem ignoradas na carga
                  intQtdArquivos,               #Quantidade de arquivos gerados na covnersão
                  dtCriacaoGlossario,           #Data que o glossário foi criado
                  dtUltimaAtualizacaoGlosasrio, #Data que a última vez que o glossário foi atulizado
                  intQtdTempoExtracao           #Tempo gasto para tratar os dados do arquivo extraído
                ]

  #Executa comando
  un_bancodados.executaDmlViaParametros (
                                          obConexao,
                                          stSqlInsereDados,
                                          lstValores
                                        )

  #Recupera o código da inserção
  stSqlRetornaIdArquivo = "SELECT last_insert_rowid()"

  #Executa consulta
  curIdioma = un_bancodados.retornaDados  (
                                            obConexao,
                                            stSqlRetornaIdArquivo
                                          )

  #Amezena o código do termpo
  intIdIdioma = curIdioma.fetchone()[0]

  #Fecha o cursor
  curIdioma.close()

  #Retorna o código do arquivo_adicionado
  return intIdIdioma

#Retorna o valor de uma célular de um determinado dataframe
def retornaValorDataFrame (
                            dfDados,
                            stValorProcurar,
                          ):
  
  #Inicializa a variável de retorno
  stRetorno = ""

  for intContador in range(len(dfDados)):

    #Se o nome do campo for igual a linha do dataframe, pega o valor
    if dfDados.iloc[intContador, 0] == stValorProcurar:

        #Armazena o valor
        stRetorno = dfDados.iloc[intContador, 1]

        #Sai do laço
        break

  #Retorno da função
  return stRetorno
  
#Função para retornar o código do idioma
def retornaCodigoIdioma (
                          obConexao,
                          stIdioma
                        ):

  #SQL para verificar se o idioma já está cadastrado
  stSqlVerificaIdioma = "SELECT id_idioma, COUNT(*) AS qt_totalinhas FROM babylon_glossario_idioma WHERE nm_idioma = ?"

  #Lista de valores
  lstValores =  [stIdioma]

  #Executa consulta
  curIdioma = un_bancodados.retornaDadosViaParametros (
                                                        obConexao,
                                                        stSqlVerificaIdioma,
                                                        lstValores
                                                      )

  #Obtem só uma linha
  arResultado = curIdioma.fetchone()

  #Se a quantidade de linhas for maior que zero, armazena o código
  if arResultado[1] > 0:

    #Armazena o código do idioma
    intIdIdioma = arResultado[0]

  #Caso contrário, realia o procedimeto de adição e retorno do ID que foi usado
  else:

    #SQL para adicionar o idioma
    stSqlInsereIdioma = "INSERT INTO babylon_glossario_idioma (nm_idioma) VALUES ('"+ stIdioma +"')"

    #Grava o dados
    un_bancodados.executaDml  (
                                obConexao,
                                stSqlInsereIdioma
                              )

    #Recupera o código da inserção
    stSqlVerificaIdioma = "SELECT last_insert_rowid()"

    #Executa consulta
    curIdioma = un_bancodados.retornaDados  (
                                              obConexao,
                                              stSqlVerificaIdioma
                                            )

    #Armazena o código do idioma
    intIdIdioma = curIdioma.fetchone()[0]

    #Fecha o cursor
    curIdioma.close()

  #Retorno da função
  return intIdIdioma

#Função para retornar o código do auitor
def retornaCodigoAutor (
                          obConexao,
                          stNomeAutor
                        ):

  #SQL para verificar se o idioma já está cadastrado
  stSqlVerificaAutor = "SELECT id_autor, COUNT(*) AS qt_totalinhas FROM babylon_glossario_autor WHERE nm_autor = ?"

  #Lista de valores
  lstValores =  [stNomeAutor]

  #Executa consulta
  curAutor = un_bancodados.retornaDadosViaParametros  (
                                                        obConexao,
                                                        stSqlVerificaAutor,
                                                        lstValores
                                                      )

  #Obtem só uma linha
  arResultado = curAutor.fetchone()

  #Se a quantidade de linhas for maior que zero, armazena o código
  if arResultado[1] > 0:

    #Armazena o código do autor
    intIdAutor = arResultado[0]

  #Caso contrário, realia o procedimeto de adição e retorno do ID que foi usado
  else:

    #SQL para adicionar o autor
    stSqlInsereAutor = "INSERT INTO babylon_glossario_autor (nm_autor) VALUES (?)"

    lstValores = [stNomeAutor]

    #Grava o dados
    un_bancodados.executaDmlViaParametros (
                                            obConexao,
                                            stSqlInsereAutor,
                                            lstValores
                                          )

    #Recupera o código da inserção
    stSqlVerificaAutor = "SELECT last_insert_rowid()"

    #Executa consulta
    curAutor = un_bancodados.retornaDados  (
                                              obConexao,
                                              stSqlVerificaAutor
                                            )

    #Armazena o código do autor
    intIdAutor = curAutor.fetchone()[0]

  #Fecha o cursor
  curAutor.close()

  #Retorno da função
  return intIdAutor

#Função para dar carregar o corpo do glossário
def carregaTermosGlossario  (
                              obConexao,
                              dfDados,
                              intIdGlossario
                            ):

  #Adiciona coluna no dataframe
  dfDados.insert  (
                    loc     = 0,
                    column  = "id_glossario",
                    value   = intIdGlossario
                  )
  
  #Converte o dataframe em lista
  lstTermos = dfDados.values.tolist()

  #Grava os dados dos termos
  un_bancodados.cargaViaMany  (
                                  obConexao,
                                  "INSERT INTO babylon_glossario_termo (id_glossario, te_termo, ds_termo) VALUES (?, ?, ?);",
                                  lstTermos
                              )

#Para converter arquivo em binário  
def converterArquivomBinario(stArquivo):

  #Converte a imagem em binário
  with open(stArquivo, "rb") as file:
      binbData = file.read()

  #Retorno da função
  return binbData

#Função para inserir a imagem no banco
def insereArquivomBanco (  
                          obConexao,
                          intIdGlossario,
                          stNomeArquivo,
                          stArquivo
                        ):

    try:

        #Converte a imagem
        binArquivo = converterArquivomBinario(stArquivo)

        #SQL para inserir os dados
        stSqlInsert = "INSERT INTO babylon_glossario_termo_arquivos (id_glossario, nm_arquivo, ob_arquivo) VALUES (?, ?, ?)"

        # Converte os dados em uma tupla
        tplDados =  (
                      intIdGlossario,
                      stNomeArquivo,
                      binArquivo
                    )

        #Cria o cursor
        curDados = obConexao.cursor()

        #Executa o comando
        curDados.execute(stSqlInsert, tplDados)

        #Confirma a transação        
        obConexao.commit()

        #Fecha o cursor
        curDados.close()

    except obConexao.Error as error:
        print("\t\tFailed to insert blob data into sqlite table", error)
        exit()

#Função responsável por atualizar o status da carga de dados do glossário
def atualizaStatusCargaGlossario  (
                                    obConexao,
                                    dcmTempoCarga,
                                    intIdGlossario
                                  ):

    #Atualia o código da carga para "6" (carregado)
    stSqlAtulizaDadosCarga  = "UPDATE babylon_glossario SET id_situacao = ?, qt_tempocarga = ? WHERE id_glossario = ?"

    #Lista de valores
    lstValores =  [
                    6,              #Situação do glossário
                    dcmTempoCarga,  #Tempo de execução da rotina
                    intIdGlossario  #ID do glossário
                  ]

    #Executa consulta
    un_bancodados.executaDmlViaParametros (
                                            obConexao,
                                            stSqlAtulizaDadosCarga,
                                            lstValores
                                          )

#Função responsável por atualizar o tempo gasto e a quantidade de arquivos carregados
def atualizaTotaisArquivos  (
                              obConexao,
                              intIdGlossario,
                              dcmTempoCarga,
                              intQtdArquivos
                            ):

    #Atualia o código da carga para "6" (carregado)
    stSqlAtulizaDadosCarga  = "UPDATE babylon_glossario SET qt_totalarquivos = ?, qt_tempocargaarquivos = ? WHERE id_glossario = ?"

    #Lista de valores
    lstValores =  [
                    intQtdArquivos, #Quantidade de arquivos carregados
                    dcmTempoCarga,  #Tempo de execução da rotina
                    intIdGlossario  #ID do glossário
                  ]

    #Executa consulta
    un_bancodados.executaDmlViaParametros (
                                            obConexao,
                                            stSqlAtulizaDadosCarga,
                                            lstValores
                                          )

#Função responsável por criar o diretório se ele não existir
def criarDiretorioNaoExistir(stCaminho):

  #Se o diretório não existir, cria
  if os.path.exists(stCaminho) == False:

    #Cria o diretório
    os.makedirs(stCaminho)

#Função para tratar os registros que possuam mais de um termo separado por pipe "|"
def trataTermosComPipe(dfDados):

  #Inicializa as listas
  lstTermos     = []
  lstDescricoes = []

  #Parâmetros do filtro
  arParametrosFiltro = ["\|"]

  #Filtra os registros a serem tratados
  dfDados = dfDados[dfDados.termo.str.contains("|".join(arParametrosFiltro))]

  #Se tiver algum registro, trata os dados
  if dfDados.shape[0] > 0:

    #Laço para percorrer o dataframe
    for intContadorTermosDataFrame in dfDados.index:

      #Pega a lista de termos que foram separados
      lstTermosSeparados = dfDados["termo"][intContadorTermosDataFrame].split("|")

      #Monta os dados nas listas
      lstTermos.extend      (lstTermosSeparados)
      lstDescricoes.extend  ([dfDados["descricao"][intContadorTermosDataFrame]] * len(lstTermosSeparados))

    #Junta as listas
    lstCarga = list (
                      zip (
                            lstTermos,
                            lstDescricoes
                          )
                    )

    #Cria o dataframe temporário com base na lista de dados
    dfDadosTratados = pd.DataFrame(lstCarga)

    #Renomeia os campos
    dfDadosTratados.columns = ["termo", "descricao"]

    #Caso contrário, retorna um dataframe vazio
  else:

    #Cria o dataframe vazio
    dfDadosTratados = pd.DataFrame  (columns =  ["termo","descricao"])

  #Retorno da função
  return dfDadosTratados