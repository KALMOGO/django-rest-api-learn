from rest_framework.authentication import TokenAuthentication as TokenBaseAuthen

        # change the token authentication
class TokenAuthentication(TokenBaseAuthen):
    keyword = 'todos'
    