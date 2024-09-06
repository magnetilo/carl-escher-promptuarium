import networkx as nx
import matplotlib.pyplot as plt
import uuid

class FamilyGraph:
    def __init__(self):
        """
        Initializes an empty directed graph.
        """
        self.G = nx.DiGraph()

    def add_person(self, person_attributes):
        """
        Adds a single node to the graph.
        
        Parameters:
            node: The node to add to the graph.
        """
        # check if person is already in G:
        person_id = self.get_id_from_attributes(person_attributes)

        if person_id is not None:
            # TODO update node...
        else:
            person_id = uuid.uuid4()
            self.G.add_node(new_id, person_attributes)
        
        return person_id
    
    def add_realation(self, id_from, id_to, relation_type):
        """

        """
        if relation_type not in ['FATHER_CHILD', 'HUSBAND_WIFE', 'MOTHER_CHILD']:
            raise Exeption('relation_type should be one of: FATHER_CHILD, HUSBAND_WIFE, MOTHER_CHILD')
        self.G.add_edge(id_from, id_to, relation_type)

    def get_id_from_attributes(person_attributes):
        """
        Adds multiple nodes to the graph.
        
        Parameters:
            nodes: A list of nodes to add to the graph.
        """
        self.G.add_nodes_from(nodes)
        print(f"Nodes {nodes} added to the graph.")

    def visualize(self):
        """
        Visualizes the directed graph using matplotlib and networkx.
        """
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.G)  # Positions for all nodes
        nx.draw(self.G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_weight='bold', edge_color='gray', arrows=True)
        plt.title("Directed Graph")
        plt.show()

    def get_nodes(self):
        """
        Returns the list of nodes in the graph.
        """
        return list(self.G.nodes)

    def get_edges(self):
        """
        Returns the list of edges in the graph.
        """
        return list(self.G.edges)