#Conexão com banco de dados
def conexaoBanco  (
                    obSqLite3,
                    stCaminhoBanco
                  ):

  #Abre conexão
  obConexao = obSqLite3.connect(stCaminhoBanco)

  #Abre coneão com banco de dados
  return obConexao

#Executa comandos DML
def executaDml  (
                  obConexao,
                  stSql
                ):

  #Abre o cursor
  curSql = obConexao.cursor()

  #Executa o comando
  curSql.execute(stSql)

  #Confirma o comando
  obConexao.commit()

  #Fecha o cursor
  curSql.close()

#Executa comandos SQL que retornem dados
def retornaDados  (
                    obConexao,
                    stSql
                  ):

  #Executa comando
  curSql = obConexao.execute(stSql)

  #Retorno da função
  return curSql

#Executa comandos SQL que retornem dados
def retornaDadosViaParametros  (
                    obConexao,
                    stSql,
                    lstParametros
                  ):

  #Executa comando
  curSql = obConexao.execute  (
                                stSql,
                                lstParametros
                              )

  #Retorno da função
  return curSql

#Executa comandos DML com parâmetros
def executaDmlViaParametros (
                              obConexao,
                              stSql,
                              lstParametros
                            ):

  #Abre o cursor
  curSql = obConexao.cursor()

  #Executa o comando
  curSql.execute  (
                    stSql,
                    lstParametros
                  )

  #Confirma o comando
  obConexao.commit()

  #Fecha o cursor
  curSql.close()

#Função para dar carga usando o comando "executemany"
def cargaViaMany  (
                    obConexao,
                    stSql,
                    lstDados
                  ):

  #Executa a gravação dos dados
  obConexao.executemany (
                          stSql,
                          lstDados
                        )

  #Confirma a transação
  obConexao.commit()