# Meu Caderno de Receitas

Caderno de receitas digital interativo assistido pelo **Hermes Agent**.

## Como Funciona

- **Interface Web:** Single Page Application construída com Tailwind CSS.
- **Categorias:** Filtro por `refeicao`, `lanche` e `sobremesa`.
- **Modo Cozinha:** Checklist com ingredientes interativos para riscar enquanto prepara o prato.
- **Alimentação Exclusiva via Telegram:** As receitas são enviadas diretamente para o Hermes no Telegram (link do Instagram, YouTube, TikTok ou texto). O Hermes extrai os dados, categoriza, aplica as notas e cadastra no `receitas.json` automaticamente.

## Regras de Classificação do Hermes

- `category`: `refeicao` (almoço/jantar), `lanche` (pães, salgados, cafés) ou `sobremesa` (doces, bolos, tortas).
- `isCooked`: Padrão `false`. Se o usuário disser *"acabei de fazer"* ou *"ficou ótima"*, define como `true`.
- `rating`: Se o usuário disser *"dou nota 5"*, grava 5 estrelas. Caso contrário, define 0.

## Estrutura do Projeto

- `index.html`: Interface web completa.
- `receitas.json`: Base de dados das receitas em JSON.
- `add_recipe.py`: Script de adição e versionamento automatizado.
