# Arquitetura local — ARI NEWS

```text
Setor + Região + Data
        ↓
obtenção
        ↓
validação
        ↓
formatação
        ↓
Hero Image
        ↓
ARI NEWS
```

No modo DEMO, a obtenção retorna três notícias locais e demonstrativas, sem rede. No modo TEMPO REAL, `providers.py` expõe apenas o contrato do adaptador; sem adaptador configurado, a aplicação retorna `Modo tempo real não configurado.`

Cada item preserva `original_url` como URL de origem e cria `google_search_url` localmente a partir do título. A Aula 1 diverge entre o pedido de Link original e o Nó 6, que substitui o campo URL por uma busca Google. Por isso, o MVP mantém os dois campos: “Acesse a Fonte” usa a URL original e “Buscar no Google” usa a URL derivada.
