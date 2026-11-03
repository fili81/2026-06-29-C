import networkx as nx
from database.DAO import DAO
import copy

class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.artists = []

        # per ricorsione
        self.bestGroup = []
        self.maxTracks = 0

    def buildGraph(self):
        self.graph.clear()

        self.artists = DAO.getAllArtists()
        self.graph.add_nodes_from(self.artists)

        for i in range(len(self.artists)):
            for j in range(i+1, len(self.artists)):
                a1 = self.artists[i]
                a2 = self.artists[j]

                common = a1.Playlists & a2.Playlists
                if common:
                    self.graph.add_edge(a1, a2, weight=len(common))

    def getNumNodes(self):
        return self.graph.number_of_nodes()

    def getNumEdges(self):
        return self.graph.number_of_edges()

    def getArtistWithMaxDegree(self):
        bestArtist = None
        maxDegree = -1
        for node, degree in self.graph.degree():
            if degree > maxDegree:
                maxDegree = degree
                bestArtist = node
        return bestArtist, maxDegree

    def getArtistWithMaxWeightSum(self):
        bestArtist = None
        max_sum = -1
        for node in self.graph.nodes():
            sum = 0
            for neighbor in self.graph.neighbors(node):
                sum += self.graph[node][neighbor]["weight"]

            if sum > max_sum:
                max_sum = sum
                bestArtist = node
        return bestArtist, max_sum

    def getTop10Edges(self):
        edges = list(self.graph.edges(data=True))
        edges.sort(key=lambda x: (
            -x[2]["weight"],
            x[0].Name,
            x[1].Name
            )
        )
        return edges[:10]

    # per ricorsione
    def getBestGroup(self, starting_artist, N):

        self.bestGroup = []
        self.maxTracks = 0

        parziale = [starting_artist]

        self._ricorsione(parziale, N)

        return self.bestGroup, self.maxTracks

    def _ricorsione(self, parziale, N):

        if len(parziale) == N:

            totalTracks = self._getTotalTracks(parziale)
            if totalTracks > self.maxTracks:
                self.maxTracks = totalTracks
                self.bestGroup = copy.deepcopy(parziale)
            return

        for candidate in self.graph.nodes:
            if candidate in parziale:
                continue

            adjacent = any(
                self.graph.has_edge(candidate, existing)
                for existing in parziale
            )
            if not adjacent:
                continue

            blocked = any(
                self.graph.has_edge(candidate, existing)
                and self.graph[candidate][existing]["weight"] == 1
                for existing in parziale
            )
            if blocked:
                continue

            # scelgo
            parziale.append(candidate)

            # continuo
            self._ricorsione(parziale, N)

            # torno indietro
            parziale.pop()


    def _getTotalTracks(self, artists):
        total = 0

        for artist in artists:
            total += len(artist.Tracks)
        return total









