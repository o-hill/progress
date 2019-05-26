'''

    GraphQL Schema.

'''

from graphene import ObjectType, List, Schema, String, Int, Mutation, Float, Field
from glob import glob
import numpy as np
import pandas as pd

BASE_PATH = '/Users/oliverhill/.network_progress'


plots = np.random.randint(200, size=3)

# -----------------------------------------------------------------------------
#                                  Resolvers
# -----------------------------------------------------------------------------

def resolve_networks(root, info, names=sorted(glob(f'{BASE_PATH}/*.csv'))) -> list:
    '''Return the list of available networks that have data.'''
    ret = [ ]

    for name in names:

        # Read the data.
        df = pd.read_csv(f'{BASE_PATH}/{name.split("/")[-1].split(".")[0]}.csv')
        index = list(range(0, df.shape[0], int(max(1, df.shape[0]/1000))))

        # Always take the most recent value.
        if index[-1] != df.shape[0] - 1:
            index += [df.shape[0] - 1]

        # Create the network object with the associated data found on disk.
        ret.append(NetworkSchema(
            name = name,
            n_plots = len(df.columns),
            plot_names = list(df.columns.values),
            plot_data = [
                PlotData(
                    title=n,
                    data=d.values[index],
                    name=n.lower().replace(' ', '_'))
                for n, d in df.iteritems()
            ]
        ))

    return ret


# -----------------------------------------------------------------------------
#                                   Schema
# -----------------------------------------------------------------------------

class PlotData(ObjectType):
    title = String()
    data = List(Float)
    name = String()

class NetworkSchema(ObjectType):
    name = String(required=True)
    n_plots = Int()
    plot_names = List(String)
    plot_data = List(PlotData)

class UpdateNetwork(Mutation):
    class Arguments:
        index = Int(required=True)
        n_plot = Int(required=True)

    name = String()
    n_plots = Int()

    @staticmethod
    def mutate(root, info, index: int, n_plot: int):
        plots[index] = n_plot
        name = sorted(glob(f'{BASE_PATH}/*.txt'))[index].split('/')[-1].split('.')[0]

        return UpdateNetwork(n_plots=n_plot, name=name)


class Mutations(ObjectType):
    update_network = UpdateNetwork.Field()


class Query(ObjectType):
    networks = List(NetworkSchema,
        args= { 'names': List(String) },
        resolver=resolve_networks)


schema = Schema(query=Query, mutation=Mutations)

