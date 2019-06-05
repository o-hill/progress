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
#                                   Schema
# -----------------------------------------------------------------------------

class PlotData(ObjectType):
    '''Data for a single plot.'''
    title = String()
    data = List(Float)
    name = String()

class NetworkSchema(ObjectType):
    '''Data for a single network object.'''
    name = String(required=True)
    title = String()
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




# -----------------------------------------------------------------------------
#                                  Helpers
# -----------------------------------------------------------------------------


def build_network_schema(name: str) -> NetworkSchema:
    '''Return a single NetworkSchema.'''

    # Read the data.
    df = pd.read_csv(f'{BASE_PATH}/{name.split("/")[-1].split(".")[0]}.csv')
    index = list(range(0, df.shape[0], int(max(1, df.shape[0]/1000))))

    # Always take the most recent value.
    if index[-1] != df.shape[0] - 1:
        index += [df.shape[0] - 1]

    # Create the network object with the associated data found on disk.
    return NetworkSchema(
        name = name,
        title = name.split('/')[-1],
        n_plots = len(df.columns),
        plot_names = list(df.columns.values),
        plot_data = [
            PlotData(
                title=n,
                data=d.values[index],
                name=n.lower().replace(' ', '_'))
            for n, d in df.iteritems()
        ]
    )

# -----------------------------------------------------------------------------
#                                  Resolvers
# -----------------------------------------------------------------------------

def resolve_networks(root, info) -> list:
    '''Return the list of available networks that have data.'''
    return [build_network_schema(name) for name in sorted(glob(f'{BASE_PATH}/*.csv'))]


def resolve_network(root, info, name: str) -> NetworkSchema:
    '''Return a single network object.'''
    return build_network_schema(name)

# -----------------------------------------------------------------------------
#                               Published API
# -----------------------------------------------------------------------------

class Mutations(ObjectType):
    update_network = UpdateNetwork.Field()

class Query(ObjectType):
    networks = List(NetworkSchema,
        resolver=resolve_networks)
    network = Field(NetworkSchema,
        args={ 'name': String() },
        resolver=resolve_network)

schema = Schema(query=Query, mutation=Mutations)


