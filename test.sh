# PARA SIMPLE QUERIES

# 1º PASSO: PRODUZIR RESULTADOS SOLR
# Produzir resultados para no schema
./scripts/query_solr.py --query config/simple_queries/no_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar > config/simple_queries/no_schema/results/result_query1.json

# Produzir resultados para simple schema
./scripts/query_solr.py --query config/simple_queries/simple_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar > config/simple_queries/simple_schema/results/result_query1.json

# Produzir resultados para boosted schema
./scripts/query_solr.py --query config/simple_queries/boosted_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar > config/simple_queries/boosted_schema/results/result_query1.json


# 2º PASSO: CONVERTER RESULTADOS SOLR PARA FORMATO TREC

# Produzir resultados para no schema
./scripts/query_solr.py --query config/simple_queries/no_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar | ./scripts/solr2trec.py > config/simple_queries/no_schema/qrels/result_query1_trec.txt

# Produzir resultados para simple schema
./scripts/query_solr.py --query config/simple_queries/simple_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar | ./scripts/solr2trec.py > config/simple_queries/simple_schema/qrels/result_query1_trec.txt

# Produzir resultados para boosted schema
./scripts/query_solr.py --query config/simple_queries/boosted_schema/queries/query1.json --uri http://localhost:8983/solr --collection wikiwar | ./scripts/solr2trec.py > config/simple_queries/boosted_schema/qrels/result_query1_trec.txt


# 3º PASSO: CONVERTER QRELS PARA FORMATO TREC

# Produzir resultados para no schema
cat config/simple_queries/no_schema/qrels/qrels1.txt | ./scripts/qrels2trec.py > config/simple_queries/no_schema/qrels/qrels_trec1.txt

# Produzir resultados para simple schema
cat config/simple_queries/simple_schema/qrels/qrels1.txt | ./scripts/qrels2trec.py > config/simple_queries/simple_schema/qrels/qrels_trec1.txt

# Produzir resultados para boosted schema
cat config/simple_queries/boosted_schema/qrels/qrels1.txt | ./scripts/qrels2trec.py > config/simple_queries/boosted_schema/qrels/qrels_trec1.txt

# 4º PASSO: AVALIAR RESULTADOS

# Avaliar resultados para no schema
src/trec_eval/trec_eval config/simple_queries/no_schema/qrels/qrels_trec1.txt config/simple_queries/no_schema/qrels/result_query1_trec.txt

# Avaliar resultados para simple schema
src/trec_eval/trec_eval config/simple_queries/simple_schema/qrels/qrels_trec1.txt config/simple_queries/simple_schema/qrels/result_query1_trec.txt

# Avaliar resultados para boosted schema
src/trec_eval/trec_eval config/simple_queries/boosted_schema/qrels/qrels_trec1.txt config/simple_queries/boosted_schema/qrels/result_query1_trec.txt

# 5º PASSO: PLOTAR PRECISION-RECALL



cat config/advanced/results/results_sys1_trec.txt | ./scripts/plot_pr.py --qrels config/advanced/qrels/qrels_trec1.txt --output config/advanced/images/prec_rec_sys1.png