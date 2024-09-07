import networkx as nx
import matplotlib.pyplot as plt
import uuid


class FamilyGraph:
    def __init__(self):
        """
        Initializes an empty directed graph self.G and 
        an empty dict self.family_id_index used to relate each family_id to node ids.
        """
        self.G = nx.DiGraph()
        self.family_id_index = {}

    def add_person(self, person_attributes):
        """
        Adds a single person node to the graph and returns the UUID of the node.
        If the person already exists, the UUID of the existing node is returned.

        Parameters:
            person_attributes: Dict specifying person of structure:
            {
                "family_id": None,
                "father_family_id": "Billeter0001",
                "family_name": "Billeter",
                "given_name": "Susanna",
                "birth_year": 1615,
                "death_year": 1644,
                "profession": None,
                "origin": None
            }
        
        Returns:
            person_id: UUID of new or already existing person node
        """

        # check for mandatory fields in person_attributes:
        if any(x not in person_attributes.keys() for x in [
            "family_id", "father_family_id", "family_name", "given_name"
        ]):
            raise Exception("person_attributes attributes missing. Required: family_id, father_family_id, family_name, given_name")
        
        # initialize other fields in person_attributes with None if not existing:
        for key in ["birth_year", "death_year", "profession", "origin"]:
            if key not in person_attributes.keys():
                person_attributes[key] = None

        # check if person is already in self.G:
        person_id = self.get_id_from_attributes(person_attributes)

        if person_id is not None:
            # Merge the new person_attributes with already existing ones ...
            for key, val in self.G.nodes[person_id].items():
                if val is None or (
                    len(str(val)) < len(str(person_attributes.get(key))) 
                    and person_attributes.get(key) is not None
                    ):
                    self.G.nodes[person_id][key] = person_attributes.get(key)
        else:
            # Person is not in self.G yet:
            person_id = uuid.uuid4()
            self.G.add_node(person_id, **person_attributes)
            # Add person_id to self.family_id_index
            if person_attributes.get("family_id") is not None:
                self.family_id_index["family_id"] = person_id
        
        return person_id
    
    def add_relation(self, id_from, id_to, relation_type):
        """
        Creates a directed edge from id_from to id_to.

        Parameters:
            id_from: person_id of first node
            id_to: persion_id of second note
            relation_type: code specifying relation of first to second node (FATHER_CHILD, HUSBAND_WIFE, MOTHER_CHILD)
        """
        if relation_type not in ['FATHER_CHILD', 'HUSBAND_WIFE', 'MOTHER_CHILD']:
            raise Exception('relation_type should be one of: FATHER_CHILD, HUSBAND_WIFE, MOTHER_CHILD')
        self.G.add_edge(id_from, id_to, relation_type=relation_type)

    def get_id_from_attributes(self, person_attributes):
        """
        Checks if a person node of given person_attributes already exists in the graph.
        It finds already existing persons through matching the family_id of person_attributes
        with the nodes in the graph.
        Otherwise it also looks if father_family_id of person_attributes is already in the graph
        and matches the name and birth_year of its children
        
        Parameters:
            person_attributes: person attribute containing (at least):
            {
                "family_id": None,
                "father_family_id": "Billeter0001",
                "surname": "Susanna",
                "birth_year": 1615
            }

        Returns: UUID of person node if already exists, or else None
        """
        
        # Check if person with family_id is already in self.G:
        person_id = self.family_id_index.get(person_attributes['family_id'])
        # person_ids = [
        #     id for id, data in self.G.nodes(data=True)
        #     if data['family_id'] == person_attributes['family_id'] and person_attributes['family_id'] is not None
        # ]

        if person_id is not None:
            return person_id
        
        # if len(person_ids) > 1:
        #     raise Exception("Person exists multiple times.")
        # elif len(person_ids) == 1:
        #     # Person is already in self.G:
        #     return person_ids[0]

        # Check if father with family_id is already in self.G:
        if person_attributes['father_family_id'] is not None:
            father_id = self.family_id_index.get(person_attributes['father_family_id'])

            if father_id is not None:
                # Father is already in self.G
                # get all children:
                children_ids = list(self.G.successors(father_ids[0]))

                # Filter children with same names only:
                children_ids = [
                    id for id in children_ids 
                    if self.G.nodes[id]['surname'] == person_attributes['surname']
                ]
                if len(children_ids) > 1:
                    # If multiple children with same name, filter for same birth_year only:
                    children_ids = [
                        id for id in children_ids 
                        if self.G.nodes[id]['birth_year'] == person_attributes['birth_year']
                    ]
                print(f"{person_attributes['surname']} is already in self.G!")
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