# -*- coding: utf-8 -*-
import sys

class Graph:
    def __init__(self):
        """
        Initialisiert einen leeren Graphen.
        """
        self.nodes = set()
        self.edges = {}  # Dictionary: (node1, node2) -> weight
        
    def add_node(self, node):
        """
        Fügt einen Knoten zum Graphen hinzu.
        
        Args:
            node: Knotenbezeichnung (String oder Integer)
        """
        self.nodes.add(node)
        
    def add_edge(self, node1, node2, weight):
        """
        Fügt eine bewertete Kante zum Graphen hinzu.
        
        Args:
            node1: Startknoten
            node2: Endknoten
            weight: Gewicht/Bewertung der Kante
        """
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.edges[(node1, node2)] = weight
        self.edges[(node2, node1)] = weight  # Ungerichteter Graph
        
    def read_from_string(self, graph_string):
        """
        Liest einen Graphen aus einem String ein.
        Format: "A-B:5, B-C:3, A-C:7" wobei A-B:5 bedeutet Kante von A nach B mit Gewicht 5
        
        Args:
            graph_string: String mit Kantendefinitionen
        """
        try:
            edges_list = graph_string.strip().split(',')
            for edge_str in edges_list:
                edge_str = edge_str.strip()
                if not edge_str:
                    continue
                    
                # Format: "A-B:5"
                parts = edge_str.split(':')
                if len(parts) != 2:
                    raise ValueError(f"Ungültiges Format: {edge_str}. Erwartet: 'A-B:5'")
                
                nodes_part = parts[0].strip()
                weight = float(parts[1].strip())
                
                nodes = nodes_part.split('-')
                if len(nodes) != 2:
                    raise ValueError(f"Ungültiges Knotenformat: {nodes_part}. Erwartet: 'A-B'")
                
                node1 = nodes[0].strip()
                node2 = nodes[1].strip()
                
                self.add_edge(node1, node2, weight)
                
            return True
        except Exception as e:
            raise ValueError(f"Fehler beim Einlesen des Graphen: {str(e)}")
    
    def floyd_warshall(self, return_initial=False):
        """
        Berechnet kürzeste Wege zwischen allen Knotenpaaren mit Floyd-Warshall Algorithmus.
        
        Args:
            return_initial: Wenn True, gibt auch die initialen Matrizen zurück
        
        Returns:
            tuple: (Distanzmatrix, Routingmatrix, Knotenliste) oder
                   (Distanzmatrix, Routingmatrix, Knotenliste, Initial_Dist, Initial_Routing)
            tuple: (Distanzmatrix, Routingmatrix, Knotenliste)
        """
        if not self.nodes:
            raise ValueError("Graph ist leer!")
        
        # Knoten sortieren für konsistente Reihenfolge
        nodes_list = sorted(list(self.nodes))
        n = len(nodes_list)
        
        # Index-Mapping erstellen
        node_to_idx = {node: idx for idx, node in enumerate(nodes_list)}
        
        # Initialisiere Distanzmatrix mit Unendlich
        INF = float('inf')
        dist = [[INF for _ in range(n)] for _ in range(n)]
        next_node = [[None for _ in range(n)] for _ in range(n)]
        
        # Setze Diagonale auf 0
        for i in range(n):
            dist[i][i] = 0
            next_node[i][i] = nodes_list[i]
        
        # Setze direkte Kanten
        for (node1, node2), weight in self.edges.items():
            i = node_to_idx[node1]
            j = node_to_idx[node2]
            dist[i][j] = weight
            next_node[i][j] = node2
        
        # Kopiere initiale Matrizen wenn gewünscht
        if return_initial:
            import copy
            initial_dist = copy.deepcopy(dist)
            initial_next = copy.deepcopy(next_node)
        
        # Floyd-Warshall Algorithmus
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
        
        # Prüfe auf negative Zyklen
        for i in range(n):
            if dist[i][i] < 0:
                raise ValueError("Graph enthält negative Zyklen!")
        
        # Prüfe Zusammenhang (nur für finale Matrix)
        if not return_initial:
            for i in range(n):
                for j in range(n):
                    if dist[i][j] == INF:
                        raise ValueError(f"Graph ist nicht zusammenhängend! "
                                       f"Keine Verbindung zwischen {nodes_list[i]} und {nodes_list[j]}")
        
        if return_initial:
            return dist, next_node, nodes_list, initial_dist, initial_next
        
        return dist, next_node, nodes_list
    
    def get_initial_matrices(self):
        """
        Gibt die initialen Distanz- und Routingmatrizen zurück (vor Floyd-Warshall).
        
        Returns:
            tuple: (Initial_Distanzmatrix, Initial_Routingmatrix, Knotenliste)
        """
        _, _, nodes_list, initial_dist, initial_next = self.floyd_warshall(return_initial=True)
        return initial_dist, initial_next, nodes_list
    
    def get_distance_matrix(self):
        """
        Erstellt die Distanzmatrix mit kürzesten Wegen.
        
        Returns:
            tuple: (Distanzmatrix, Knotenliste)
        """
        dist, _, nodes_list = self.floyd_warshall()
        return dist, nodes_list
    
    def get_routing_matrix(self):
        """
        Erstellt die Routingmatrix (nächster Knoten für kürzesten Weg).
        
        Returns:
            tuple: (Routingmatrix, Knotenliste)
        """
        _, next_node, nodes_list = self.floyd_warshall()
        return next_node, nodes_list
    
    def get_path(self, start, end):
        """
        Gibt den kürzesten Pfad zwischen zwei Knoten zurück.
        
        Args:
            start: Startknoten
            end: Endknoten
            
        Returns:
            list: Liste von Knoten entlang des kürzesten Pfads
        """
        _, next_node, nodes_list = self.floyd_warshall()
        
        if start not in self.nodes or end not in self.nodes:
            raise ValueError("Start- oder Endknoten nicht im Graph!")
        
        node_to_idx = {node: idx for idx, node in enumerate(nodes_list)}
        i = node_to_idx[start]
        j = node_to_idx[end]
        
        if next_node[i][j] is None:
            return []
        
        path = [start]
        current = start
        while current != end:
            i = node_to_idx[current]
            j = node_to_idx[end]
            current = next_node[i][j]
            path.append(current)
        
        return path
    
    def format_distance_matrix_str(self, dist, nodes_list):
        """
        Formatiert die Distanzmatrix als lesbaren String.
        
        Args:
            dist: Distanzmatrix
            nodes_list: Liste der Knoten
            
        Returns:
            str: Formatierte Distanzmatrix
        """
        n = len(nodes_list)
        INF = float('inf')
        
        # Spaltenbreite berechnen (berücksichtige ∞ Symbol)
        max_len = max(len(str(nodes_list[i])) for i in range(n))
        for i in range(n):
            for j in range(n):
                if dist[i][j] == INF:
                    max_len = max(max_len, 1)  # Länge von ∞
                else:
                    max_len = max(max_len, len(f"{dist[i][j]:.1f}"))
        col_width = max_len + 2
        
        # Header
        result = " " * col_width
        for node in nodes_list:
            result += f"{node:>{col_width}}"
        result += "\n"
        
        # Zeilen
        for i in range(n):
            result += f"{nodes_list[i]:>{col_width}}"
            for j in range(n):
                if dist[i][j] == INF:
                    result += f"{'∞':>{col_width}}"
                else:
                    result += f"{dist[i][j]:>{col_width}.1f}"
            result += "\n"
        
        return result
    
    def format_routing_matrix_str(self, next_node, nodes_list):
        """
        Formatiert die Routingmatrix als lesbaren String.
        
        Args:
            next_node: Routingmatrix
            nodes_list: Liste der Knoten
            
        Returns:
            str: Formatierte Routingmatrix
        """
        n = len(nodes_list)
        
        # Spaltenbreite berechnen
        max_len = max(len(str(nodes_list[i])) for i in range(n))
        max_len = max(max_len, max(len(str(next_node[i][j]) if next_node[i][j] else "-") 
                                    for i in range(n) for j in range(n)))
        col_width = max_len + 2
        
        # Header
        result = " " * col_width
        for node in nodes_list:
            result += f"{node:>{col_width}}"
        result += "\n"
        
        # Zeilen
        for i in range(n):
            result += f"{nodes_list[i]:>{col_width}}"
            for j in range(n):
                next_val = next_node[i][j] if next_node[i][j] else "-"
                result += f"{next_val:>{col_width}}"
            result += "\n"
        
        return result


