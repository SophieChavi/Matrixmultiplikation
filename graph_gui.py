# -*- coding: utf-8 -*-
import FreeSimpleGUI as sg
from graph import Graph

class GraphGUI:
    def __init__(self):
        self.graph = Graph()
    
    def start_gui(self):
        sg.set_options(font=("Helvetica", 12))
        
        # Layout für Graph-Eingabe
        layout_input = [
            [sg.Text("Graph-Eingabe", font=("Helvetica", 15, "bold"))],
            [sg.Text("Format: A-B:5, B-C:3, A-C:7")],
            [sg.Text("(Knoten-Knoten:Gewicht, durch Komma getrennt)")],
            [sg.Multiline(key="-GRAPHINPUT-", size=(50, 8), 
                         default_text="A-B:4, A-C:2, B-C:1, B-D:5, C-D:3")],
            [sg.Button("Matrizen berechnen"), sg.Button("Beispiel laden")]
        ]
        
        # Layout für Distanzmatrix
        layout_distance = [
            [sg.Text("Initiale Distanzmatrix (mit ∞):", font=("Helvetica", 12, "bold"))],
            [sg.Multiline(key="-INITIALDIST-", size=(50, 12), disabled=True)],
            [sg.Text("Finale Distanzmatrix (kürzeste Wege):", font=("Helvetica", 12, "bold"))],
            [sg.Multiline(key="-DISTANCE-", size=(50, 12), disabled=True)]
        ]
        
        # Layout für Routingmatrix
        layout_routing = [
            [sg.Text("Initiale Routingmatrix:", font=("Helvetica", 12, "bold"))],
            [sg.Multiline(key="-INITIALROUTE-", size=(50, 12), disabled=True)],
            [sg.Text("Finale Routingmatrix (nächster Knoten):", font=("Helvetica", 12, "bold"))],
            [sg.Multiline(key="-ROUTING-", size=(50, 12), disabled=True)]
        ]
        
        # Layout für Pfadsuche
        layout_path = [
            [sg.Text("Pfadsuche:", font=("Helvetica", 12, "bold"))],
            [sg.Text("Start:"), sg.Input(key="-START-", size=(10, 1)), 
             sg.Text("Ziel:"), sg.Input(key="-END-", size=(10, 1)),
             sg.Button("Pfad finden")],
            [sg.Text("Kürzester Pfad:")],
            [sg.Multiline(key="-PATH-", size=(50, 4), disabled=True)]
        ]
        
        # Gesamtlayout
        layout = [
            [sg.Column(layout_input)],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_distance), sg.VerticalSeparator(), sg.Column(layout_routing)],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_path)],
            [sg.Button("Schließen")]
        ]
        
        window = sg.Window("Graph - Distanz- und Routingmatrix", layout, resizable=True, size=(1200, 950))
        
        while True:
            event, values = window.read()
            
            if event == "Schließen" or event == sg.WIN_CLOSED:
                break
            
            if event == "Beispiel laden":
                # Lade ein komplexeres Beispiel
                example = "1-2:7, 1-3:9, 1-6:14, 2-3:10, 2-4:15, 3-4:11, 3-6:2, 4-5:6, 5-6:9"
                window["-GRAPHINPUT-"].update(example)
            
            if event == "Matrizen berechnen":
                try:
                    # Neuen Graph erstellen
                    self.graph = Graph()
                    graph_string = values["-GRAPHINPUT-"]
                    
                    if not graph_string.strip():
                        window["-DISTANCE-"].update("Fehler: Bitte geben Sie einen Graphen ein!")
                        continue
                    
                    # Graph einlesen
                    self.graph.read_from_string(graph_string)
                    
                    # Initiale Matrizen berechnen
                    initial_dist, initial_route, nodes = self.graph.get_initial_matrices()
                    initial_dist_str = self.graph.format_distance_matrix_str(initial_dist, nodes)
                    window["-INITIALDIST-"].update(initial_dist_str)
                    
                    initial_route_str = self.graph.format_routing_matrix_str(initial_route, nodes)
                    window["-INITIALROUTE-"].update(initial_route_str)
                    
                    # Finale Distanzmatrix berechnen
                    dist, nodes = self.graph.get_distance_matrix()
                    distance_str = self.graph.format_distance_matrix_str(dist, nodes)
                    window["-DISTANCE-"].update(distance_str)
                    
                    # Finale Routingmatrix berechnen
                    routing, nodes = self.graph.get_routing_matrix()
                    routing_str = self.graph.format_routing_matrix_str(routing, nodes)
                    window["-ROUTING-"].update(routing_str)
                    
                    window["-PATH-"].update("Matrizen erfolgreich berechnet!")
                    
                except ValueError as e:
                    error_msg = f"Fehler: {str(e)}"
                    window["-INITIALDIST-"].update(error_msg)
                    window["-INITIALROUTE-"].update("")
                    window["-DISTANCE-"].update("")
                    window["-ROUTING-"].update("")
                    window["-PATH-"].update(error_msg)
                except Exception as e:
                    error_msg = f"Unerwarteter Fehler: {str(e)}"
                    window["-INITIALDIST-"].update(error_msg)
                    window["-INITIALROUTE-"].update("")
                    window["-DISTANCE-"].update("")
                    window["-ROUTING-"].update("")
                    window["-PATH-"].update(error_msg)
            
            if event == "Pfad finden":
                try:
                    start = values["-START-"].strip()
                    end = values["-END-"].strip()
                    
                    if not start or not end:
                        window["-PATH-"].update("Fehler: Bitte Start- und Zielknoten angeben!")
                        continue
                    
                    # Pfad finden
                    path = self.graph.get_path(start, end)
                    
                    if not path:
                        window["-PATH-"].update(f"Kein Pfad von {start} nach {end} gefunden!")
                    else:
                        path_str = " -> ".join(path)
                        
                        # Distanz berechnen
                        dist, nodes = self.graph.get_distance_matrix()
                        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
                        i = node_to_idx[start]
                        j = node_to_idx[end]
                        distance = dist[i][j]
                        
                        result = f"Pfad: {path_str}\n"
                        result += f"Gesamtdistanz: {distance:.1f}"
                        window["-PATH-"].update(result)
                        
                except ValueError as e:
                    window["-PATH-"].update(f"Fehler: {str(e)}")
                except Exception as e:
                    window["-PATH-"].update(f"Unerwarteter Fehler: {str(e)}")
        
        window.close()


if __name__ == "__main__":
    gui = GraphGUI()
    gui.start_gui()
