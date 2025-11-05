# Análise de Sentimento - Azure Language Studio

## 📊 Visão Geral
Este documento apresenta os resultados da análise de sentimento realizada no Azure Language Studio sobre a transcrição de uma aula sobre Azure Speech Studio. A análise foi realizada para demonstrar a capacidade do serviço em identificar sentimentos em texto transcrito.

## 🔍 Metodologia

### Fonte e Preparação
- **Origem**: Transcrição de áudio de uma aula sobre Azure Speech Studio
- **Formato**: Texto em português do Brasil
- **Duração**: Aproximadamente 10 minutos de áudio transcrito
- **Contexto**: Aula técnica sobre funcionalidades do Azure

### Ferramenta Utilizada
- **Serviço**: Azure Language Studio
- **Recurso**: Análise de Sentimento e Mineração de Opinião
- **Versão**: Azure AI Language 2023
- **Tipo de Análise**: Análise de Sentimento por Frase

### Métricas Analisadas
- **Sentimento Geral**: Classificação em Positivo, Neutro ou Negativo
- **Pontuação**: Percentual de confiança para cada classificação (0-100%)
- **Granularidade**: Análise individual por frase
- **Critérios**: Contexto, tom e escolha de palavras

## 📈 Resultados da Análise

### 📝 Legenda dos Sentimentos
- 😊 **Positivo**: Indica sentimento positivo (confiança, satisfação, aprovação)
- 😐 **Neutro**: Indica tom neutro ou informativo
- ☹️ **Negativo**: Indica sentimento negativo (insatisfação, dúvida, problema)

### 📊 Análise Detalhada por Frase

| ID | Texto Analisado | Sentimento | Pontuação (%) |
|:--:|----------------|:-----------:|---------------|
| 01 | Então vamos iniciar aqui a nosso laboratório falando um pouquinho sobre a exploração do estúdio de fala. | 😐 Neutro | P: 3% N: 96% Neg: 1% |
| 09 | Do áudio pra escrita, como é escrita para o próprio áudio, isso é muito legal. | 😊 Positivo | P: 98% N: 2% Neg: 0% |
| 33 | Trazer aqui muito mais informação a partir daí, beleza, gostei, funciona... | � Positivo | P: 100% N: 0% Neg: 0% |
| 14 | E a partir daí, meu, que ele já está aparecendo para mim, que eu não tenho nenhum trabalho criado e tudo mais. | 😐 Neutro | P: 0% N: 73% Neg: 27% |

> **Nota**: Esta é uma seleção representativa das 60 frases analisadas. Os exemplos foram escolhidos para demonstrar diferentes níveis de sentimento.

### 📊 Resumo da Análise
- Total de frases analisadas: 60
- Distribuição de sentimentos:
  - 😊 Frases positivas: 13 (21.7%)
  - 😐 Frases neutras: 47 (78.3%)
  - ☹️ Frases negativas: 0 (0%)

### 🔍 Observações Importantes
1. A maioria das frases possui tom neutro, típico de conteúdo educacional
2. Momentos positivos coincidem com demonstrações de funcionalidades
3. Ausência de sentimentos fortemente negativos indica boa qualidade do material
4. Alta porcentagem de neutralidade é apropriada para material instrucional

### ⭐ Destaques da Análise

#### Frases Mais Positivas
1. "Trazer aqui muito mais informação a partir daí, beleza, gostei, funciona..." (100% positivo)
2. "Do áudio pra escrita, como é escrita para o próprio áudio, isso é muito legal." (98% positivo)
3. "Curtas horas tem grátis, alguns serviços ofertam isso, né?" (100% positivo)

#### Frases Mais Neutras
1. "Como que a gente vai fazer o login?" (100% neutro)
2. "Aqui está o áudio." (97% neutro)
3. "Depois você só vem aqui no X. Fechou." (100% neutro)

#### Padrões Observados
- Frases positivas geralmente aparecem após demonstrações bem-sucedidas
- Instruções técnicas tendem a ser mais neutras
- Explicações de funcionalidades apresentam um mix de neutralidade e positividade

### 🎯 Conclusão
A análise demonstra que o conteúdo mantém um tom profissional e educativo adequado, com momentos positivos bem distribuídos durante as demonstrações práticas. O predomínio de sentimentos neutros é apropriado para material instrucional, garantindo clareza e objetividade na transmissão do conhecimento.