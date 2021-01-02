import itertools
import graph as g
import vertex as v
import state as s
import names


def generate_graph(file_name):
    output_graph = g.Graph()
    file = open(file_name)
    lines = file.readlines()
    name_vertices_dict = {}
    for line in lines:
        element_type = line[0]
        line = line.split(' ')
        if element_type == 'V':
            name = line[1]
            num_of_people = int(line[2])
            u = None
            if num_of_people > 0:
                u = v.Vertex(name, True)
            else:
                u = v.Vertex(name)
            name_vertices_dict[u.name] = u
            output_graph.add_vertex(u)
        elif element_type == 'E':
            source_name = line[1]
            target_name = line[2]
            edge_weight = int(line[4])
            edge_name = line[3]
            probability = float(line[5])
            v1 = name_vertices_dict[source_name]
            v2 = name_vertices_dict[target_name]
            output_graph.add_edge(v1, v2, edge_weight,edge_name,probability)
    file.close()
    return output_graph


if __name__ == '__main__':
    graph = generate_graph(names.input_file)
    print(graph)
    print(s.state_list_as_string(s.generate_states(graph)))
