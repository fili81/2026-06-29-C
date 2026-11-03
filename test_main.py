from model.model import Model

model = Model()
model.buildGraph()

print("Numero nodi: ", model.getNumNodes())
print("Numero archi: ", model.getNumEdges())

artist, degree = model.getArtistWithMaxDegree()
print("Artista con grado massimo:", artist, degree)

artist, weight_sum = model.getArtistWithMaxWeightSum()
print("Artista con somma pesi massima:", artist, weight_sum)

print("\nTop 10 archi:")
for a1, a2, data in model.getTop10Edges():
    print(a1, "-", a2, "- peso:", data["weight"])

artists = list(model.graph.nodes)

starting_artist = artists[0]

# scelgo N
N = 3

bestGroup, maxTracks = model.getBestGroup(starting_artist, N)

print("\nArtista di partenza:")
print(starting_artist)

print("\nMiglior gruppo trovato:")

for artist in bestGroup:
    print(
        artist,
        "- tracce:",
        len(artist.Tracks)
    )

print("\nNumero totale di tracce:", maxTracks)