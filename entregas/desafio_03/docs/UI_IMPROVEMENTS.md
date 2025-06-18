# 🤖 CSV Agent Pro - Metadron

Interface aprimorada do CSV Agent com funcionalidades avançadas de análise e visualização.

## ✨ Novas Funcionalidades

### 🎨 Interface Moderna

- **Design responsivo** com gradientes e animações
- **Dashboard lateral** com estatísticas em tempo real
- **Métricas visuais** e indicadores de status
- **Tema customizado** com cores do projeto

### 📊 Análise Avançada

- **Múltiplos modos de análise**:
  - 📊 Arquivo Individual
  - 🔗 Múltiplos Arquivos (comparação)
  - 📈 Dashboard Geral
- **Visualizações interativas** com Plotly
- **Estatísticas descritivas** completas
- **Matriz de correlação** para dados numéricos

### 🔧 Funcionalidades Técnicas

- **Upload múltiplo** de arquivos
- **Amostragem inteligente** configurável
- **Modo debug** para desenvolvedores
- **Export de dados** processados
- **Cache e limpeza** automática

### 💡 UX Melhorada

- **Sugestões de perguntas** contextuais
- **Progress bars** para uploads
- **Feedback visual** em tempo real
- **Tooltips** explicativos
- **Shortcuts** para análises comuns

## 🚀 Como usar

### Versão Original

```bash
streamlit run streamlit_app.py
```

### Versão Avançada

```bash
streamlit run streamlit_app_advanced.py
```

## 📦 Dependências Adicionais

A versão avançada requer:

- `plotly` - Gráficos interativos
- `seaborn` - Visualizações estatísticas
- `matplotlib` - Gráficos complementares

## 🎯 Principais Melhorias

### 1. **Design System Completo**

- CSS customizado com variáveis
- Componentes reutilizáveis
- Paleta de cores consistente
- Microinterações e hover effects

### 2. **Dashboard Avançado**

- Sidebar com controles
- Métricas em tempo real
- Status do sistema
- Configurações personalizáveis

### 3. **Análise Multi-Arquivo**

- Comparação side-by-side
- Análise cruzada
- Estatísticas agregadas
- Visualizações comparativas

### 4. **Visualizações Interativas**

- Histogramas dinâmicos
- Box plots informativos
- Matriz de correlação
- Gráficos de dispersão

### 5. **UX Inteligente**

- Auto-complete para perguntas
- Sugestões contextuais
- Feedback de progresso
- Error handling elegante

## 🛠️ Configurações Avançadas

### Sidebar Controls

- **Sample Size**: Controla quantas linhas são enviadas para a IA
- **Debug Mode**: Mostra informações técnicas detalhadas
- **Cache Control**: Gerenciamento de memória e arquivos temporários

### Modos de Análise

1. **Individual**: Foco em um arquivo específico
2. **Comparativo**: Análise de múltiplos arquivos
3. **Dashboard**: Visão geral de todos os dados

### Tipos de Pergunta

- **Estruturais**: Sobre a organização dos dados
- **Estatísticas**: Cálculos e agregações
- **Qualitativas**: Insights e interpretações
- **Comparativas**: Entre diferentes datasets

## 📊 Screenshots das Melhorias

### Header Moderno

- Gradiente personalizado
- Badges informativos
- Layout responsivo

### Dashboard Lateral

- Métricas em tempo real
- Dicas contextuais
- Links úteis
- Controles avançados

### Análise Multi-Tab

- Dados, Informações, Estatísticas, Gráficos
- Visualizações interativas
- Export de dados
- Comparações visuais

## 🎨 Customização

### Cores do Tema

```css
--primary: #667eea
--secondary: #764ba2
--success: #28a745
--info: #17a2b8
--warning: #ffc107
--danger: #dc3545
```

### Componentes Personalizados

- `main-header`: Header principal com gradiente
- `step-header`: Cabeçalhos de seção
- `answer-box`: Caixa de resposta da IA
- `file-card`: Cards de arquivo
- `stat-box`: Métricas visuais

## 🔄 Migração

Para migrar da versão original para a avançada:

1. **Instale dependências**:

   ```bash
   pip install plotly seaborn matplotlib
   ```

2. **Use o novo arquivo**:

   ```bash
   streamlit run streamlit_app_advanced.py
   ```

3. **Configure conforme necessário** na sidebar

## 🚀 Roadmap

Próximas funcionalidades planejadas:

- [ ] Análise de texto com NLP
- [ ] Export para múltiplos formatos
- [ ] Dashboards salvos
- [ ] Histórico de análises
- [ ] API REST para integração
- [ ] Modo offline com modelos locais

---

**Desenvolvido pela equipe Metadron para o curso I2A2** 🚀
