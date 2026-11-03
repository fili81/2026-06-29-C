import flet as ft

from test_main import bestGroup, maxTracks


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        # per ricorsione
        self._artistValue = None


    # per ricorsione dropdown oggetti
    def fillDDArtists(self):
        self._view._ddArtista.options.clear()

        artists = self._model.artists

        self._view._ddArtista.options = list(
            map(lambda x: ft.dropdown.Option(
                data=x,
                key=str(x),
                on_click=self._handleOggetto
            ),
                artists
        )
        )
        self._view.update_page()

    def _handleOggetto(self,e):
        self._artistValue = e.control.data

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        self._model.buildGraph()
        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Numero nodi: {self._model.getNumNodes()}")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Numero archi: {self._model.getNumEdges()}")
        )

        # per ricorsione
        self.fillDDArtists()

        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        artist, degree = self._model.getArtistWithMaxDegree()
        self._view._txt_result.controls.append(
            ft.Text(
                f"Artista con grado maggiore: {artist} - grado: {degree}"
            )
        )
        artist, weight_sum = self._model.getArtistWithMaxWeightSum()

        self._view._txt_result.controls.append(
            ft.Text(
                f"Artista con somma dei pesi massima: {artist} - somma: {weight_sum}"
            )
        )
        top10 = self._model.getTop10Edges()
        for a1, a2, data in top10:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{a1} - {a2} - peso: {data['weight']}"
                )
            )
        self._view.update_page()

    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodes() == 0:
            self._view.create_alert("Creare prima il grafo")
            return

        if self._artistValue is None:
            self._view.create_alert("Selezionare un artista")
            return

        try:
            N = int(self._view._txtInN.value)
        except ValueError:
            self._view.create_alert("Inserire un numero valido.")
            return

        if N <= 0:
            self._view.create_alert("N deve essere maggiore di zero.")
            return

        bestGroup, maxTracks = self._model.getBestGroup(self._artistValue, N)
        if len(bestGroup) == 0:
            self._view._txt_result.controls.append(
                ft.Text("Nessun gruppo trovato.")
            )
            self._view.update_page()
            return

        self._view._txt_result.controls.append(
            ft.Text("Miglior gruppo trovato:")
        )

        for artist in bestGroup:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{artist} - {len(artist.Tracks)} tracce"
                )
            )

        self._view._txt_result.controls.append(
            ft.Text(
                f"Numero totale di tracce: {maxTracks}"
            )
        )

        self._view.update_page()