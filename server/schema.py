'''

    GraphQL Schema.

'''

from graphene import ObjectType, List, Schema, String, Int, Mutation
from glob import glob
import numpy as np

BASE_PATH = '/Users/oliverhill/.network_progress'


plots = np.random.randint(200, size=3)


class NetworkSchema(ObjectType):
    name = String()
    n_plots = Int()


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
    networks = List(NetworkSchema)

    def resolve_networks(root, info):
        ret = [ ]

        # Build the network objects from the available CSV files.
        for i, network in enumerate(sorted(glob(f'{BASE_PATH}/*.txt'))):
            ret.append(NetworkSchema(
                name = network.split('/')[-1].split('.')[0],
                n_plots = plots[i]
            ))

        return ret



schema = Schema(query=Query, mutation=Mutations)

