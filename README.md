# 🎥 Interactive Media Evolution and Recommendation

Este projeto tem como objetivo simular dados de uso de uma plataforma de mídia interativa ainda em desenvolvimento, e com base nesses dados, desenvolver e testar algoritmos de recomendação de conteúdo.

---

## 📊 Objetivo

1. **Gerar dados de comportamento de usuários** fictícios ou reais (quando disponíveis).
2. **Construir pipelines de dados** para processar e transformar os dados em features úteis.
3. **Treinar e avaliar algoritmos de recomendação** com base nesses dados.

---

## 🗂 Estrutura do Projeto
data/ 
├── behavior_generated/ # Dados simulados 
├── behavior_imported/ # Dados reais (importados) 
├── tables/ # Dados auxiliares (como países) 
└── words/ # Vocabulário ou conteúdo textual

src/ 
├── creators/ # Scripts que criam entidades (usuários, conteúdos, etc.) 
├── generators/ # Geração de dados e features 
│   └───feature_generators/ # Subconjunto focado em geração de atributos derivados 
├── initialization/ # Inicialização e preparação dos dados 
├── recommendation/ # Algoritmos de recomendação 
├── utils/ # Funções auxiliares 
└── main.py # (opcional) ponto de entrada do sistema

---

## 🔗 Dados Utilizados

### 💤 Sleep Data
Baseado em dados públicos de [SleepCycle](https://sandman.sleepcycle.com/data), coletados em **04/05/2025**.

### 🌍 Country Data
Baseado em dados do [GeoNames](https://download.geonames.org/export/dump/countryInfo.txt), baixados em **05/05/2025**.

---