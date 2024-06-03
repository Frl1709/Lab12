import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        years = self._model._listaAnni
        country = self._model._listaCountry
        for a in years:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        for c in country:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    def handle_graph(self, e):
        if self._view.ddcountry.value is not None and self._view.ddyear.value is not None:
            self._model.creaGrafo(self._view.ddcountry.value, self._view.ddyear.value)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Numero di vertici: {self._model.getNumNodes()}, Numero di archi: {self._model.getNumEdges()}"))
            self._view.btn_volume.disabled = False
            self._view.btn_path.disabled = False
            self._view.update_page()
        else:
            if self._view.ddyear.value is None:
                self._view.create_alert("Inserire l'anno da considerare")
            elif self._view.ddcountry.value is None:
                self._view.create_alert("Inserire il paese da considerare")

    def handle_volume(self, e):
        self._model.getVolumi()
        sortedVolumi = sorted(self._model._volumi, key=lambda x: self._model._volumi[x], reverse=True)
        self._view.txtOut2.controls.clear()
        for i in sortedVolumi:
            self._view.txtOut2.controls.append(
                ft.Text(f"{i.Retailer_name} --> {self._model._volumi[i]}"))
        self._view.update_page()

    def handle_path(self, e):
        try:
            int(self._view.txtN.value)
            if int(self._view.txtN.value) >= 2:
                self._model.getBestPath(int(self._view.txtN.value))
                self._view.txtOut3.controls.clear()
                self._view.txtOut3.controls.append(
                    ft.Text(f"Peso cammino massimo: {self._model._bestWeight}")
                )
            for i in range(len(self._model._bestPath) - 1):
                self._view.txtOut3.controls.append(
                    ft.Text(
                        f"{self._model._bestPath[i].Retailer_name} --> {self._model._bestPath[i + 1].Retailer_name}: {self._model._grafo[self._model._bestPath[i]][self._model._bestPath[i + 1]]['weight']}"))
            self._view.update_page()

        except ValueError:
            if self._view.txtN.value == "":
                self._view.create_alert("Inserire la lunghezza del percorso")
            else:
                self._view.create_alert("Inserire un numero intero positivo")
