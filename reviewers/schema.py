
# Import necessary modules and packages
import graphene  # Main GraphQL package for Python
from graphene_django import DjangoObjectType  # For converting Django models to GraphQL types
from django.contrib.auth import get_user_model  # Get the active User model
from django.db.models import Count, Q, F  # For complex database queries

# Import local models
from .models import Reviewer
from publications.schema import ReviewAssignmentNode
from publications.models import ReviewAssignment

# Get the User model that is currently active in this project
User = get_user_model()

# GraphQL type definition for User model
class UserType(DjangoObjectType):
    """
    GraphQL type for User model exposing basic user information
    """
    class Meta:
        model = User
        fields = ("id", "username", "email")

# GraphQL type definition for Reviewer model
class ReviewerType(DjangoObjectType):
    """
    GraphQL type for Reviewer model exposing reviewer details including foreign key to User
    """
    class Meta:
        model = Reviewer
        # now exposes `user` FK as well as your other fields
        fields = ('id', 'name', 'user', 'expertise')

# Define GraphQL queries
class Query(graphene.ObjectType):
    """
    GraphQL Query type defining available queries for reviewers
    """
    # Query to get all reviewers
    all_reviewers = graphene.List(ReviewerType)
    # Query to get a specific reviewer by ID
    reviewer      = graphene.Field(ReviewerType, id=graphene.Int(required=True))
    # Query to get top reviewers based on completed reviews
    top_reviewers  = graphene.List(
        ReviewerType,
        limit=graphene.Int(default_value=5)
    )

    def resolve_all_reviewers(self, info):
        """Resolver to fetch all reviewers with their related user information"""
        return Reviewer.objects.select_related('user').all()

    def resolve_reviewer(self, info, id):
        """Resolver to fetch a specific reviewer by ID"""
        try:
            return Reviewer.objects.get(pk=id)
        except Reviewer.DoesNotExist:
            return None

    def resolve_top_reviewers(self, info, limit):
        """
        Resolver to fetch top reviewers based on number of completed reviews
        Uses annotation to count completed reviews and orders by that count
        """
        return (
            Reviewer.objects
            .annotate(completed=Count('assigned_publications__reviewassignment__status', 
                     filter=Q(reviewassignment__status='completed')))
            .order_by('-completed')[:limit]
        )

# GraphQL mutation for creating a new reviewer
class CreateReviewer(graphene.Mutation):
    """
    Mutation to create a new reviewer
    Requires a name and user_id
    """
    reviewer = graphene.Field(ReviewerType)

    class Arguments:
        name    = graphene.String(required=True)
        user_id = graphene.Int(required=True)

    def mutate(self, info, name, user_id):
        """Creates and returns a new reviewer instance"""
        user = User.objects.get(pk=user_id)
        rev  = Reviewer(name=name, user=user)
        rev.save()
        return CreateReviewer(reviewer=rev)

# GraphQL mutation for updating an existing reviewer
class UpdateReviewer(graphene.Mutation):
    """
    Mutation to update an existing reviewer
    Requires reviewer ID and accepts optional name update
    """
    reviewer = graphene.Field(ReviewerType)

    class Arguments:
        id   = graphene.Int(required=True)
        name = graphene.String()

    def mutate(self, info, id, name=None):
        """Updates and returns the modified reviewer instance"""
        rev = Reviewer.objects.get(pk=id)
        if name is not None:
            rev.name = name
            rev.save()
        return UpdateReviewer(reviewer=rev)

# GraphQL mutation for deleting a reviewer
class DeleteReviewer(graphene.Mutation):
    """
    Mutation to delete an existing reviewer
    Returns success status
    """
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        """Deletes the reviewer and returns success status"""
        deleted, _ = Reviewer.objects.filter(pk=id).delete()
        return DeleteReviewer(success=bool(deleted))

# GraphQL mutation for bulk assigning publications to a reviewer
class BulkAssignReviewer(graphene.Mutation):
    """
    Mutation to assign multiple publications to a reviewer at once
    Creates ReviewAssignment instances for each publication
    """
    assignments = graphene.List(ReviewAssignmentNode)

    class Arguments:
        publication_ids = graphene.List(graphene.ID, required=True)
        reviewer_id     = graphene.ID(required=True)

    def mutate(self, info, publication_ids, reviewer_id):
        """
        Creates review assignments for multiple publications and a single reviewer
        Returns list of created assignments
        """
        from publications.models import Publication
        reviewer = Reviewer.objects.get(pk=reviewer_id)
        pubs     = Publication.objects.filter(pk__in=publication_ids)

        assignments = []
        for pub in pubs:
            # Create or get existing assignment for each publication
            assignment, _ = ReviewAssignment.objects.get_or_create(
                publication=pub,
                reviewer=reviewer
            )
            assignments.append(assignment)

        return BulkAssignReviewer(assignments=assignments)

# Register all mutations
class Mutation(graphene.ObjectType):
    """
    Root mutation class that registers all available mutations
    """
    create_reviewer        = CreateReviewer.Field()
    update_reviewer        = UpdateReviewer.Field()
    delete_reviewer        = DeleteReviewer.Field()
    bulk_assign_reviewer   = BulkAssignReviewer.Field()