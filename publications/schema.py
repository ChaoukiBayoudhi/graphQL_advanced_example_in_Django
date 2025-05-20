# Required GraphQL imports
import graphene
from graphene_django import DjangoObjectType
from .models import Publication
from .models import ReviewAssignment

# Define the Publication type for GraphQL schema
# This maps the Publication model to a GraphQL type
class PublicationType(DjangoObjectType):
    class Meta:
        model = Publication
        fields = ('id', 'title', 'abstract', 'published_date')

# Define Query class for handling GraphQL queries
class Query(graphene.ObjectType):
    # Query to fetch all publications
    all_publications = graphene.List(PublicationType)

    # Query to fetch publications within a date range
    # Requires both start_date and end_date parameters
    publications_by_date = graphene.List(
        PublicationType,
        start_date=graphene.Date(required=True),
        end_date=graphene.Date(required=True)
    )

    # Resolver method for all_publications query
    def resolve_all_publications(self, info):
        return Publication.objects.all()

    # Resolver method for publications_by_date query
    # Returns publications filtered by date range and ordered by published_date
    def resolve_publications_by_date(self, info, start_date, end_date):
        return Publication.objects.filter(
            published_date__gte=start_date,
            published_date__lte=end_date
        ).order_by('published_date')


# Define ReviewAssignment type for GraphQL schema
class ReviewAssignmentNode(DjangoObjectType):
    class Meta:
        model = ReviewAssignment
        fields = ('id', 'publication', 'reviewer', 'status', 'assigned_at')

# Mutation for handling review assignments
class ReviewAssignmentMutation(graphene.Mutation):
    review_assignment = graphene.Field(ReviewAssignmentNode)
    
    # Define required arguments for the mutation
    class Arguments:
        publication_id = graphene.ID(required=True)
        reviewer_id    = graphene.ID(required=True)
        status         = graphene.String(required=True)
    
    # Mutation resolver method
    def mutate(self, info, publication_id, reviewer_id, status):
        # Get publication and reviewer objects
        publication = Publication.objects.get(pk=publication_id)
        reviewer    = Reviewer.objects.get(pk=reviewer_id)
        
        # Create or get existing review assignment
        review_assignment, _ = ReviewAssignment.objects.get_or_create(
            publication=publication,
            reviewer=reviewer
        )
        # Update status and save
        review_assignment.status = status
        review_assignment.save()
        return ReviewAssignmentMutation(review_assignment=review_assignment)

# Mutation for creating new publications
class CreatePublication(graphene.Mutation):
    publication = graphene.Field(PublicationType)

    # Define required fields for publication creation
    class Arguments:
        title          = graphene.String(required=True)
        abstract       = graphene.String(required=True)
        published_date = graphene.Date(required=True)

    # Mutation resolver to create and save new publication
    def mutate(self, info, title, abstract, published_date):
        pub = Publication(
            title=title,
            abstract=abstract,
            published_date=published_date
        )
        pub.save()
        return CreatePublication(publication=pub)

# Mutation for updating publication abstract
class UpdatePublicationAbstract(graphene.Mutation):
    publication = graphene.Field(PublicationType)

    # Define required arguments for abstract update
    class Arguments:
        id       = graphene.ID(required=True)
        abstract = graphene.String(required=True)

    # Mutation resolver to update publication abstract
    def mutate(self, info, id, abstract):
        pub = Publication.objects.get(pk=id)
        pub.abstract = abstract
        pub.save()
        return UpdatePublicationAbstract(publication=pub)

# Mutation for bulk deleting publications
class BulkDeletePublications(graphene.Mutation):
    success_count = graphene.Int()

    # Define list of IDs as required argument
    class Arguments:
        ids = graphene.List(graphene.ID, required=True)

    # Mutation resolver to delete multiple publications
    def mutate(self, info, ids):
        qs = Publication.objects.filter(pk__in=ids)
        count = qs.count()
        qs.delete()
        return BulkDeletePublications(success_count=count)

# Root Mutation class that combines all mutations
class Mutation(graphene.ObjectType):
    create_publication            = CreatePublication.Field()
    update_publication_abstract   = UpdatePublicationAbstract.Field()
    bulk_delete_publications      = BulkDeletePublications.Field()
    assign_review                 = ReviewAssignmentMutation.Field()
