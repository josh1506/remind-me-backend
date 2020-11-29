import facebook


class Facebook:
    @staticmethod
    def validate(auth_token):
        try:
            graph = facebook.GraphAPI(auth_token)
            profile = graph.request('/me?fields=name,email')

            return profile

        except:
            return {'error': 'Token is invalid or expired.'}
