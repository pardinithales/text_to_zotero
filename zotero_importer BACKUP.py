from pyzotero import zotero
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from openai import OpenAI
from firecrawl import FirecrawlApp
import traceback

class ZoteroImporter:
    def __init__(self):
        try:
            self.window = tk.Tk()
            self.window.title("Importador de Referências para Zotero")
            self.window.geometry("800x700")
            
            # Inicializar variáveis
            self.library_id = None
            self.api_key = None
            self.openai_key = None
            self.firecrawl_key = None
            
            self.setup_ui()
            self.load_credentials()
            
        except Exception as e:
            self.show_error("Erro na inicialização", str(e))
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        try:
            # Configure credentials frame
            credentials_frame = ttk.LabelFrame(self.window, text="Credenciais", padding="10")
            credentials_frame.pack(fill="x", padx=10, pady=5)
            
            # Zotero credentials
            zotero_frame = ttk.LabelFrame(credentials_frame, text="Zotero", padding="5")
            zotero_frame.pack(fill="x", padx=5, pady=5)
            
            ttk.Label(zotero_frame, text="Library ID:").grid(row=0, column=0, padx=5, pady=5)
            self.library_id = ttk.Entry(zotero_frame)
            self.library_id.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(zotero_frame, text="API Key:").grid(row=1, column=0, padx=5, pady=5)
            self.api_key = ttk.Entry(zotero_frame, show="*")
            self.api_key.grid(row=1, column=1, padx=5, pady=5)
            
            # OpenAI credentials
            openai_frame = ttk.LabelFrame(credentials_frame, text="OpenAI", padding="5")
            openai_frame.pack(fill="x", padx=5, pady=5)
            
            ttk.Label(openai_frame, text="API Key:").grid(row=0, column=0, padx=5, pady=5)
            self.openai_key = ttk.Entry(openai_frame, show="*")
            self.openai_key.grid(row=0, column=1, padx=5, pady=5)

            # Firecrawl credentials
            firecrawl_frame = ttk.LabelFrame(credentials_frame, text="Firecrawl", padding="5")
            firecrawl_frame.pack(fill="x", padx=5, pady=5)
            
            ttk.Label(firecrawl_frame, text="API Key:").grid(row=0, column=0, padx=5, pady=5)
            self.firecrawl_key = ttk.Entry(firecrawl_frame, show="*")
            self.firecrawl_key.grid(row=0, column=1, padx=5, pady=5)
            
            # Botões de credenciais
            cred_button_frame = ttk.Frame(credentials_frame)
            cred_button_frame.pack(fill="x", padx=5, pady=5)
            
            self.save_cred_btn = ttk.Button(cred_button_frame, text="Salvar Credenciais", command=self.save_credentials)
            self.save_cred_btn.pack(side="left", padx=5)
            
            self.load_cred_btn = ttk.Button(cred_button_frame, text="Recarregar Credenciais", command=self.load_credentials)
            self.load_cred_btn.pack(side="left", padx=5)
            
            # Configure input frame
            input_frame = ttk.LabelFrame(self.window, text="Cole suas Referências Aqui", padding="10")
            input_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            self.text_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=15)
            self.text_area.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Configure buttons
            button_frame = ttk.Frame(self.window)
            button_frame.pack(fill="x", padx=10, pady=5)
            
            self.submit_btn = ttk.Button(button_frame, text="Importar Referências", command=self.import_references, style='Accent.TButton')
            self.submit_btn.pack(side="left", padx=5)
            
            self.clear_btn = ttk.Button(button_frame, text="Limpar", command=self.clear_text)
            self.clear_btn.pack(side="left", padx=5)
            
            # Configure status
            self.status_var = tk.StringVar()
            self.status_label = ttk.Label(self.window, textvariable=self.status_var, wraplength=780)
            self.status_label.pack(pady=5)
            
            # Configurar estilo para botão de destaque
            style = ttk.Style()
            style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
            
        except Exception as e:
            self.show_error("Erro na configuração da UI", str(e))
    
    def show_error(self, title, message):
        """Mostra uma mensagem de erro"""
        print(f"ERRO - {title}: {message}")
        print(traceback.format_exc())
        messagebox.showerror(title, f"{message}\n\nVerifique o console para mais detalhes.")
    
    def load_credentials(self):
        """Load saved credentials if they exist"""
        try:
            if os.path.exists('zotero_credentials.json'):
                print("Arquivo de credenciais encontrado")
                with open('zotero_credentials.json', 'r', encoding='utf-8') as f:
                    creds = json.load(f)
                    print("Credenciais carregadas do arquivo")
                    
                    # Verificar se os widgets existem
                    if all(hasattr(self, attr) for attr in ['library_id', 'api_key', 'openai_key', 'firecrawl_key']):
                        # Limpar entradas existentes
                        for widget in [self.library_id, self.api_key, self.openai_key, self.firecrawl_key]:
                            if widget and widget.winfo_exists():
                                widget.delete(0, tk.END)
                        
                        # Inserir novos valores
                        self.library_id.insert(0, creds.get('library_id', ''))
                        self.api_key.insert(0, creds.get('api_key', ''))
                        self.openai_key.insert(0, creds.get('openai_key', ''))
                        self.firecrawl_key.insert(0, creds.get('firecrawl_key', ''))
                        
                        print("Credenciais inseridas nos campos")
                        self.status_var.set("Credenciais carregadas com sucesso!")
                    else:
                        raise Exception("Widgets de credenciais não inicializados corretamente")
            else:
                print("Arquivo de credenciais não encontrado")
                self.status_var.set("Arquivo de credenciais não encontrado")
        except Exception as e:
            self.show_error("Erro ao carregar credenciais", str(e))
    
    def save_credentials(self):
        """Save credentials for future use"""
        try:
            if not all(hasattr(self, attr) for attr in ['library_id', 'api_key', 'openai_key', 'firecrawl_key']):
                raise Exception("Widgets de credenciais não inicializados")
                
            creds = {
                'library_id': self.library_id.get(),
                'api_key': self.api_key.get(),
                'openai_key': self.openai_key.get(),
                'firecrawl_key': self.firecrawl_key.get()
            }
            
            with open('zotero_credentials.json', 'w', encoding='utf-8') as f:
                json.dump(creds, f, indent=4)
            print("Credenciais salvas com sucesso")
            self.status_var.set("Credenciais salvas com sucesso!")
        except Exception as e:
            self.show_error("Erro ao salvar credenciais", str(e))
    
    def clear_text(self):
        """Clear the text area"""
        self.text_area.delete('1.0', tk.END)
        self.status_var.set("")
    
    def parse_references(self, text):
        """Analisa as referências usando OpenAI e retorna JSON estruturado"""
        client = OpenAI(api_key=self.openai_key.get())
        
        prompt_template = f"""
        Analise as referências bibliográficas abaixo e converta em um JSON estruturado para o Zotero.
        
        Regras importantes:
        1. Determine o tipo correto do item (itemType):
           - "journalArticle" para artigos de periódicos
           - "book" para livros
           - "bookSection" para capítulos de livros
           - "thesis" para teses e dissertações
           - "conferencePaper" para trabalhos em eventos
        
        2. Para autores, use SEMPRE o formato:
           "creators": [
              {{"creatorType": "author", "firstName": "Nome", "lastName": "Sobrenome"}}
           ]
        
        3. Campos obrigatórios por tipo:
           - Para journalArticle:
             "title", "creators", "date", "publicationTitle", "volume", "issue", "pages"
           - Para book:
             "title", "creators", "date", "publisher", "place"
           - Para bookSection:
             "title", "creators", "bookTitle", "publisher", "date"
           - Para thesis:
             "title", "creators", "date", "university", "thesisType"
           - Para conferencePaper:
             "title", "creators", "date", "conferenceName", "place"
        
        4. Regras adicionais:
           - Não inclua campos vazios
           - Use o campo "language" apenas se tiver certeza
           - Extraia o DOI se disponível
           - Mantenha datas no formato YYYY-MM-DD ou YYYY
           - Para páginas, use o formato "1-10" ou apenas "1" se for página única
        
        Referências para processar:
        {text}
        
        Retorne APENAS o JSON, sem explicações ou comentários.
        """

        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[{"role": "user", "content": prompt_template}]
            )
            
            parsed_data = json.loads(response.choices[0].message.content)
            return parsed_data if isinstance(parsed_data, list) else [parsed_data]
            
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar JSON da resposta do OpenAI: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao analisar referências com OpenAI: {str(e)}")
    
    def create_zotero_items(self, items):
        """Create items in Zotero"""
        zot = zotero.Zotero(self.library_id.get(), 'user', self.api_key.get())
        
        if not items:
            raise Exception("Nenhum item válido para criar no Zotero.")
        
        # Process in batches of 50 (API limit)
        BATCH_SIZE = 50
        current_batch = []
        results = []
        
        # Get valid fields for items
        valid_fields = {}
        try:
            item_types = zot.item_types()
            for item_type in item_types:
                type_fields = zot.item_type_fields(item_type['itemType'])
                valid_fields[item_type['itemType']] = [field['field'] for field in type_fields]
        except Exception as e:
            raise Exception(f"Erro ao obter campos válidos do Zotero: {str(e)}")
        
        for idx, item in enumerate(items, start=1):
            try:
                # Get item type, default to 'journalArticle' if not specified
                item_type = item.get('itemType', 'journalArticle')
                
                # Create a new template for this item type
                template = zot.item_template(item_type)
                
                # Only copy valid fields for this item type
                if item_type in valid_fields:
                    valid_item_fields = valid_fields[item_type]
                    for field, value in item.items():
                        if field in valid_item_fields:
                            template[field] = value
                        elif field == 'creators':
                            # Handle creators separately as they have a special structure
                            template['creators'] = value
                
                current_batch.append(template)
                
                if (idx % BATCH_SIZE == 0) or (idx == len(items)):
                    try:
                        zot.check_items(current_batch)
                        result = zot.create_items(current_batch)
                        results.append(result)
                    except Exception as e:
                        raise Exception(f"Erro ao criar lote de itens no Zotero: {str(e)}")
                    current_batch = []
            
            except Exception as e:
                print(f"Aviso: Erro ao processar item {idx}: {str(e)}")
                continue
        
        return results
    
    def generate_firecrawl_query(self, text):
        """Gera URLs para o Firecrawl usando OpenAI"""
        client = OpenAI(api_key=self.openai_key.get())
        
        prompt_template = f"""
        A partir das referências abaixo, identifique e retorne a URL do documento acadêmico.
        Se houver múltiplas referências, retorne apenas a URL mais relevante.
        Priorize URLs de repositórios acadêmicos (ex: scielo.org, researchgate.net, academia.edu).
        Se não encontrar uma URL específica, retorne a URL da página principal do periódico ou instituição.

        Referências:
        {text}

        Retorne APENAS a URL, sem explicações ou formatação adicional.
        """

        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[{"role": "user", "content": prompt_template}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Erro ao gerar URL para Firecrawl: {str(e)}")

    def fetch_firecrawl_data(self, query):
        """Busca dados usando Firecrawl"""
        try:
            app = FirecrawlApp(api_key=self.firecrawl_key.get())
            print(f"Buscando URL: {query}")
            
            # Primeiro fazemos um scrape da URL
            results = app.scrape_url(
                query,
                params={
                    'formats': ['markdown', 'json'],
                    'jsonOptions': {
                        'prompt': 'Extraia os metadados acadêmicos desta página, incluindo: título, autores, data, DOI, abstract, palavras-chave e informações de publicação.'
                    }
                }
            )
            
            print(f"Resultado do Firecrawl: {json.dumps(results, indent=2)}")
            
            # Organizando os dados retornados
            data = results.get('data', {})
            json_data = data.get('json', {})
            
            # Converter autores para o formato do Zotero
            creators = []
            if 'authors' in json_data:
                for author in json_data['authors']:
                    name_parts = author['name'].split()
                    if len(name_parts) > 1:
                        creators.append({
                            'creatorType': 'author',
                            'firstName': ' '.join(name_parts[:-1]),
                            'lastName': name_parts[-1]
                        })
                    else:
                        creators.append({
                            'creatorType': 'author',
                            'firstName': '',
                            'lastName': name_parts[0]
                        })
            
            # Construir metadados formatados
            metadata = {
                'title': json_data.get('title', ''),
                'abstractNote': json_data.get('abstract', ''),
                'url': query,
                'language': data.get('language', ''),
                'creators': creators,
                'date': json_data.get('date', ''),
                'extra': ''
            }
            
            # Adicionar informações de publicação
            pub_info = json_data.get('publication_info', {})
            if pub_info:
                metadata['publisher'] = pub_info.get('publisher', '')
                metadata['edition'] = pub_info.get('edition', '')
                if 'print_year' in pub_info:
                    metadata['date'] = str(pub_info['print_year'])
                
                # Adicionar informações adicionais ao campo extra
                extra_info = []
                if pub_info.get('online_version'):
                    extra_info.append(f"Versão online: {pub_info['online_version']}")
                if pub_info.get('available_from'):
                    extra_info.append(f"Disponível em: {pub_info['available_from']}")
                if extra_info:
                    metadata['extra'] = '\n'.join(extra_info)
            
            # Adicionar palavras-chave
            if 'keywords' in json_data:
                metadata['tags'] = [{'tag': kw} for kw in json_data['keywords']]
            
            # Adicionar conteúdo markdown como nota se disponível
            if 'markdown' in data:
                metadata['notes'] = [{'note': data['markdown']}]
            
            return metadata
            
        except Exception as e:
            print(f"Erro detalhado do Firecrawl: {str(e)}")
            raise Exception(f"Erro ao buscar dados via Firecrawl: {str(e)}")

    def merge_reference_data(self, openai_json, firecrawl_data):
        """Mescla dados do OpenAI com dados do Firecrawl"""
        client = OpenAI(api_key=self.openai_key.get())
        
        merge_prompt = f"""
        Mescle os dois conjuntos de dados em um único JSON para Zotero.
        Mantenha a estrutura do Zotero e priorize dados mais completos.
        
        Regras importantes:
        1. Mantenha o itemType original do OpenAI
        2. Preserve todos os creators do OpenAI, mas adicione novos do Firecrawl se não existirem
        3. Use os dados do Firecrawl para enriquecer:
           - title se mais completo
           - abstractNote para o resumo
           - url da fonte
           - DOI se disponível
           - tags para palavras-chave
           - notes para conteúdo adicional
           - extra para informações complementares
        4. Para campos conflitantes, use a versão mais completa
        5. Mantenha apenas campos válidos do Zotero

        Dados OpenAI:
        {json.dumps(openai_json, ensure_ascii=False)}

        Dados Firecrawl:
        {json.dumps(firecrawl_data, ensure_ascii=False)}

        Retorne APENAS o JSON mesclado, sem explicações.
        """

        try:
            response = client.chat.completions.create(
                model="o1",
                messages=[{"role": "user", "content": merge_prompt}]
            )
            merged_data = json.loads(response.choices[0].message.content)
            return merged_data if isinstance(merged_data, list) else [merged_data]
        except Exception as e:
            raise Exception(f"Erro ao mesclar dados: {str(e)}")

    def import_references(self):
        """Import references to Zotero"""
        if not all([self.library_id.get(), self.api_key.get(), self.openai_key.get(), self.firecrawl_key.get()]):
            self.status_var.set("Por favor, insira todas as credenciais (Zotero, OpenAI e Firecrawl)")
            return
        
        try:
            text = self.text_area.get('1.0', tk.END).strip()
            if not text:
                self.status_var.set("Por favor, insira algumas referências")
                return
            
            # Passo 1: Parse inicial com OpenAI
            self.status_var.set("Analisando referências com OpenAI...")
            self.window.update()
            openai_parsed = self.parse_references(text)
            
            # Passo 2: Gerar query e buscar no Firecrawl
            self.status_var.set("Buscando dados complementares via Firecrawl...")
            self.window.update()
            firecrawl_query = self.generate_firecrawl_query(text)
            firecrawl_data = self.fetch_firecrawl_data(firecrawl_query)
            
            # Passo 3: Mesclar dados
            self.status_var.set("Mesclando dados...")
            self.window.update()
            merged_items = self.merge_reference_data(openai_parsed, firecrawl_data)
            
            # Passo 4: Criar no Zotero
            self.status_var.set(f"Criando {len(merged_items)} itens no Zotero...")
            self.window.update()
            results = self.create_zotero_items(merged_items)
            
            self.save_credentials()
            
            total_success = sum(len(result.get('success', {})) for result in results)
            self.status_var.set(f"Importados com sucesso: {total_success} referências")
            
        except Exception as e:
            self.status_var.set(f"Erro: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ZoteroImporter()
    app.run()
