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
        # check if person is already in self.G:
        person_id = self.get_id_from_attributes(person_attributes)

        if person_id is not None:
            # TODO update node...
            pass
        else:
            # Person is not in self.G yet:
            person_id = uuid.uuid4()
            self.G.add_node(person_id, **person_attributes)
        
        return person_id
    
    def add_relation(self, id_from, id_to, relation_type):
        """

        """
        if relation_type not in ['FATHER_CHILD', 'HUSBAND_WIFE', 'MOTHER_CHILD']:
            raise Exception('relation_type should be one of: FATHER_CHILD, HUSBAND_WIFE, MOTHER_CHILD')
        self.G.add_edge(id_from, id_to, relation_type=relation_type)

    def get_id_from_attributes(self, person_attributes):
        """
        Adds multiple nodes to the graph.
        
        Parameters:
            nodes: A list of nodes to add to the graph.
        """
        
        # Check if person with family_id is already in self.G:
        person_ids = [
            id for id, data in self.G.nodes(data=True)
            if data['family_id'] == person_attributes['family_id'] and person_attributes['family_id'] is not None
        ]
        
        if len(person_ids) > 1:
            raise Exception("Person exists multiple times.")
        elif len(person_ids) == 1:
            # Person is already in self.G:
            return person_ids[0]

        # Check if father with family_id is already in self.G:
        if person_attributes['father_family_id'] is not None:
            father_ids = [
                id for id, data in self.G.nodes(data=True)
                if data['family_id'] == person_attributes['father_family_id']
            ]

            if len(father_ids) > 1:
                raise Exception("Father exists multiple times.")
            elif len(father_ids) == 1:
                # Father is already in self.G
                # get all children:
                children_ids = list(self.G.successors(father_ids[0]))
                # Filter children with same names only:
                children_ids = [
                    id for id in children_ids 
                    if self.G.nodes[id]['surname'] == person_attributes['surname']
                ]
                if len(children_ids) == 1:
                    # Person is already in self.G:
                    return children_ids[0]
                elif len(children_ids) > 0:
                    # If multiple children with same name, filter for same birth_year:
                    children_ids = [
                        id for id in children_ids 
                        if self.G[children_ids]['birth_year'] == person_attributes['birth_year']
                    ]
                    if len(children_ids) == 1:
                        # Person is already in self.G:
                        return children_ids[0]

        # Person doesn't exist yet in self.G:
        return None

    def visualize(self):
        """
        Visualizes the directed graph using matplotlib and networkx.
        """
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.G)  # Positions for all nodes
        label1 = nx.get_node_attributes(self.G, 'surname')
        label2 = nx.get_node_attributes(self.G, 'family_name')
        labels = {
            key: label1.get(key, '') + ' ' + label2.get(key, '')
            for key in set(label1) | set(label2)
        }
        edge_labels = nx.get_edge_attributes(self.G, 'relation_type')
        nx.draw(self.G, pos, with_labels=True, labels=labels, node_color="lightblue", node_size=100, font_size=7, edge_color='gray', arrows=True)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=7)
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