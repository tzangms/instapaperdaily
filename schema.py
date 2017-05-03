import graphene

import app.schema

class Query(app.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
