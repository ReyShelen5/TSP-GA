import utils
import random
import argparse
import tsp_ga as ga
from datetime import datetime


def run(args):

    # =====================================================
    # Read all cities from CSV
    # =====================================================
    all_genes = utils.get_genes_from(args.cities_fn)

    print("\nAvailable Cities\n")

    for i, city in enumerate(all_genes):
        print(f"{i+1}. {city.name}")

    print()

    n = int(input("Enter number of cities to use: "))

    genes = []

    print("\nEnter the indices of the cities:\n")

    for i in range(n):

        idx = int(input(f"City {i+1}: "))

        genes.append(all_genes[idx-1])

    print("\nSelected Cities\n")

    for city in genes:
        print(city.name)

    # =====================================================
    # Run the Genetic Algorithm
    # =====================================================

    if args.verbose:
        print("\nRunning TSP-GA with", len(genes), "cities...\n")

    history = ga.run_ga(
        genes,
        args.pop_size,
        args.n_gen,
        args.tourn_size,
        args.mut_rate,
        args.verbose
    )

    # =====================================================
    # Display Optimal Route
    # =====================================================

    print("\n===================================")
    print("OPTIMAL ROUTE")
    print("===================================\n")

    for i, city in enumerate(history['route'].genes):

        print(
            f"{i+1}. {city.name} "
            f"({city.lat:.4f}, {city.lng:.4f})"
        )

    print(f"\nTotal Distance : {history['route'].travel_cost} KM")

    # =====================================================
    # Plot
    # =====================================================

    if args.verbose:
        print("\nDrawing Route...\n")

    utils.plot(
        history['cost'],
        history['route']
    )

    if args.verbose:
        print("\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--pop_size', type=int, default=500, help='Population size')
    parser.add_argument('--tourn_size', type=int, default=50, help='Tournament size')
    parser.add_argument('--mut_rate', type=float, default=0.02, help='Mutation rate')
    parser.add_argument('--n_gen', type=int, default=20, help='Number of equal generations before stopping')
    parser.add_argument('--cities_fn', type=str, default="data/cities.csv", help='Data containing the geographical coordinates of cities')

    

# Convert to float timestamp
    random.seed(datetime.now().timestamp())
    args = parser.parse_args()

    if args.tourn_size > args.pop_size:
        raise argparse.ArgumentTypeError('Tournament size cannot be bigger than population size.')

    run(args)