import unittest
from directed_graph import DirectedGraph  # Assuming DirectedGraph is in directed_graph.py

class TestDirectedGraph(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a new DirectedGraph object before each test.
        """
        self.graph = DirectedGraph()

    def test_add_nodes(self):
        """
        Test the add_nodes function to check if the nodes are correctly added to the graph.
        """
        nodes_to_add = [1, 2, 3, 4, 5]
        
        # Call the function to add nodes
        self.graph.add_nodes(nodes_to_add)
        
        # Get the nodes from the graph
        nodes_in_graph = self.graph.get_nodes()
        
        # Assert that the nodes added are the same as the nodes in the graph
        self.assertEqual(set(nodes_to_add), set(nodes_in_graph), "Nodes added to the graph should match the expected nodes.")
        
# Run the test
if __name__ == '__main__':
    unittest.main()
