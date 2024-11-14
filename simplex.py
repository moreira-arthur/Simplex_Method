import numpy as np
import ast  # para interpretar strings no formato de lista diretamente
from scipy.optimize import linprog
from numpy.linalg import inv
import logging
import argparse

def configure_logger(filename: str) -> None:
    """
    Configura o logger para usar um arquivo de log específico.
    :param filename: Nome do arquivo de log.
    """
    filename = filename.split('.')[0]
    log_filename = f"{filename}_output.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')

def read_input_from_file(filename):
    """
    Lê os dados de entrada para o algoritmo Simplex a partir de um arquivo de texto.
    :param filename: Nome do arquivo de entrada.
    :return: c, A, b como numpy.ndarray
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        objective_coefficients = ast.literal_eval(lines[0].strip().split('=')[1])
        constraint_matrix = ast.literal_eval(lines[1].strip().split('=')[1])
        constraint_values = ast.literal_eval(lines[2].strip().split('=')[1])
    return np.array(objective_coefficients), np.array(constraint_matrix), np.array(constraint_values)

def standardizing(constraint_matrix, constraint_values, objective_coefficients) -> tuple:
    """
    Padroniza as matrizes e vetores para o algoritmo Simplex.
    :param constraint_matrix: Matriz de coeficientes das restrições.
    :param constraint_values: Vetor de termos independentes das restrições.
    :param objective_coefficients: Vetor de coeficientes da função objetivo.
    :return: Matrizes e vetores padronizados.
    """
    num_constraints = constraint_matrix.shape[0]
    num_variables = constraint_matrix.shape[1]

    # Criar matriz identidade para variáveis artificiais
    identity_matrix = np.eye(num_constraints)

    # Concatenar matriz identidade à matriz de restrições
    augmented_constraint_matrix = np.hstack((constraint_matrix, identity_matrix))

    # Ajustar vetor de custos para incluir variáveis artificiais
    augmented_objective_coefficients = np.hstack((objective_coefficients, np.zeros(num_constraints)))
    return augmented_constraint_matrix, constraint_values, augmented_objective_coefficients, num_constraints, num_variables

def simplex_iteration(constraint_matrix, constraint_values, objective_coefficients, num_constraints: int, num_variables: int):
    """
    Executa iterações do algoritmo Simplex.
    :param constraint_matrix: Matriz de coeficientes das restrições.
    :param constraint_values: Vetor de termos independentes das restrições.
    :param objective_coefficients: Vetor de coeficientes da função objetivo.
    :param num_constraints: Número de restrições.
    :param num_variables: Número de variáveis.
    :return: Valor ótimo, solução ótima, custos reduzidos, status e número de iterações.
    """
    iteration_count = 0
    optimal_value = 0
    solution_vector = np.zeros((num_variables + num_constraints))
    basic_solution = np.zeros((num_constraints))
    basic_costs = np.zeros((num_constraints))
    non_basic_solution = np.zeros((num_variables))
    non_basic_costs = np.zeros((num_variables))
    reduced_costs = np.zeros((num_variables + num_constraints))
    basis_indices = np.zeros((num_constraints), dtype=int)
    basis_matrix = np.zeros((num_constraints, num_constraints))
    non_basis_matrix = np.zeros((num_constraints, num_variables))
    entering_variable_index = -1
    leaving_variable_index = -1
    epsilon = 1e-12
    status = "optimal"

    # Phase 1: Inicialização das variáveis básicas e não básicas
    for i in range(num_constraints):
        basis_indices[i] = num_variables + i
        for j in range(num_constraints):
            basis_matrix[i, j] = constraint_matrix[i, num_variables + j]
        for j in range(num_variables):
            non_basis_matrix[i, j] = constraint_matrix[i, j]

    for i in range(num_variables):
        non_basic_costs[i] = objective_coefficients[i]
        logging.info(f"Non-basic costs: {non_basic_costs[i]}")

    # Verificar se a solução básica inicial é viável
    basic_solution = np.dot(inv(basis_matrix), constraint_values)
    if np.any(basic_solution < 0):
        logging.info("Problem Infeasible.")
        status = "infeasible"
        return None, None, None, status, iteration_count

    reduced_costs = objective_coefficients - np.dot(basic_costs.transpose(), np.dot(inv(basis_matrix), constraint_matrix))
    min_reduced_cost = 0
    for i in range(num_variables + num_constraints):
        if min_reduced_cost > reduced_costs[i]:
            min_reduced_cost = reduced_costs[i]
            entering_variable_index = i

    logging.info(f"Basis indices: {basis_indices}")

    # Phase 2: Iterações do Simplex
    while min_reduced_cost < -epsilon:
        iteration_count += 1
        logging.info(f"=> Iteration: {iteration_count}")
        logging.info(f" Entering variable index: {entering_variable_index}")
        leaving_variable_index = -1
        min_ratio = float('inf')
        logging.info(f"Basis matrix: {basis_matrix}")
        for i in range(num_constraints):
            if np.dot(inv(basis_matrix), constraint_matrix)[i, entering_variable_index] > 0:
                ratio = np.dot(inv(basis_matrix), constraint_values)[i] / np.dot(inv(basis_matrix), constraint_matrix)[i, entering_variable_index]
                logging.info(f"  Ratio: {ratio}")
                if min_ratio > ratio:
                    leaving_variable_index = i
                    logging.info(f"  Leaving variable index: {leaving_variable_index}")
                    min_ratio = ratio
                    logging.info(f"  Min ratio: {min_ratio}")
        if leaving_variable_index == -1:
            logging.info("Problem Unbounded.")
            status = "unbounded"
            return optimal_value, solution_vector, reduced_costs, status, iteration_count
        basis_indices[leaving_variable_index] = entering_variable_index
        logging.info(f"Before updated basis indices: {basis_indices}")
        logging.info(f"  Leaving variable index: {leaving_variable_index}")
        for i in range(num_constraints - 1, 0, -1):
            if basis_indices[i] < basis_indices[i - 1]:
                temp = basis_indices[i - 1]
                basis_indices[i - 1] = basis_indices[i]
                basis_indices[i] = temp

        logging.info(f"Updated basis indices: {basis_indices}")

        for i in range(num_constraints):
            for j in range(num_variables + num_constraints):
                if j == basis_indices[i]:
                    basis_matrix[:, i] = constraint_matrix[:, j]
                    basic_costs[i] = objective_coefficients[j]

        logging.info(f"Exit basis indices: {basis_indices}")
        logging.info(f"Exit basis matrix: {basis_matrix}")

        reduced_costs = objective_coefficients - np.dot(basic_costs.transpose(), np.dot(inv(basis_matrix), constraint_matrix))
        min_reduced_cost = 0
        for i in range(num_variables + num_constraints):
            if min_reduced_cost > reduced_costs[i]:
                min_reduced_cost = reduced_costs[i]
                entering_variable_index = i
        logging.info(f"Min reduced cost: {min_reduced_cost}")
        solution_vector = np.dot(inv(basis_matrix), constraint_values)
        optimal_value = np.dot(basic_costs, solution_vector)
    return optimal_value, solution_vector, reduced_costs, status, iteration_count

def simplex(constraint_matrix, constraint_values, objective_coefficients):
    """
    Executa o algoritmo Simplex.
    :param constraint_matrix: Matriz de coeficientes das restrições.
    :param constraint_values: Vetor de termos independentes das restrições.
    :param objective_coefficients: Vetor de coeficientes da função objetivo.
    """
    augmented_constraint_matrix, augmented_constraint_values, augmented_objective_coefficients, num_constraints, num_variables = standardizing(constraint_matrix, constraint_values, objective_coefficients)
    optimal_value, solution_vector, reduced_costs, status, iteration_count = simplex_iteration(augmented_constraint_matrix, augmented_constraint_values, augmented_objective_coefficients, num_constraints, num_variables)
    
    if status == "infeasible":
        logging.info("The problem is infeasible.")
        print("-------------------------------------------------------------")
        print("The problem is infeasible.")
        print("-------------------------------------------------------------")
        print(f"Number of iterations: {iteration_count}")
        print(f"Status: {status}")
    elif status == "unbounded":
        logging.info("The problem is unbounded.")
        print("-------------------------------------------------------------")
        print("The problem is unbounded.")
        print("-------------------------------------------------------------")
        print(f"Number of iterations: {iteration_count}")
        print(f"Status: {status}")
    else:
        logging.info("-------------------------------------------------------------")
        logging.info("The problem is optimal.")
        logging.info("Results from my implementation")
        logging.info(f"Optimal value: {optimal_value}")
        logging.info(f"Solution vector: {solution_vector}")
        logging.info(f"Reduced costs: {reduced_costs}")
        logging.info("-------------------------------------------------------------")
        print("-------------------------------------------------------------")
        print("The problem is optimal.")
        print("-------------------------------------------------------------")
        print(f"Optimal value: {optimal_value}")
        print(f"Number of iterations: {iteration_count}")
        print(f"Status: {status}")

def linprog_run(filename: str) -> None:
    """
    Executa o algoritmo Simplex usando a biblioteca scipy.
    :param filename: Nome do arquivo de entrada.
    """
    objective_coefficients, constraint_matrix, constraint_values = read_input_from_file(filename)
    augmented_constraint_matrix, augmented_constraint_values, augmented_objective_coefficients, num_constraints, num_variables = standardizing(constraint_matrix, constraint_values, objective_coefficients)
    result = linprog(augmented_objective_coefficients, A_eq=augmented_constraint_matrix, b_eq=augmented_constraint_values, bounds=(0, None))
    logging.info("-------------------------------------------------------------")
    logging.info("Results from scipy implementation")
    logging.info(result)

def run_and_log(filename: str) -> None:
    """
    Configura o logger e executa simplex_run e linprog_run com base no arquivo de entrada.
    :param filename: Nome do arquivo de entrada.
    """
    configure_logger(filename)
    simplex_run(filename)
    linprog_run(filename)

def simplex_run(filename: str) -> None:
    """
    Executa o algoritmo Simplex com base nos dados de entrada de um arquivo.
    :param filename: Nome do arquivo de entrada.
    """
    objective_coefficients, constraint_matrix, constraint_values = read_input_from_file(filename)
    simplex(constraint_matrix, constraint_values, objective_coefficients)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute Simplex algorithm on input file.')
    parser.add_argument('filename', type=str, help='Nome do arquivo de entrada (sem extensão .txt)')
    args = parser.parse_args()
    
    input_filename = args.filename + '.txt'
    run_and_log(input_filename)