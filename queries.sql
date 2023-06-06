-- Metadados e estatísticas

-- A quantidade de tabelas do banco de dados:
SELECT COUNT(tablename)
FROM pg_catalog.pg_tables
WHERE 
  schemaname != 'pg_catalog' AND 
  schemaname != 'information_schema';

-- A quantidade de atributos de cada tabela:
SELECT table_name, count(column_name)
FROM 
  information_schema.columns
WHERE table_name IN (
  SELECT
  table_name
  FROM information_schema.tables
  WHERE table_schema = 'public'
)
GROUP BY table_name;

-- O tamanho de cada tabela em em gigabaytes
SELECT
  table_name,
  pg_size_pretty(pg_relation_size(quote_ident(table_name))),
  pg_relation_size(quote_ident(table_name))
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY 3 DESC;

-- A quantidade de acessos sequenciais realizada em cada tabela
SELECT relname, seq_scan
FROM pg_stat_user_tables;

-- Consulta 1
SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
FROM estabelecimento E
INNER JOIN cnae C
ON E.cnae_fiscal_principal = C.codigo
WHERE ano_inicio_atividade BETWEEN '2015' AND '2023'
GROUP BY 1;

-- Consulta 2
SELECT E.uf as estado, count(E.cnpj_basico) as quantidade
FROM estabelecimento E
INNER JOIN cnae C ON E.cnae_fiscal_principal = C.codigo
INNER JOIN pais on pais.codigo = E.pais
WHERE ano_inicio_atividade BETWEEN '2015' AND '2023'
  AND pais.descricao = 'BRASIL'
GROUP BY 1
ORDER BY 2 ASC;

-- Consulta 3
SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
WHERE SI.opcao_pelo_simples = 'S' AND ano_inicio_atividade BETWEEN '2015' AND '2023'
GROUP BY 1;

-- Consulta 4
SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
INNER JOIN pais on pais.codigo = ES.pais
WHERE ano_inicio_atividade BETWEEN '2015' AND '2023'
  AND pais.descricao = 'BRASIL'
GROUP BY 1
ORDER BY 2 ASC;

-- Consulta 5
SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
WHERE SI.opcao_mei = 'S' AND ano_inicio_atividade BETWEEN '2015' AND '2023'
GROUP BY 1;

-- Consulta 6
SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
INNER JOIN pais on pais.codigo = ES.pais
WHERE ano_inicio_atividade BETWEEN '2015' AND '2023'
  AND pais.descricao = 'BRASIL'
GROUP BY 1
ORDER BY 2 ASC;

-- Consulta 7
SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
FROM estabelecimento E
INNER JOIN cnae C
ON E.cnae_fiscal_principal = C.codigo
WHERE ano_inicio_atividade BETWEEN '2015' AND '2023'
    AND C.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
GROUP BY 1
ORDER BY 1;

-- Consulta 8
SELECT E.uf as estado, count(E.cnpj_basico) as quantidade
FROM estabelecimento E
INNER JOIN cnae C ON E.cnae_fiscal_principal = C.codigo
INNER JOIN pais on pais.codigo = E.pais
WHERE ano_inicio_atividade BETWEEN '2015' AND '2023'
    AND C.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
    AND pais.descricao = 'BRASIL'
GROUP BY 1
ORDER BY 2 ASC;

-- Consulta 9
SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
WHERE SI.opcao_pelo_simples = 'S' 
    AND ano_inicio_atividade BETWEEN '2015' AND '2023'
    AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
GROUP BY 1
ORDER BY 1;

-- Consulta 10
SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
INNER JOIN pais on pais.codigo = ES.pais
WHERE SI.opcao_pelo_simples = 'S' 
  AND ano_inicio_atividade BETWEEN '2015' AND '2023'
  AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100')
  AND pais.descricao = 'BRASIL'
GROUP BY 1
ORDER BY 2 ASC;

-- Consulta 11
SELECT ano_inicio_atividade as ano, count(data_inicio_atividade) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
WHERE SI.opcao_mei = 'S' 
    AND ano_inicio_atividade BETWEEN '{start}' AND '{end}'
    AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100', '9511800')
GROUP BY 1;

-- Consulta 12
SELECT ES.uf as estado, count(ES.cnpj_basico) as quantidade
FROM estabelecimento ES
INNER JOIN empresa EM ON ES.cnpj_basico = EM.cnpj_basico
INNER JOIN simples SI ON SI.cnpj_basico = EM.cnpj_basico
INNER JOIN cnae CN ON ES.cnae_fiscal_principal = CN.codigo
WHERE SI.opcao_mei = 'S' 
  AND ano_inicio_atividade BETWEEN '2015' AND '2023'
  AND CN.codigo IN ('6201500', '6201501', '6202300', '6203100', '6204000', '6209100', '9511800')
GROUP BY 1
ORDER BY 2 ASC;

-- Indices hash
CREATE INDEX empresa_cnpj_basico_hash_index ON empresa USING HASH(cnpj_basico);
CREATE INDEX simples_cnpj_basico_hash_index ON simples USING HASH(cnpj_basico);
CREATE INDEX estabelecimento_cnpj_basico_hash_index ON estabelecimento USING HASH(cnpj_basico);
CREATE INDEX cnae_codigo_hash_index ON cnae USING HASH(codigo);
CREATE INDEX ano_inicio_atividade_estabelecimento_btree_index ON estabelecimento USING BTREE(ano_inicio_atividade);
 