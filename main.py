import heapq
from numpy import random as rand

class AStarConfig:

    nodes = None # dict[dict[int]]
    heuristics = None #dict[int]

    def __init__(self, nodes, heuristics):
        self.nodes = nodes
        self.heuristics = heuristics

def generate_graph():
    #returns a dict of all the nodes that are part of the graph for the astar including the relation of their distances

    while True:
        input_value = input("Insira o numero de de nos (minimo 5, maximo 26) ou pressione enter para o minimo, podendo ser qualquer coisa, lugares ou nodos de estações: ")
        if(input_value == ""):
            num_nodes = 5
        else:
            num_nodes = int(input_value)
            
        if(not (num_nodes < 5 or num_nodes > 26)):
            break
        print("NUMERO DE NODOS INVALIDDO, TENTE NOVAMENTE")

    nodes = {}
    heuristics = {}
    
    min_distance = 100
    max_distance = 500
    min_heuristic = 10
    max_heuristic = 500

    #define the nodes and the heuristics
    for i in range(num_nodes):
        letter = chr(ord('a')+i)
        nodes[letter] = None
        heuristics[letter] = rand.randint(min_heuristic, max_heuristic)

    #everything coming after this is defining the connections that each node has to other nodes and the distance
    for node in nodes:  
        #connections_length = the ammount of connections for the node
        #random_connections = the other nodes are gonna be on the connections_length connected to the node
        connections_length = rand.randint(1, num_nodes)
        # esse ai em baixo vai remover todas as chaves repetidas, usando um macete com dict.fromkeys e list
        random_connections = rand.randint(num_nodes, size=(connections_length))
        
        while True:
            #organize the list first to remove repeated values
            random_connections = list(dict.fromkeys(random_connections))
            
            #check if the connections points to the same node
            self_node = ord(node)-ord('a')
            if(self_node in random_connections):
                random_connections.remove(self_node)

            #if we keep the same length we defined, break
            if(len(random_connections) == connections_length):
                break

            new_conn = rand.randint(0, num_nodes)
            random_connections.append(new_conn)

        random_connections.sort()
        nodes[node] = dict()
        for conn in random_connections:
            letter = chr(ord('a') + conn)
            nodes[node][letter] = rand.randint(min_distance, max_distance)
        

    #astar_config.nodes = nodes
    #astar_config.heuristic = heuristics
    
    return AStarConfig(nodes, heuristics)

def astar(astar_config, start, finish):
    nodes = astar_config.nodes
    heuristics = astar_config.heuristics

    g_value = {node: float('inf') for node in nodes.keys()}
    f_value = {node: float('inf') for node in nodes.keys()}

    g_value[start] = 0
    f_value[start] = heuristics[start]

    priority_queue = [(0, start)]
    #visited = set()
    visited = set()
    came_from = {}

    while priority_queue:
        node_val, node = heapq.heappop(priority_queue)
        
        if node == finish:
            print("\n\n\nNODO FINAL ENCONTRADO!\n\n\n")
            break

        visited.add(node)

        for neighbor_node in nodes[node].keys():
            if neighbor_node in visited:
                continue

            #calcula a distância do nó atual até o vizinho
            neighbor_disance = nodes[node][neighbor_node]

            #calcula o valor de g do vizinho a partir do valor de g do nó atual
            temp_g_value = g_value[node] + neighbor_disance

            #verifica se o valor de g do vizinho é menor que o valor de g ja guardado para o vizinho no dicionário
            if temp_g_value < g_value[neighbor_node]:

                #atualiza o valor de g do vizinho com o novo valor
                g_value[neighbor_node] = temp_g_value

                #atualiza o valor de f do vizinho com a soma do valor de g do vizinho e da heuristica do vizinho
                f_value[neighbor_node] = temp_g_value + heuristics[neighbor_node]

                #adiciona o nó vizinho na fila de prioridade com o valor de f como chave
                heapq.heappush(priority_queue, (f_value[neighbor_node], neighbor_node))

                #guarda o nó atual como o nó que o nó vizinho veio de, para depois poder percorrer o caminho
                came_from[neighbor_node] = node



        # Imprimir informações (tive que roubar infelizmente)
        print("\n\n\n------PASSO------\n")
        print(f"Nodo atual: {node}\n")
        print(f"Nodos vizinhos{list(nodes[node].keys())}\n")
        print(f"Nodos na fila: ")
        for f, node in priority_queue:
            print(f"\tNodo: {node}, g({node}) + f({node}) = {f}")
            
        print(f"Proximo Nodo: {priority_queue[0][1] if priority_queue else 'None'}")
        print(f"----------------------------")

    return


#INIT
if __name__ == "__main__":
    astar_config = generate_graph()

    print(f"\n\nCONFIGURAÇÃO DOS NODOS: \n\n {astar_config.nodes} \n\nCONFIGURAÇÃO DAS HEURÍSTICAS: \n\n {astar_config.heuristics} \n\n")


    start = input("Insira o no inicial: ").lower()
    finish = input("Insira o no final: ").lower()

    result = astar(astar_config, start, finish)

    #result = astar(set.map, set.start, set.finish)
    #print_result(result)