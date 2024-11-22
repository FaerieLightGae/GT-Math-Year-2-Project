import networkx as nx

# Define the edge list with weights (distances)
edges = [
    ("Northview High School", "A", {"weight": 0.4}),
    ("Northview High School", "B", {"weight": 0.2}),
    ("Northview High School", "C", {"weight": 1.0}),
    ("Northview High School", "D", {"weight": 0.3}),
    ("Northview High School", "E", {"weight": 1.2}),
    ("A", "C", {"weight": 0.6}),
    ("A", "D", {"weight": 0.3}),
    ("B", "C", {"weight": 0.8}),
    ("B", "F", {"weight": 0.3}),
    ("C", "G", {"weight": 0.2}),
    ("G", "H", {"weight": 0.4}),
    ("H", "I", {"weight": 1.0}),
    ("I", "AF", {"weight": 0.6}),
    ("J", "AD", {"weight": 0.9}),
    ("AD", "AE", {"weight": 0.6}),
    ("AE", "AF", {"weight": 1.6}),
    ("AF", "AH", {"weight": 1.3}),
    ("AF", "The Creek Café + Gelato", {"weight": 1.5}),
    ("AE", "The Creek Café + Gelato", {"weight": 0.1}),
    ("Peach Coffee Roosters", "AB", {"weight": 0.7}),
    ("Peach Coffee Roosters", "McDonald's 2", {"weight": 0.4}),
    ("McDonald's 2", "AC", {"weight": 0.8}),
    ("McDonald's 1", "Cafe Rothem", {"weight": 0.3}),
    ("W", "Z", {"weight": 1.9}),
    ("Z", "AA", {"weight": 0.5}),
    ("AB", "Y", {"weight": 1.1}),
    ("AA", "AB", {"weight": 0.4}),
    ("Northview High School", "Seven Sisters Kitchen", {"weight": 1.2}),
    ("K", "McDonald's 1", {"weight": 0.6}),
    ("McDonald's 1", "T", {"weight": 0.8}),
    ("E", "T", {"weight": 0.6}),
    ("T", "U", {"weight": 0.2}),
    ("U", "V", {"weight": 1.3}),
    ("V", "W", {"weight": 0.7}),
    ("W", "X", {"weight": 0.8}),
    ("U", "X", {"weight": 0.8}),
    ("X", "Y", {"weight": 1.2}),
    ("E", "Y", {"weight": 1.2}),
    ("K", "L", {"weight": 1.8}),
    ("F", "L", {"weight": 0.3}),
    ("L", "Q", {"weight": 1.3}),
    ("Q", "R", {"weight": 0.6}),
    ("R", "S", {"weight": 1.2}),
    ("S", "McDonald's 1", {"weight": 1.3}),
    ("B", "M", {"weight": 1.0}),
    ("M", "N", {"weight": 1.0}),
    ("N", "O", {"weight": 1.0}),
    ("O", "P", {"weight": 0.7}),
    ("N", "P", {"weight": 1.2}),
    ("O", "Seven Sisters Kitchen", {"weight": 1.0}),
    ("I", "Seven Sisters Kitchen", {"weight": 0.8}),
    ("C", "J", {"weight": 1.5}),
    ("A", "J", {"weight": 1.6}),
]

# Create the graph
G = nx.Graph()
G.add_edges_from(edges)

# Define cafes and their attributes
cafes = {
    "Cafe Rothem": {"price": 2.99, "rating": 4.8},
    "Peach Coffee Roosters": {"price": 3.00, "rating": 4.8},
    "The Creek Café + Gelato": {"price": 3.00, "rating": 4.9},
    "McDonald's 1": {"price": 1.89, "rating": 2.9},
    "McDonald's 2": {"price": 1.89, "rating": 3.5},
    "Seven Sisters Kitchen": {"price": 2.50, "rating": 4.7},
}

# Get user-defined importance factors
print("Assign importance values (0 to 1) for each factor. The sum must equal 1.")
alpha = float(input("Importance of distance (α): "))
beta = float(input("Importance of price (β): "))
gamma = float(input("Importance of quality (γ): "))

if abs(alpha + beta + gamma - 1) > 1e-6:
    print("Error: The weights must sum to 1. Please try again.")
    exit()

# Normalize price and rating
max_price = max(cafe["price"] for cafe in cafes.values())
max_rating = max(cafe["rating"] for cafe in cafes.values())

def calculate_edge_weight(distance, price, rating):
    # Normalize distance (already provided as edge weight)
    W_distance = distance
    W_price = price / max_price
    W_rating = 1 - (rating / max_rating)  # Higher rating = lower weight

    return alpha * W_distance + beta * W_price + gamma * W_rating

# Update weights for edges dynamically
for u, v, data in G.edges(data=True):
    distance = data["weight"]
    if u in cafes or v in cafes:
        # Use the average price and rating between connected cafes
        price = (cafes.get(u, {}).get("price", 0) + cafes.get(v, {}).get("price", 0)) / 2
        rating = (cafes.get(u, {}).get("rating", 0) + cafes.get(v, {}).get("rating", 0)) / 2
        data["weight"] = calculate_edge_weight(distance, price, rating)

# Apply Prim's algorithm to find MST
mst = nx.minimum_spanning_tree(G, weight="weight")

# Calculate the ranking of cafes based on weights
cafe_scores = {}
for cafe in cafes:
    total_weight = 0
    for neighbor in G.neighbors(cafe):
        if G.has_edge(cafe, neighbor):
            total_weight += G[cafe][neighbor]['weight']
    cafe_scores[cafe] = total_weight

# Rank cafes from best to worst (lowest total weight is best)
ranked_cafes = sorted(cafe_scores.items(), key=lambda x: x[1])

print("\nRanking of Cafes from Best to Worst:")
for rank, (cafe, score) in enumerate(ranked_cafes, start=1):
    print(f"{rank}. {cafe} (Score: {score:.2f})")
    
# Keep the program open until the user closes it
input("\nPress Enter to exit the program.")
