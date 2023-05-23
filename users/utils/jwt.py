"""
    @author: Arif Ipek<arifsamedipek@gmail.com>
    @date: October 3rd, 2021
"""


from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    token = RefreshToken.for_user(user)

    token['id'] = user.id
    token['email'] = user.email
    token['email_validation_time'] = user.email_validation_time.isoformat() \
        if user.email_validation_time else None
    token['full_name'] = user.get_full_name()
    token['first_name'] = user.first_name
    token['last_name'] = user.last_name
    token['date_joined'] = user.date_joined.isoformat()
    token['permissions'] = list(user.get_all_permissions())

    return {
        'refresh_token': str(token),
        'access_token': str(token.access_token),
    }
