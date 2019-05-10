'''

    GraphQL Schema.

'''

from graphene import ObjectType, List, Schema, String, Int
from glob import glob
import numpy as np

BASE_PATH = '/Users/oliverhill/.network_progress'


class NetworkSchema(ObjectType):
    name = String()
    n_plots = Int()


class AvailableNetworks(ObjectType):
    networks = List(NetworkSchema)

    def resolve_networks(root, info):
        ret = [ ]

        # Build the network objects from the available CSV files.
        for network in sorted(glob(f'{BASE_PATH}/*.txt')):
            ret.append(NetworkSchema(
                name = network.split('/')[-1].split('.')[0],
                n_plots = np.random.randint(200)
            ))

        return ret



schema = Schema(query=AvailableNetworks)

