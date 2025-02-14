# Text to Zotero

Importador de referências bibliográficas para o Zotero usando OpenAI e Firecrawl.

## Requisitos

- Python 3.8 ou superior
- Conta no Zotero (para obter Library ID e API Key)
- Chave de API do OpenAI
- Chave de API do Firecrawl

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pardinithales/text_to_zotero.git
cd text_to_zotero
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   ```bash
   cp .env.example .env
   ```
   - Edite o arquivo `.env` com suas credenciais:
     - `ZOTERO_LIBRARY_ID`: ID da sua biblioteca Zotero
     - `ZOTERO_API_KEY`: Chave de API do Zotero
     - `OPENAI_API_KEY`: Chave de API do OpenAI
     - `FIRECRAWL_API_KEY`: Chave de API do Firecrawl

4. Execute o programa:
```bash
python zotero_importer.py
```

## Uso

1. Cole suas referências bibliográficas na área de texto
2. Clique em "Importar Referências"
3. O programa irá:
   - Analisar as referências com OpenAI
   - Buscar dados complementares via Firecrawl
   - Mesclar os dados
   - Criar os itens no Zotero

## Suporte

Para problemas ou sugestões, abra uma issue no GitHub. 