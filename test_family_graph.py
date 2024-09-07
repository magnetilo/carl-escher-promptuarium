import unittest
from family_graph import FamilyGraph

class TestDirectedGraph(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a new FamilyGraph object before each test.
        """
        self.graph = FamilyGraph()

    def test_add_nodes(self):
        """
        Test the add_nodes function to check if the nodes are correctly added to the graph.
        """

        # TODO: Write tests...
        #         
        # Assert that the nodes added are the same as the nodes in the graph
        #self.assertEqual(set(nodes_to_add), set(nodes_in_graph), "Nodes added to the graph should match the expected nodes.")
        pass
        
# Run the test
if __name__ == '__main__':
    unittest.main()
