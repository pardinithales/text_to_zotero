# Text to Zotero

Importador de referências bibliográficas para o Zotero usando OpenAI e Firecrawl.

## Download

Você pode baixar a versão mais recente do executável na [página de releases](https://github.com/pardinithales/text_to_zotero/releases).

## Requisitos

Para usar o programa você precisa:
- Windows 10 ou superior
- Conta no Zotero (para obter Library ID e API Key)
- Chave de API do OpenAI
- Chave de API do Firecrawl

## Instalação

### Usuários
1. Baixe o executável mais recente
2. Extraia o arquivo ZIP
3. Execute o arquivo `Text to Zotero.exe`
4. Insira suas credenciais na interface do programa

### Desenvolvedores
1. Clone o repositório:
```bash
git clone https://github.com/pardinithales/text_to_zotero.git
cd text_to_zotero
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python zotero_importer.py
```

## Uso

1. Insira suas credenciais:
   - Zotero Library ID e API Key
   - OpenAI API Key
   - Firecrawl API Key

2. Cole suas referências bibliográficas na área de texto

3. Clique em "Importar Referências"

4. O programa irá:
   - Analisar as referências com OpenAI
   - Buscar dados complementares via Firecrawl
   - Mesclar os dados
   - Criar os itens no Zotero

## Criando o Executável

Para criar o executável:

```bash
pip install -r requirements.txt
pyinstaller --clean zotero_importer.spec
```

O executável será criado na pasta `dist`.

## Suporte

Para problemas ou sugestões, abra uma issue no GitHub. 