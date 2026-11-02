import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


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
        pass