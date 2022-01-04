from unittest import TestCase

from api.DiGraph import DiGraph


class TestDiGraph(TestCase):

    def test_v_size(self):
        graph = DiGraph("data/A0")
        graph1 = DiGraph("data/A1")
        self.assertEqual(11, graph.v_size())
        self.assertEqual(17, graph1.v_size())

    def test_e_size(self):
        graph = DiGraph("data/A0")
        graph1 = DiGraph("data/A1")
        self.assertEqual(22, graph.e_size())
        self.assertEqual(36, graph1.e_size())

    def test_get_all_v(self):
        string_dict = "{0: 0: |edges out| 2 |edges in| 2, 1: 1: |edges out| 2 |edges in| 2, 2: 2:" \
                      " |edges out| 2 |edges in| 2, 3: 3: |edges out| 2 |edges in| 2," \
                      " 4: 4: |edges out| 2 |edges in| 2, 5: 5: |edges out| 2 |edges in| 2," \
                      " 6: 6: |edges out| 2 |edges in| 2, 7: 7: |edges out| 2 |edges in| 2, " \
                      "8: 8: |edges out| 2 |edges in| 2, 9: 9: |edges out| 2 |edges in| 2, " \
                      "10: 10: |edges out| 2 |edges in| 2}"
        graph = DiGraph("data/A0")
        self.assertEqual(string_dict, graph.get_all_v().__str__())


    def test_add_node(self):
        graph = DiGraph("data/A0")
        self.assertEqual(None, graph.nodes.get(27))
        self.assertTrue(graph.add_node(27, (35.16262, 26.2626, 0)))
        self.assertEqual("27: |edges out| {} |edges in| {}", graph.nodes.get(27).__str__())

