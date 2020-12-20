from node import Node
from table import Table, make_table
from multipledispatch import dispatch
import names
import itertools


def create_bayes_network(file_name):
    with open(file_name, 'r') as graph_file:
        network = BayesNetwork()
        for line in graph_file.readlines():
            words_array = line.split(' ')
            if len(words_array) > 0:
                first_letter = words_array[0]
                if first_letter == 'N':
                    pass
                elif first_letter == 'V':
                    vertex_name = words_array[1]
                    people_prob = float(words_array[2])
                    node = Node(vertex_name, make_table([[names.empty]], [people_prob]))
                    network.add_node(node)
                elif first_letter == 'E':
                    edge_name = words_array[1] + '_t:0'
                    vertex_1_name = words_array[2]
                    vertex_2_name = words_array[3]
                    weight = int(words_array[4])
                    edge_node_1 = Node(edge_name, make_table(create_all_entries(vertex_1_name, vertex_2_name),
                                                             calculate_edge_block_prob(weight)))
                    vertex_1_node = network.get_node(vertex_1_name)
                    vertex_2_node = network.get_node(vertex_2_name)
                    network.add_node(edge_node_1)
                    network.add_relation(vertex_1_node, edge_node_1, weight)
                    network.add_relation(vertex_2_node, edge_node_1, weight)

                    edge_name_t1 = words_array[1] + '_t:1'
                    weight = names.time_relation_weight
                    edge_node_t1 = Node(edge_name_t1,
                                        make_table(create_all_entries(edge_name), [0.001, names.persistence]))
                    network.add_node(edge_node_t1)
                    network.add_relation(edge_node_1, edge_node_t1, weight)

        return network


@dispatch(str)
def create_all_entries(parent_name):
    return [[(parent_name, False)], [(parent_name, True)]]


def calculate_edge_block_prob(weight):
    return [0.001, 0.6 * 1 / weight, 0.6 * 1 / weight, 1 - pow(1 - (0.6 * 1 / weight), 2)]


@dispatch(str, str)
def create_all_entries(name_1, name_2):
    return [[(name_1, False), (name_2, False)], [(name_1, True), (name_2, False)], [(name_1, False), (name_2, True)],
            [(name_1, True), (name_2, True)]]


class BayesNetwork:
    def __init__(self):
        self.children_dict = {}
        self.parents_dict = {}

    def add_node(self, node: Node):
        if not self.children_dict.get(node):
            self.children_dict[node] = []
        if not self.parents_dict.get(node):
            self.parents_dict[node] = []

    def add_relation(self, parent: Node, child: Node, weight: int):
        if child not in self.children_dict[parent]:
            self.children_dict[parent].append((child, weight))
        if parent not in self.parents_dict[child]:
            self.parents_dict[child].append((parent, weight))

    def get_node(self, node_name):
        for node in self.children_dict.keys():
            if node.name == node_name:
                return node
        return None

    def str_graph_structure(self):
        s = 'children dictionary: \n'
        for node in self.children_dict.keys():
            s += node.name
            s += ', children: '
            for child_weight in self.children_dict[node]:
                s += '[' + child_weight[0].name + ', weight=' + str(child_weight[1]) + '], '
            s += '\n'

        s += '\nparents dictionary: \n'
        for node in self.parents_dict.keys():
            s += node.name
            s += ', parents: '
            for parent_weight in self.parents_dict[node]:
                s += '[' + parent_weight[0].name + ' ,weight=' + str(parent_weight[1]) + '], '
            s += '\n'
        return s

    def __str__(self):
        s = 'Bayes Network:'
        s += 'nodes: \n'
        for node in self.children_dict.keys():
            s += str(node)
        return s

    def get_all_nodes(self):
        return self.children_dict.keys()

# evidence = {(v1, 0.5),..., (vn, 0.4)}
def has_value_in_evidence(Y, evidence):
    for tup in evidence:
        if tup[0] == Y:
            return True, tup[1]
    return False, -1


def enumeration_all(variables, evidence, bayes_network):
    if len(variables) == 0:
        return 1
    Y = variables[0]
    has_val, val = has_value_in_evidence(Y, evidence)
    if has_val:
        pass
    else:
        pass




def normalize(distribution):
    acc = 0
    for value in distribution.values():
        acc += value
    for key_value in distribution.items():
        key = key_value[0]
        value = key_value[1]
        distribution[key] = value / acc


# query is list of strings, we return the probability of all of them being true
def enumeration_ask(x_query: list, evidence: set, bayes_network: BayesNetwork):
    distribution_x = {}  # Q(X)
    options = [False, True]
    x_query_possible_values = list(itertools.product(options, repeat=len(x_query)))
    for assignment in x_query_possible_values:
        extended_evidence = evidence.union(set(zip(x_query, assignment)))
        variables = bayes_network.get_all_nodes()
        prob = enumeration_all(variables, extended_evidence, bayes_network)
        distribution_x[assignment] = prob
    return normalize(distribution_x)
