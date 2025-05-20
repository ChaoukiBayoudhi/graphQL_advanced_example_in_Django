"""
URL configuration for graphQL_example project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
# Import the csrf_exempt decorator from django.views.decorators.csrf
# This decorator is used to disable CSRF protection for specific views
# CSRF (Cross-Site Request Forgery) protection is a security feature that prevents unauthorized commands from being transmitted from a user that the website trusts
from django.views.decorators.csrf import csrf_exempt

# Import the GraphQLView from graphene_django.views
# GraphQLView is the main view for handling GraphQL queries
# It provides an interface for processing GraphQL requests and returning responses
from graphene_django.views import GraphQLView

# Define URL patterns for the Django application
urlpatterns = [
     path('admin/', admin.site.urls),
    
    # URL pattern for the GraphQL endpoint
    # When users visit '/graphql/', they will access the GraphQL interface
    # csrf_exempt is used here because GraphQL typically handles its own security
    # graphiql=True enables the GraphiQL interface, which is an in-browser IDE for exploring GraphQL
    # It's a useful tool for testing and development
    # The as_view() method is called to create the view function because it's a class-based view
    # The GraphQLView is wrapped in csrf_exempt to disable CSRF protection for this view
    
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
