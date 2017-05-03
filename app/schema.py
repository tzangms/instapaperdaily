from django.contrib.auth.models import User

import graphene

from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.AbstractType):
    all_users = graphene.List(UserType)

    def resolve_all_users(self, args, context, info):
        return User.objects.all()


