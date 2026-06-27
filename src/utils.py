import matplotlib.pyplot as plt
import tsp_ga as ga
import pandas as pd
from random import sample
from mpl_toolkits.basemap import Basemap


def get_genes_from(fn, sample_n=0):
    df = pd.read_csv(fn)
    genes = [ga.Gene(row['city'], row['latitude'], row['longitude'])
             for _, row in df.iterrows()]

    return genes if sample_n <= 0 else sample(genes, sample_n)


def plot(costs, individual, save_to=None):
    plt.figure(1)
    plt.subplot(121)
    plot_ga_convergence(costs)

    plt.subplot(122)
    plot_route(individual)

    if save_to is not None:
        plt.savefig(save_to)
        plt.close()
    else:
        plt.show()

def plot_ga_convergence(costs):
    x = range(len(costs))
    plt.title("GA Convergence")
    plt.xlabel('generation')
    plt.ylabel('cost (KM)')
    plt.text(x[len(x) // 2], costs[0], 'min cost: {} KM'.format(costs[-1]), ha='center', va='center')
    plt.plot(x, costs, '-')


def plot_route(individual):

    # =====================================================
    # ===== MODIFIED =====
    # Automatically determine map boundaries
    # =====================================================

    lats = [g.lat for g in individual.genes]
    lngs = [g.lng for g in individual.genes]

    m = Basemap(
        projection='merc',
        llcrnrlat=min(lats)-2,
        urcrnrlat=max(lats)+2,
        llcrnrlon=min(lngs)-2,
        urcrnrlon=max(lngs)+2,
        resolution='i'
    )

    m.drawcoastlines()
    m.drawcountries()

    plt.title("Shortest Route")

    for i in range(len(individual.genes)):

        city = individual.genes[i]

        x, y = m(city.lng, city.lat)

        plt.plot(x, y, 'ro', markersize=6)

        # =====================================================
        # ===== ADDED =====
        # Display city name beside every point
        # =====================================================

        plt.text(
            x,
            y,
            city.name,
            fontsize=9,
            color='blue'
        )

        if i == len(individual.genes)-1:
            nxt = individual.genes[0]
        else:
            nxt = individual.genes[i+1]

        x2, y2 = m(nxt.lng, nxt.lat)

        plt.plot(
            [x, x2],
            [y, y2],
            'r-',
            linewidth=2
        )
