from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)

    token['username'] = user.username
    token['organization'] = None if user.organization == None else user.organization.name
    token['organization_slug'] = None if user.organization == None else user.organization.slug
    token['user_id'] = str(user.id)
    token['profile_image'] = user.profile_image
    return token

class CustomObtainTokenPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer