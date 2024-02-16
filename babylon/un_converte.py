'''
  Data:       05/02/2025
  Autor:      Otacílio Ribeiro
  Descrição:	Rotina responsável por converter os glossário Babylon para formato CSV (separado por tabulação) para dar
              carga no banco de dados. Este código é uma reedição do código feito por mim em PHP, só que otimizando a
              sua estrutura.

  Alteração
  Data:       06/02/2025
  Autor:      Otacílio Ribeiro
  Descrição:	Alteração no código de leitura do Pandas para ignorar os registros com erro de token.

  Alteração
  Data:       07/02/2025
  Autor:      Otacílio Ribeiro
  Descrição:	Alteração na lógica para em vez de criar o diretório se não existir para verificar se ele existir,
              verificar se term arquivos para serem processados.

              Se ocorrer erro de conversão (por falha do PyGlossary ou não voltar itens), move o arquivo de erros para o
              diretório "erro" e remove o diretório dos arquivos extraídos dele.

  Alteração
  Data:       08/02/2025
  Autor:      Otacílio Ribeiro
  Descrição:	Adição do aviso quando o glossário não tem nenhum conteúdo.

  Alteração
  Data:       15/02/2025
  Autor:      Otacílio Ribeiro
  Descrição:	Alteração da posição para tratar os valores nulos, em vez só no dataframe das informações do arquivo, agora
              para o dataframe bruto.

  Alteração
  Data:       16/02/2025
  Autor:      Otacílio Ribeiro
  Descrição:	Banco de dados não será mais compartilhado e ficará dentro da pasta do conversor.
'''

#Arquivos internos
import un_bancodados
import un_funcoes

#Bibliotecas externas
import glob
import pandas   as pd
import sqlite3
import os
import shutil
import subprocess
import sys
import time

#Desativa a geração do bytecode
sys.dont_write_bytecode = True

#Inicializa as variáveis
intTotalGlossarioProcessados   = 1
stNomeGlossario                = ""
stDescricao                    = ""

#Define o caminho padrão da aplicação
stCaminhoBase               = os.path.dirname(os.path.realpath(__file__)).replace("\\", "//")
stCaminhoOrigemArquivos     = stCaminhoBase + "//origem//"
stCaminhoDestinoArquivos    = stCaminhoBase + "//destino//"
stCaminhoProcessadoArquivos = stCaminhoBase + "//processado//"
stCaminhoErroArquivos       = stCaminhoBase + "//erro//"
stCaminhoBancoDados         = stCaminhoBase + "//banco_dados//babylon.sqlite"
stCaminhoPyGlossary         = stCaminhoBase + "//pyglossary-master//"

#Cria os diretórios base se não existir
un_funcoes.criarDiretorioNaoExistir(stCaminhoDestinoArquivos)
un_funcoes.criarDiretorioNaoExistir(stCaminhoProcessadoArquivos)
un_funcoes.criarDiretorioNaoExistir(stCaminhoErroArquivos)

#Abre conexão com banco de daods
obConexao = un_bancodados.conexaoBanco  (
                                          sqlite3,
                                          stCaminhoBancoDados
                                        )

#Define o tipo de log do SQLite
obConexao.execute("pragma journal_mode=MEMORY")

#Obtem a lista de categorias
lstCategorias = un_funcoes.retornaListaCategorias(obConexao)

#Percorre a lista de categorias
for intContadorCategorias in range(len(lstCategorias)):

  #Monta o caminho dos arquivos
  stCaminhoArquivosOrigem = stCaminhoOrigemArquivos + str(lstCategorias[intContadorCategorias][0])

  #Se o diretório existir, verifica se tem arquivos
  if os.path.exists(stCaminhoArquivosOrigem) == True:

    #Muda para o diretório dos arquivos
    os.chdir(stCaminhoArquivosOrigem)

    #Filtro dos arquivos padrão Babylon
    stFiltroBabylon = glob.iglob('*.bgl')

    print("\n\nID da categoria: " + str(lstCategorias[intContadorCategorias][0])  +" - Nome da categoria: "+ lstCategorias[intContadorCategorias][1])

    #Laço para mostrar os arquivos
    for lstArquivos in stFiltroBabylon:

      #Obtem quantas linhas já foram processadas do arquivo
      lstTotalTermos = un_funcoes.retornaTotalLinhasArquvo  (
                                                              obConexao,
                                                              str(lstCategorias[intContadorCategorias][0]),
                                                              lstArquivos
                                                            )

      #Se a quantidade de linhas for igual a zero, inicia a conversão dos dados
      if len(lstTotalTermos) == 0:

        #Inicializa as variáveis
        stNomeArquivoConvertido       = lstArquivos
        stNomeArquivoConvertido       = stNomeArquivoConvertido.replace(".bgl", ".tab")
        stNomeArquivoConvertido       = stNomeArquivoConvertido.replace(".BGL", ".tab")
        stCaminhoArquivosExtraidos    = stCaminhoArquivosOrigem + "//" + stNomeArquivoConvertido.replace(".tab", ".tab_res")
        stParametroConversao          = "python3 \""+ stCaminhoPyGlossary +"pyglossary.pyw\" --no-progress-bar --remove-html-all --optimize-memory \""+ stCaminhoArquivosOrigem + "//" + lstArquivos +"\" \""+ stCaminhoArquivosOrigem + "//"+ stNomeArquivoConvertido +"\""
        stDescricaoGlossario          = ""
        dcmInicioExtracao             = time.time()
        intIdSituacao                 = 1
        intQtdLinhas                  = 0
        intQtdArquivos                = 0
        intIdIdiomaOrigem             = 1
        intIdIdiomaDestino            = 1
        intIdAutor                    = 1
        dtCriacaoGlossario            = ""
        dtUltimaAtualizacaoGlosasrio  = ""

        print("\tArquivo: "+ stNomeArquivoConvertido)

        print("\t\tIniciando a conversão")

        #Chama a rotina de conversão dos glossários
        stRetornoConversao  = subprocess.run  (
                                                stParametroConversao,
                                                shell           = True,
                                                capture_output  = True,
                                                text            = True
                                              )
                                                                      
        print("\t\tFim da conversão")

        #Se o arquivo existir, conta a quantide de linhas
        if os.path.exists(stCaminhoArquivosOrigem + "//"+ stNomeArquivoConvertido):

          print("\t\tIniciando o tratamento dos dados")

          #Carrega o arquivo no Pandas
          dfDados = pd.read_csv (
                                  stCaminhoArquivosOrigem + "//"+ stNomeArquivoConvertido,
                                  sep             = "\t",
                                  header          = None,
                                  on_bad_lines    = "skip",
                                  engine          = "python",
                                  names           = [
                                                      "termo",
                                                      "descricao"
                                                    ]
                                )

          #Calcula o tempo gasto na extração dos dados
          dmcFimExtracao = time.time() - dcmInicioExtracao

          #Amazena o início da conversão dos dados
          dmcInicioConversao = time.time()

          #Removendo registros duplicados
          dfDados = dfDados.drop_duplicates()

          #Altera os valores nulos por "?"
          dfDados = dfDados.fillna("?")

          #Pega somente os registros dos glossário
          dfInformacoesGlossario = dfDados[dfDados["termo"].str.contains("##") == True]

          #Pega somente os dados das informações do glossário
          dfDadosGlossario = dfDados[dfDados["termo"].str.contains("##") == False]

          #Obtem o nome do glossário
          stNomeGlossario = un_funcoes.retornaValorDataFrame  (
                                                                dfInformacoesGlossario,
                                                                "##name"
                                                              )

          #Obtem a descrição do glossário
          stDescricaoGlossario = un_funcoes.retornaValorDataFrame (
                                                                    dfInformacoesGlossario,
                                                                    "##description"
                                                                  )

          #Obtem a data da criação do glossario
          dtCriacaoGlossario = un_funcoes.retornaValorDataFrame (
                                                                  dfInformacoesGlossario,
                                                                  "##creationTime"
                                                                )      

          #Obtem a data da última atulização do glossario
          dtUltimaAtualizacaoGlosasrio = un_funcoes.retornaValorDataFrame (
                                                                            dfInformacoesGlossario,
                                                                            "##lastUpdated"
                                                                          )
          
          #Obtem o idioma de origem
          intIdIdiomaOrigem = un_funcoes.retornaCodigoIdioma  (
                                                                obConexao,
                                                                un_funcoes.retornaValorDataFrame  (
                                                                                                    dfInformacoesGlossario,
                                                                                                    "##sourceLang"
                                                                                                  )
                                                              )

          #Obtem o idioma de destino
          intIdIdiomaDestino = un_funcoes.retornaCodigoIdioma (
                                                                obConexao,
                                                                un_funcoes.retornaValorDataFrame  (
                                                                                                    dfInformacoesGlossario,
                                                                                                    "##targetLang"
                                                                                                  )
                                                              )

          #Obtem o idioma do autor
          intIdAutor = un_funcoes.retornaCodigoAutor  (
                                                        obConexao,
                                                        un_funcoes.retornaValorDataFrame  (
                                                                                            dfInformacoesGlossario,
                                                                                            "##author"
                                                                                          )
                                                      )

          #Se a quantidade de linhas for igual zero, coloca o código 4 (sem dados)
          if len(dfDadosGlossario) == 0:

            print("\t\tArquivo sem dados :" + lstArquivos)

            #Sem dados
            intIdSituacao = 4

        #Se o arquivo não exisitir, coloca o código 9
        else:

            print("\t\tErro ao converter o arquivo :" + lstArquivos)

            #Erro de conversão
            intIdSituacao = 9

            #Cria dois dataframes vazios só para o controle
            dfDadosGlossario        = pd.DataFrame()
            dfInformacoesGlossario  = pd.DataFrame()

        #Só chama a rotina abaixo se o código da situação for igual a 1
        if intIdSituacao == 1:

          print("\tIniciando a quebra dos termos separados por \"|\"")

          #Executa função para tratar os termos que estão separados por pipe
          dfDadosGlossarioTratados = un_funcoes.trataTermosComPipe(dfDadosGlossario)

          #Parâmetros do filtro
          arParametrosFiltro = ["\|"]

          #Limpa o dataframe de origem com registros com pipe
          dfDadosGlossario = dfDadosGlossario[dfDadosGlossario["termo"].str.contains("|".join(arParametrosFiltro)) == False]

          #Junta os dataframes com os dados ok com os dados tratados
          dfDadosGlossario = pd.concat  (
                                          [
                                            dfDadosGlossario,
                                            dfDadosGlossarioTratados
                                          ],
                                          axis          = 0,
                                          ignore_index  = True
                                        )

          #Ordena os dados
          dfDadosGlossario = dfDadosGlossario.sort_values(["termo"])

          print("\tFim da quebra dos termos separados por \"|\"")

        print("\tFim do tratadameto dos dados")

        #Calcula a diferença de tempo gasto tratar o arquivo
        dmtFimConversao = time.time() - dmcInicioConversao

        print("\tInício da gravação dados do arquivo convertido no banco")

        #Se o diretório existir, conta a quantidade de arquivos extraídos do glossário
        if os.path.exists(stCaminhoArquivosExtraidos):

          #Conta a quantidade de arquivos
          intQtdArquivos = len(os.listdir(stCaminhoArquivosExtraidos))

        #Chama a função para gravar os dados do glossário
        intIdGlossario = un_funcoes.adicionarDadosGlossario (
                                                              obConexao,
                                                              lstArquivos,
                                                              stDescricaoGlossario,
                                                              intIdSituacao,
                                                              lstCategorias[intContadorCategorias][0],
                                                              dmcFimExtracao,
                                                              len(dfDadosGlossario),
                                                              intIdIdiomaOrigem,
                                                              intIdIdiomaDestino,
                                                              intIdAutor,
                                                              stNomeGlossario,
                                                              dfInformacoesGlossario.shape[0],
                                                              intQtdArquivos,
                                                              dtCriacaoGlossario.replace(",", ""),
                                                              dtUltimaAtualizacaoGlosasrio.replace(",", ""),
                                                              dmtFimConversao
                                                            )

        #Se o ID da situação for 1 move para diretório de processados
        if intIdSituacao == 1:

          #Move o arquivo exportad para o diretório "destino"
          shutil.move (
                        stCaminhoArquivosOrigem + "//" + stNomeArquivoConvertido,
                        stCaminhoDestinoArquivos + str(intIdGlossario)  + "_" + stNomeArquivoConvertido
                      )

          #Apaga o arquivo original
          os.remove(stCaminhoArquivosOrigem + "//" + lstArquivos)

        #Caso contrário, para o diretório de arquivos com erro
        else:

          #Se o arquivo existir, move para o diretório de erros
          if os.path.exists(stCaminhoArquivosOrigem + "//" + stNomeArquivoConvertido):

            #Remove o arquivo de origem
            os.remove(stCaminhoArquivosOrigem + "//" + lstArquivos)

            #Move o arquivo exportad para o diretório "erro"
            shutil.move (
                          stCaminhoArquivosOrigem + "//" + stNomeArquivoConvertido,
                          stCaminhoErroArquivos + str(intIdGlossario)  + "_" + stNomeArquivoConvertido
                        )

            #Se existtir o diretório dos arquivos extraídos existir, removove
            if os.path.exists(stCaminhoArquivosExtraidos):

              #Remove o diretório dos arquivos processados
              shutil.rmtree(stCaminhoArquivosExtraidos)

        print("\tFim da gravação dados do arquivo convertido no banco")

        #Se o código da situação for igual a 1, adiciona os dados do glossário
        if intIdSituacao == 1:
          
          #Para calcular o tempo de carga
          dcmInicio = time.time()

          print("\tIniciando a gravação dos termos")

          #Chama função para dar carga dos dados do glossário
          un_funcoes.carregaTermosGlossario (
                                              obConexao,
                                              dfDadosGlossario,
                                              intIdGlossario
                                            )

          #Atualiza a situação da carga
          un_funcoes.atualizaStatusCargaGlossario (
                                                    obConexao,
                                                    str(time.time() - dcmInicio),
                                                    intIdGlossario
                                                  )

          print("\tFim da gravação dos termos")

          #Se a quantidade de arquivos for maior que zero, adiciona no banco
          if intQtdArquivos > 0:

            #Para calcular o tempo de execução da rotina
            dcmInicio = time.time()

            print("\tIniciando a gravação dos dos arqivos após extração")

            #Listar arquivos do diretório
            lstArquivos = os.listdir(stCaminhoArquivosExtraidos)

            #Percorre a lista de arquivos
            for arquivo in lstArquivos:

              #Adicinoa o arquivo no banco
              un_funcoes.insereArquivomBanco  (
                                                obConexao,
                                                intIdGlossario,
                                                arquivo,
                                                stCaminhoArquivosExtraidos + "//" + arquivo
                                              )

            #Atualiza os totais de arquivos e o tempo de execução
            un_funcoes.atualizaTotaisArquivos (
                                                obConexao,
                                                intIdGlossario,
                                                str(time.time() - dcmInicio),
                                                str(len(os.listdir(stCaminhoArquivosExtraidos)))
                                              )

            #Remove o diretório dos arquivos processados
            shutil.rmtree(stCaminhoArquivosExtraidos)

            print("\tFim da gravação dos dos arqivos após extração")

          #Move o arquivo carregado para o diretório "processado"
          shutil.move (
                        stCaminhoDestinoArquivos + str(intIdGlossario)  + "_" + stNomeArquivoConvertido,
                        stCaminhoProcessadoArquivos + str(intIdGlossario)  + "_" + stNomeArquivoConvertido
                      )

          print("-------------------------------------------------")

          #Destroi os Dataframes
          del [
                [
                    dfDados,
                    dfDadosGlossario,
                    dfInformacoesGlossario,
                    dfDadosGlossarioTratados
                ]
              ]

#Fecha conexão
obConexao.close