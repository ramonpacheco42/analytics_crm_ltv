**# Sobre o Projeto**
# Introdução
O Customer Lifetime Value (CLTV) muitas vezes é usado para medir o valor vitalício que um cliente gasta na sua vida de relacionamento com a empresa e também com uma visão do lucro líquido que aquele relacionamento trouxe a empresa. O CLTV é uma métrica crítica pois representa o valor máximo que se espera que os clientes gastem para adquirir novos produtos. Para aderencia de um bom resultado é essencial cruzar com as despesas de Custo de Aquisição de Clientes(CAC).

## Definição do Projeto

O valor presente dos fluxos de caixa futuros atribuídos ao cliente durante toda a sua relação com a empresa!

Esta conta representa um único período de tempo. Representa o momento em que a análise foi realizada. Vou dar uma projeção para que possamos avaliar a questão com projeções de 3 meses e 6 meses.

Como posso fazer minha inferência? Vamos realizar o valor vitalício com projeções de médio e longo prazo para indivíduos, incluindo o padrão específico de toda a população, extraindo a distribuição de probabilidade condicional e generalizando-as em termos das características de um indivíduo específico.

![CLTV](https://user-images.githubusercontent.com/74688664/235321212-fcea6e56-e3e7-4b1d-be13-1787ed4b2d28.png)

# Formulas

Estimativa probabilística do valor vitalício com projeção de tempo

CLTV = (Valor do Cliente / Churn Rate) * Margem de Lucro

Valor do Cliente = Frequência de Compra * Valor Médio de Compra

CLTV = Número Esperado de Transações * Lucro Médio Esperado

Acima, a frequência de compra e o número de transações significam a mesma coisa. Da mesma forma, o Valor Médio de Compra e o Lucro Médio significam a mesma coisa. Eles diferem com a parte "Esperada" que acontece com eles.

# Aviso

Será adicionada uma distribuição probabilística. A declaração "Esperado" refere-se a essa parte. Número esperado de compras, lucratividade esperada.

BG/NBD = Gama de transações esperada, Gama de lucro esperada.

# Como será estimado o modelo estatístico 

Vamos adicionar estatísticas e padrões de probabilidade à fórmula acima. Haverá modelos BG/NBD e Gama Gama que farão isso acontecer para nós. Esses modelos farão uma coisa, que é modelar o comportamento de compra de todos os clientes desta empresa. Após modelar o comportamento de compra de todos os clientes, eles substituirão as características pessoais do indivíduo neste modelo e reduzirão o número esperado de vendas para a pessoa, seguindo o padrão geral do público.

Os modelos BG/NBD e Gama Gama são modelos estatísticos, não modelos de aprendizado de máquina. Na verdade, esses modelos têm a expressão "Condicional" no início.

# Problema de Negócio

Uma empresa de comércio eletrônico deseja segmentar seus clientes e determinar estratégias de marketing de acordo com esses segmentos. Por exemplo, deseja-se organizar campanhas diferentes para novos clientes e campanhas diferentes para reter clientes que são muito rentáveis para a empresa.



