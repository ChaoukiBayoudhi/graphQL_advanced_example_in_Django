###############################################################################
# This is the root schema file that combines all app-level GraphQL schemas.
# It aggregates queries and mutations from different Django apps into a single
# schema that will be used by the GraphQL endpoint.
###############################################################################

# Import the base GraphQL library
import graphene

# Import Query and Mutation classes from the publications app
# PubQuery: Handles all read operations for publications
# PubMut: Handles all write operations for publications
from publications.schema import Query as PubQuery, Mutation as PubMut

# Import Query and Mutation classes from the reviewers app
# RevQuery: Handles all read operations for reviewers
# RevMut: Handles all write operations for reviewers
from reviewers.schema    import Query as RevQuery, Mutation as RevMut

class Query(PubQuery, RevQuery, graphene.ObjectType):
    """
    Root Query class that inherits from all app-level queries.
    This combines all read operations from different apps into a single Query interface.
    - PubQuery: Publication-related queries
    - RevQuery: Reviewer-related queries
    """
    pass

class Mutation(PubMut, RevMut, graphene.ObjectType):
    """
    Root Mutation class that inherits from all app-level mutations.
    This combines all write operations from different apps into a single Mutation interface.
    - PubMut: Publication-related mutations
    - RevMut: Reviewer-related mutations
    """
    pass

# Create the root schema by combining the Query and Mutation classes
# This schema will be used by the GraphQL endpoint to handle all operations
schema = graphene.Schema(query=Query, mutation=Mutation)
