'''

    GraphQL Server for serving training progress.

'''


import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from schema import schema


app = Flask(__name__)
app.debug = True

CORS(app, resources={r'/graphql': { 'origins': '*' }})

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run()

