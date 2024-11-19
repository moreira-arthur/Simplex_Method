
# README

## Descrição

Este projeto implementa o algoritmo Simplex para resolver problemas de programação linear. Além disso, a biblioteca `scipy` é utilizada para comparar os resultados da implementação personalizada do Simplex com a função `linprog` do `scipy`.

## Estrutura do Projeto
- `simplex.py`: Contém a implementação do algoritmo Simplex e funções auxiliares para leitura de dados, padronização de matrizes e execução do algoritmo.
- `input.txt`: Arquivo de entrada contendo os coeficientes da função objetivo, a matriz de restrições e os valores das restrições.

## Dependências

- `numpy`
- `scipy`
- `argparse`
- `logging`
- `ast`

## Como Executar

1. Certifique-se de ter todas as dependências instaladas. Você pode instalá-las usando `pip`:
    ```bash
    pip install numpy scipy
    ```

2. Prepare um arquivo de entrada no formato `input.txt` com o seguinte conteúdo:
    ```
    c = [coeficientes da função objetivo]
    A = [matriz de coeficientes das restrições]
    b = [valores das restrições]
    ```

3. Execute o script `simplex.py` passando o nome do arquivo de entrada (sem a extensão `.txt`):
    ```bash
    python simplex.py input
    ```

## Comparação com Scipy

A biblioteca `scipy` é utilizada para comparar os resultados da implementação personalizada do Simplex com a função `linprog`. Os resultados de ambas as implementações são registrados em um arquivo de log para análise.


## Uso

O script `simplex.py` lê os dados de entrada de um arquivo de texto, executa o algoritmo Simplex e a função `linprog` da biblioteca `scipy`, e salva os resultados em arquivos de log. Ele também imprime um resumo dos resultados no terminal.

## Executando o Script

Para executar o script, use o seguinte comando no terminal, fornecendo o nome do arquivo de entrada (sem a extensão `.txt`) e o tipo de problema (`upper` para upperbound ou `equal` para forma padrão):

```bash
python simplex.py nome_do_arquivo tipo_de_problema
```

Por exemplo, se o arquivo de entrada for `entrada_1_success.txt` e o tipo de problema for `upper`, execute:

```bash
python simplex.py entrada_1_success upper
```


## Formato do Arquivo de Entrada

O arquivo de entrada contém os dados do problema no formato de desigualdade de limite superior (upper bound), com a restrição adicional de não negatividade nas variáveis. O problema está configurado da seguinte forma:
minimizar $`c^T \cdot x`$

sujeito a:

$`A \cdot x \leq b`$

$`x \geq 0`$

onde:

- \( c \) é o vetor de coeficientes da função objetivo,
- \( A \) é a matriz de coeficientes das restrições,
- \( b \) é o vetor de limites superiores para cada restrição,
- \( x \) representa as variáveis de decisão, que devem ser não-negativas.

O arquivo de entrada deve estar no formato:

```
c = [coeficientes da função objetivo]
A = [[coeficientes das restrições]]
b = [termos independentes das restrições]
```


## Exemplo de Arquivo de Entrada

Aqui está um exemplo de arquivo de entrada (`entrada_1_success.txt`):

```
c = [1, 2, 3]
A = [[1, 1, 0], [0, 1, 1]]
b = [2, 3]
```

## Saída

O script cria um arquivo de log com o nome do arquivo de entrada seguido de `_output.log`. Por exemplo, para o arquivo de entrada `entrada_1_success.txt`, o arquivo de log será `entrada_1_success_output.log`.

O log contém informações detalhadas sobre as iterações do algoritmo Simplex e os resultados da função `linprog` da biblioteca `scipy`.

Além disso, o script imprime no terminal um resumo dos resultados, incluindo o valor ótimo, o número de iterações e o status da solução.


## Estrutura do Código

- `configure_logger(filename: str)`: Configura o logger para usar um arquivo de log específico.
- `read_input_from_file(filename: str)`: Lê os dados de entrada para o algoritmo Simplex a partir de um arquivo de texto.
- `standardizing(constraint_matrix, constraint_values, objective_coefficients)`: Padroniza as matrizes e vetores para o algoritmo Simplex.
- `simplex_iteration(constraint_matrix, constraint_values, objective_coefficients, num_constraints: int, num_variables: int)`: Executa iterações do algoritmo Simplex.
- `simplex(constraint_matrix, constraint_values, objective_coefficients, standard_form=True)`: Executa o algoritmo Simplex.
- `linprog_run(filename: str, standard_form=True)`: Executa o algoritmo Simplex usando a biblioteca `scipy`.
- `run_and_log(filename: str, standard_form: bool = True)`: Configura o logger e executa `simplex_run` e `linprog_run` com base no arquivo de entrada.
- `simplex_run(filename: str, standard_form=True)`: Executa o algoritmo Simplex com base nos dados de entrada de um arquivo.

## Funções do Código

### `configure_logger(filename: str)`

Configura o logger para usar um arquivo de log específico.

**Parâmetros:**

- `filename`: Nome do arquivo de log.

### `read_input_from_file(filename: str)`

Lê os dados de entrada para o algoritmo Simplex a partir de um arquivo de texto.

**Parâmetros:**

- `filename`: Nome do arquivo de entrada.

**Retorna:**

- `c`, `A`, `b` como `numpy.ndarray`

### `standardizing(constraint_matrix, constraint_values, objective_coefficients)`

Padroniza as matrizes e vetores para o algoritmo Simplex.

**Parâmetros:**

- `constraint_matrix`: Matriz de coeficientes das restrições.
- `constraint_values`: Vetor de termos independentes das restrições.
- `objective_coefficients`: Vetor de coeficientes da função objetivo.

**Retorna:**

- Matrizes e vetores padronizados.

### `simplex_iteration(constraint_matrix, constraint_values, objective_coefficients, num_constraints: int, num_variables: int)`

Executa iterações do algoritmo Simplex.

**Parâmetros:**

- `constraint_matrix`: Matriz de coeficientes das restrições.
- `constraint_values`: Vetor de termos independentes das restrições.
- `objective_coefficients`: Vetor de coeficientes da função objetivo.
- `num_constraints`: Número de restrições.
- `num_variables`: Número de variáveis.

**Retorna:**

- Valor ótimo, solução ótima, custos reduzidos, status e número de iterações.

### `simplex(constraint_matrix, constraint_values, objective_coefficients, standard_form=True)`

Executa o algoritmo Simplex.

**Parâmetros:**

- `constraint_matrix`: Matriz de coeficientes das restrições.
- `constraint_values`: Vetor de termos independentes das restrições.
- `objective_coefficients`: Vetor de coeficientes da função objetivo.
- `standard_form`: Booleano indicando se o problema está na forma padrão.

### `linprog_run(filename: str, standard_form=True)`

Executa o algoritmo Simplex usando a biblioteca `scipy`.

**Parâmetros:**

- `filename`: Nome do arquivo de entrada.
- `standard_form`: Booleano indicando se o problema está na forma padrão.

### `run_and_log(filename: str, standard_form: bool = True)`

Configura o logger e executa `simplex_run` e `linprog_run` com base no arquivo de entrada.

**Parâmetros:**

- `filename`: Nome do arquivo de entrada.
- `standard_form`: Booleano indicando se o problema está na forma padrão.

### `simplex_run(filename: str, standard_form=True)`

Executa o algoritmo Simplex com base nos dados de entrada de um arquivo.

**Parâmetros:**

- `filename`: Nome do arquivo de entrada.
- `standard_form`: Booleano indicando se o problema está na forma padrão.


## Autor

Arthur Moreira Correa