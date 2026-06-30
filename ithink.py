import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def create_transport_graph():
    G = nx.Graph()

    # lines and stations
    lines = {
        "Central": ["Liverpool Street", "Bank", "St. Paul's", "Chancery Lane", "Holborn", "Oxford Circus"],
        "Northern": ["Euston", "King's Cross", "Angel", "Old Street", "Moorgate", "Bank"],
        "Piccadilly": ["Holborn", "Covent Garden", "Leicester Square", "Piccadilly Circus", "Green Park", "Hyde Park Corner"],
        "Jubilee": ["Swiss Cottage", "St John's Wood", "Baker Street", "Bond Street", "Green Park", "Westminister"],
        "Elizabeth": ["Acton Main Line", "Paddington", "Bond Street", "Tottenham Court Road", "Farrington", "Liverpool Street"],
        "Bakerloo": ["Baker Street", "Regent's Park", "Oxford Circus", "Piccadilly Circus", "Charing Cross", "Embankment"]
    }

    # distances (in km)
    distances_km = {
        ("Liverpool Street", "Bank"): 0.8, ("Bank", "St. Paul's"): 1.0, ("St. Paul's", "Chancery Lane"): 0.9,
        ("Chancery Lane", "Holborn"): 0.7, ("Holborn", "Oxford Circus"): 1.2,
        ("Euston", "King's Cross"): 0.5, ("King's Cross", "Angel"): 1.1, ("Angel", "Old Street"): 1.3,
        ("Old Street", "Moorgate"): 1.2, ("Moorgate", "Bank"): 0.9,
        ("Holborn", "Covent Garden"): 0.7, ("Covent Garden", "Leicester Square"): 0.3,
        ("Leicester Square", "Piccadilly Circus"): 0.4, ("Piccadilly Circus", "Green Park"): 0.7,
        ("Green Park", "Hyde Park Corner"): 1.0,
        ("Swiss Cottage", "St John's Wood"): 0.7, ("St John's Wood", "Baker Street"): 1.1, ("Baker Street", "Bond Street"): 0.8,
        ("Bond Street", "Green Park"): 0.6, ("Green Park", "Westminister"): 1,
        ("Acton Main Line", "Paddington"): 4.6, ("Paddington", "Bond Street"): 1.4,
        ("Bond Street", "Tottenham Court Road"): 0.6, ("Tottenham Court Road", "Farrington"): 1.3,
        ("Farrington", "Liverpool Street"): 1.1,
        ("Baker Street", "Regent's Park"): 0.7, ("Regent's Park", "Oxford Circus"): 0.9,
        ("Oxford Circus", "Piccadilly Circus"): 0.4, ("Piccadilly Circus", "Charing Cross"): 0.5,
        ("Charing Cross", "Embankment"): 0.6
    }

    # Dictionary of TfL Tube lines and their corresponding colors
    tube_lines_colors = {
        'Bakerloo': '#A67C52',
        'Central': '#E30000',
        'Jubilee': '#8B8D8F',
        'Northern': '#000000',
        'Piccadilly': '#0033A0',
        'Elizabeth': '#800080'

    }

    # Example function to display a tube line and its color
    def get_line_color(line_name):
        return tube_lines_colors.get(line_name, "Line not found")

    # Testing the function
    line_name = 'Central'
    print(f"The color for the {line_name} line is {get_line_color(line_name)}")

    # Convert distances to miles
    distances_miles = {edge: round(km * 0.621371, 2) for edge, km in distances_km.items()}

    # Add edges with attributes (distance in km and miles)
    for (u, v), km in distances_km.items():
        G.add_edge(u, v, km=km, miles=distances_miles[(u, v)])

    return G, lines, distances_km, distances_miles

def visualize_graph(G, lines, unit="km"):
    pos = nx.spring_layout(G, seed=42, k=0.4)  # Improved spacing for readability
    plt.figure(figsize=(12, 8))

    # Tube line colors
    colors = {
        "Central": "red", "Northern": "black", "Piccadilly": "blue",
        "Elizabeth": "Purple", "Jubilee": "grey", "Bakerloo": "brown"
    }

    # Draw nodes and edges for each line
    for line, stations in lines.items():
        available_stations = [s for s in stations if s in pos]
        if available_stations:
            nx.draw_networkx_nodes(G, pos, nodelist=available_stations, node_color=colors[line], node_size=300)
            edges = [(available_stations[i], available_stations[i+1]) for i in range(len(available_stations)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors[line], width=2)

    # Add edge labels for distances
    edge_labels = {(u, v): f"{d[unit]:.1f} {unit}" for u, v, d in G.edges(data=True) if u in pos and v in pos}
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.title("TFL Map", fontsize=14)
    plt.show()

def compute_network_statistics(G, distances_km, distances_miles):
    total_km = sum(distances_km.values())
    total_miles = sum(distances_miles.values())
    avg_km = total_km / len(distances_km)
    avg_miles = total_miles / len(distances_miles)

    return total_km, total_miles, avg_km, avg_miles

def main():
    G, lines, distances_km, distances_miles = create_transport_graph()

    # User input for distance unit
    unit_choice = input("Choose distance unit (km/miles): ").strip().lower()
    if unit_choice not in ["km", "miles"]:
        print("Invalid input, defaulting to km.")
        unit_choice = "km"

    # Visualize the graph with the chosen unit
    visualize_graph(G, lines, unit=unit_choice)

    # Compute network statistics
    total_km, total_miles, avg_km, avg_miles = compute_network_statistics(G, distances_km, distances_miles)

    if unit_choice == "km":
        print(f"Total Network Length: {total_km:.2f} km")
        print(f"Average Distance: {avg_km:.2f} km")
    else:
        print(f"Total Network Length: {total_miles:.2f} miles")
        print(f"Average Distance: {avg_miles:.2f} miles")

if __name__ == "__main__":
    main()