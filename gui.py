import PySimpleGUI as sg
from utility import Utility
#Gauß

class GUI:

    def __init__(self) -> None:
        self.util = Utility()
        #self.gauss = Gauss()

    def start_gui(self):
        """
        Starts the gui and runs an event-loop that blocks code from executing after this until the gui-window is closed
        """

        # Definition der Eingabefelder (Matrix A & B) 
        column_mat_a = [
            [sg.Text("Matrix A")],
            [sg.Multiline(key="-MATRIXA-", size=(20, 10))]
        ]

        column_mat_b = [
            [sg.Text("Matrix B")],
            [sg.Multiline(key="-MATRIXB-", size=(20, 10))]
        ]
        # + Ausgabefelder für GAUß: column_mat_l = [...], column_mat_u = [...], column_mat_lu = [...]
        column_mat_l = [
            [sg.Text("Matrix L")],
            [sg.Multiline(key="-MATRIXL-", size=(20, 10))]
        ]

        column_mat_u = [
            [sg.Text("Matrix R")],
            [sg.Multiline(key="-MATRIXU-", size=(20, 10))]
        ]

        column_mat_lu = [
            [sg.Text("L&R kombiniert")],
            [sg.Multiline(key="-MATRIXLU-", size=(20, 10))]
        ]
        # Layout für Matrixmultiplikation
        layout_multi = [
            [sg.Text("Matrixmultiplikation")],
            [sg.Text(
                "Geben Sie zwei Matrizen zum Multiplizieren ein, \nz. B. [[1, 2, 3], [4, 5, 6], [7, 8, 9]]")],
            [sg.Column(column_mat_a), sg.VerticalSeparator(),
             sg.Column(column_mat_b)],
            [sg.Button("Multiplizieren")],
            [sg.Text("Ergebnis:")],
            [sg.Multiline(key="-RESULT-", size=(48, 8))]
        ]
        # Layout für Gauß und LR-Zerlegung
        layout_lu_decomposition = [
            [sg.Text("LR-Zerlegung")],
            [sg.Text(
                "Geben Sie eine Matrix zum Zerlegen ein")],
            [sg.Multiline(key="-INPUTLU-", size=(48, 8))],
            [sg.Button("Zerlegen")],
            [sg.Text("Ergebnisse:")],
            [sg.Column(column_mat_l),
             sg.Column(column_mat_u),
             sg.Column(column_mat_lu)]
        ]

        # Gesamtlayout & Window
        layout = [[sg.Column(layout_multi), sg.VerticalSeparator(color="black"),
                  sg.Column(layout_lu_decomposition)], [sg.Button("Schließen")]]

        window = sg.Window(
            "Matrixmultiplikation & LR-Zerlegung", layout, resizable=True)

        # Erstellt event loop - wartet auf Benutzeraktion
        while True:
            event, values = window.read()
            if event == "Schließen" or event == sg.WIN_CLOSED:
                break

            # Matrixmultiplikation!
            if event == "Multiplizieren":
                matrix_a = self.util.format_matrix_str_to_list(
                    values["-MATRIXA-"])
                matrix_b = self.util.format_matrix_str_to_list(
                    values["-MATRIXB-"])
                if matrix_a == None or matrix_b == None:
                    break

                if type(matrix_a) == str:
                    result = matrix_a
                elif type(matrix_b) == str:
                    result = matrix_b
                else:
                    result = self.util.get_products(matrix_a, matrix_b)

                window["-RESULT-"].update(
                    self.util.format_matrix_list_to_str(result))

            # Vorbereitung für Gauß: Übergibt Matrix an den Gauß-Algorithmus
            if event == "Zerlegen":
                input = self.util.format_matrix_str_to_list(
                    values["-INPUTLU-"])
                if input == None:
                    break
                try:
                    l_mat, u_mat, j_matrix = self.gauss.lu_decomposition(input)
                    window["-MATRIXL-"].update(
                        self.util.format_matrix_list_to_str(l_mat))
                    window["-MATRIXU-"].update(
                        self.util.format_matrix_list_to_str(u_mat))
                    window["-MATRIXLU-"].update(self.util.format_matrix_list_to_str(j_matrix))
                except ValueError:
                    window["-INPUTLU-"].print("\n Falsches Format, bitte neue Matrix eingeben")
        window.close()