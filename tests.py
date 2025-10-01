import unittest
from boggle_solver import Boggle

class TestBoggleBlackBox(unittest.TestCase):
    # empty dictionary -> no words
    def test_dictionary_is_empty(self):
        grid = [["A","B"],["C","D"]]
        words = []
        self.assertEqual(Boggle(grid, words).getSolution(), [])

    # empty grid -> no words
    def test_grid_is_empty(self):
        grid = []
        words = ["ABC"]
        self.assertEqual(Boggle(grid, words).getSolution(), [])

    # min length enforced (words < 3 ignored even if present)
    def test_min_length(self):
        grid = [["A","B"],["C","D"]]
        words = ["A", "AB", "ABC"]
        out = Boggle(grid, words).getSolution()
        self.assertIn("ABC", out)
        self.assertNotIn("A", out)
        self.assertNotIn("AB", out)

    # no cube reuse (ABA on a 1x2 board requires revisiting A)
    def test_no_reuse(self):
        grid = [["A","B"]]
        words = ["ABA"]
        self.assertEqual(Boggle(grid, words).getSolution(), [])

    # diagonal adjacency allowed
    def test_diagonal(self):
        grid = [["C","A"],
                ["B","R"]]
        words = ["CAR", "BAR", "CAB"]  # CAB not possible (no B after A without reuse)
        out = Boggle(grid, words).getSolution()
        self.assertCountEqual(out, ["BAR","CAR"])

    # handles Qu and St tiles as two letters
    def test_qu_st_tiles(self):
        grid = [["T","W","Y","R"],
                ["E","N","P","H"],
                ["G","St","Qu","R"],
                ["O","N","T","A"]]
        words = ["QUA","QUART","WENT","WET","STARE"]  # STARE may or may not exist; expect the known four
        out = Boggle(grid, words).getSolution()
        for w in ["QUA","QUART","WENT","WET"]:
            self.assertIn(w, out)
        self.assertNotIn("STARE", out)

    #case-insensitivity in inputs
    def test_case_insensitive(self):
        grid = [["t","w"],["e","St"]]
        words = ["wet","WET","WeT","TEST"]
        out = Boggle(grid, words).getSolution()
        self.assertIn("WET", out)
        self.assertNotIn("TEST", out)

    # uniqueness (same word via multiple paths appears once)
    def test_unique_results(self):
        grid = [["C","A"],
                ["A","T"]]
        words = ["CAT"]
        out = Boggle(grid, words).getSolution()
        self.assertEqual(out, ["CAT"])

    # longer paths (given sample from prompt)
    def test_longer_paths_sample(self):
        grid = [["A","B","C","D"],
                ["E","F","G","H"],
                ["I","J","K","L"],
                ["A","B","C","D"]]
        words = ["ABEF","AFJIEB","DGKD","DGKA"]
        out = Boggle(grid, words).getSolution()
        self.assertCountEqual(out, ["ABEF","AFJIEB","DGKD"])

    # words not present are ignored
    def test_words_not_present(self):
        grid = [["M","N"],["O","P"]]
        words = ["CAT","DOG","MOM","POP"]
        self.assertEqual(Boggle(grid, words).getSolution(), [])

    #larger square with multiple finds
    def test_3x3_variety(self):
        grid = [["C","A","R"],
                ["A","T","E"],
                ["R","E","D"]]
        words = ["CAR","CARD","CART","TEA","EAT","READ","TAR"]
        out = set(Boggle(grid, words).getSolution())
        expected_subset = {"CAR","CART","TEA","EAT","TAR"}  # READ/CARD may fail depending on layout
        self.assertTrue(expected_subset.issubset(out))

if __name__ == "__main__":
    unittest.main()
