"""
NAME: Pierre-Jeremiah Merry
SID: 003108044  
"""

class _TrieNode:
    __slots__ = ("children", "is_word")
    def __init__(self):
        self.children = {}
        self.is_word = False

class _Trie:
    def __init__(self):
        self.root = _TrieNode()
    def insert(self, word):
        cur = self.root
        for ch in word:
            cur = cur.children.setdefault(ch, _TrieNode())
        cur.is_word = True

class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = self._norm_grid(grid)
        self.dictionary = self._norm_words(dictionary)
        self.solutions = []
        self.r = len(self.grid)
        self.c = len(self.grid[0]) if self.r else 0
        self.trie = _Trie()
        for w in self.dictionary:
            if len(w) >= 3:
                self.trie.insert(w)

    def setGrid(self, grid):
        self.grid = self._norm_grid(grid)
        self.r = len(self.grid)
        self.c = len(self.grid[0]) if self.r else 0

    def setDictionary(self, dictionary):
        self.dictionary = self._norm_words(dictionary)
        self.trie = _Trie()
        for w in self.dictionary:
            if len(w) >= 3:
                self.trie.insert(w)

    def getSolution(self):
        if not self.r or not self.c:
            self.solutions = []
            return self.solutions
        found = set()
        seen = [[False]*self.c for _ in range(self.r)]
        for i in range(self.r):
            for j in range(self.c):
                node = self._advance(self.trie.root, self.grid[i][j])
                if node:
                    self._dfs(i, j, seen, node, self.grid[i][j], found)
        self.solutions = sorted(found)
        return self.solutions

    def solution(self):
        return self.getSolution()

    def _dfs(self, i, j, seen, node, path, found):
        seen[i][j] = True
        if node.is_word and len(path) >= 3:
            found.add(path)
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di == 0 and dj == 0: 
                    continue
                ni, nj = i+di, j+dj
                if 0 <= ni < self.r and 0 <= nj < self.c and not seen[ni][nj]:
                    nxt = self._advance(node, self.grid[ni][nj])
                    if nxt:
                        self._dfs(ni, nj, seen, nxt, path + self.grid[ni][nj], found)
        seen[i][j] = False

    def _advance(self, node, tile):
        cur = node
        for ch in tile:
            if cur is None or ch not in cur.children:
                return None
            cur = cur.children[ch]
        return cur

    def _norm_grid(self, grid):
        out = []
        for row in grid:
            rr = []
            for cell in row:
                s = str(cell).strip()
                if s.lower() == "qu": rr.append("QU")
                elif s.lower() == "st": rr.append("ST")
                else: rr.append(s.upper())
            out.append(rr)
        return out

    def _norm_words(self, words):
        return [w.strip().upper() for w in words if str(w).strip()]

def main():
    grid = [["A","B","C","D"],
            ["E","F","G","H"],
            ["I","J","K","L"],
            ["A","B","C","D"]]
    dictionary = ["ABEF","AFJIEB","DGKD","DGKA"]
    print(Boggle(grid, dictionary).getSolution())

if __name__ == "__main__":
    main()