if __name__ == "__main__":
    # Beispiel
    graph = Graph()
    
    # Beispiel 1: Einfacher Graph
    print("=== Beispiel 1: Einfacher Graph ===")
    graph.read_from_string("A-B:4, A-C:2, B-C:1, B-D:5, C-D:3")
    
    dist, nodes = graph.get_distance_matrix()
    print("\nDistanzmatrix:")
    print(graph.format_distance_matrix_str(dist, nodes))
    
    routing, nodes = graph.get_routing_matrix()
    print("Routingmatrix (nächster Knoten):")
    print(graph.format_routing_matrix_str(routing, nodes))
    
    print("\nKürzester Pfad von A nach D:")
    path = graph.get_path("A", "D")
    print(" -> ".join(path))
    
    # Beispiel 2: Komplexerer Graph
    print("\n=== Beispiel 2: Komplexerer Graph ===")
    graph2 = Graph()
    graph2.read_from_string("1-2:7, 1-3:9, 1-6:14, 2-3:10, 2-4:15, 3-4:11, 3-6:2, 4-5:6, 5-6:9")
    
    dist2, nodes2 = graph2.get_distance_matrix()
    print("\nDistanzmatrix:")
    print(graph2.format_distance_matrix_str(dist2, nodes2))
    
    routing2, nodes2 = graph2.get_routing_matrix()
    print("Routingmatrix (nächster Knoten):")
    print(graph2.format_routing_matrix_str(routing2, nodes2))
