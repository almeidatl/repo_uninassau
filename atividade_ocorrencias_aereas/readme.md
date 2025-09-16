### Dashboard de Ocorrências Aeronáuticas (CENIPA)

Este projeto é um dashboard interativo em Python/Streamlit para explorar dados de ocorrências aeronáuticas (acidentes, incidentes e recomendações).

### Requisitos
- Python 3.11+ (recomendado)
- Windows PowerShell (ou terminal equivalente)

### Instalação
1. Crie um ambiente virtual e ative:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Atualize o pip e instale dependências:
```powershell
python -m pip install -U pip
pip install -r requirements.txt
```

### Execução
Inicie o app:
```powershell
streamlit run app.py
```
Abra o link exibido (ex.: http://localhost:8501).

### Funcionalidades
- KPIs: total de ocorrências, acidentes, incidentes, recomendações.
- Filtros: período (data), UF e classificação.
- Visualizações:
  - Série temporal por mês.
  - Mapa de ocorrências (quando houver latitude/longitude).
  - Barras por UF, tipo de evento, fabricante e modelo de aeronave.
  - Histograma de variáveis numéricas (ex.: fatalidades, assentos, PMD).
- Visualização do modelo de dados (`modelo_dados.webp`).

### Dados de entrada
- Arquivos CSV no mesmo diretório do `app.py`:
  - `ocorrencia.csv`
  - `aeronave.csv`
  - `ocorrencia_tipo.csv`
  - `recomendacao.csv`
  - `fator_contribuinte.csv`
- Leitura com separador `;` e codificação `latin-1`.
- Colunas chave coalescidas para `codigo` e normalizadas para string antes de junções.

### Observações
- Se o mapa mostrar poucos pontos, pode haver faltas de coordenadas em várias linhas; os demais gráficos continuarão funcionando.
- Caso haja problemas de acentuação, confirme que os CSVs estão em `latin-1`.

### Solução de problemas
- Erro de merge (tipos diferentes em `codigo`): já tratado no app convertendo para string. Se persistir, limpe o cache do Streamlit pelo menu “Rerun”/“Clear cache”.
- Porta ocupada: use outra porta, por exemplo:
```powershell
streamlit run app.py --server.port 8502
```
- Ambiente virtual não ativa: rode o PowerShell como Administrador ou habilite scripts:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Licença
Uso acadêmico/educacional. Ajuste conforme sua necessidade.