from datetime import datetime, timedelta

from oauthlib.common import generate_signed_token
from oauthlib.oauth2.rfc6749.utils import scope_to_list


def convert_list_to_space_separated(data: list) -> str:
    return " ".join(data)


def convert_dict_to_space_separated(data: dict) -> str:
    data = list(data.keys())
    return " ".join(data)


def convert_scope_str_to_scope_dict(scopes: str) -> dict:
    scopes = scopes.split(" ")
    if not scopes:
        return scopes
    scopes_dict = {}
    resource_arr = []
    for scope in scopes:
        if scope and scope != "__all__":
            resource = scope.split(":")[0]
            permission = scope.split(":")[1]
            if not scopes_dict.get(resource):
                resource_arr.append(resource)
                scopes_dict[resource] = [permission]
            else:
                scopes_dict.get(resource).append(permission)
    formated_scopes = []
    for key in scopes_dict.keys():
        resource_temp_dict = {"scope": key, "label": key}
        children = []
        for permission in scopes_dict.get(key):
            if permission != "super_admin":
                permission_temp_dict = {
                    "scope": key + ":" + permission,
                    "label": permission,
                }
                children.append(permission_temp_dict)
        resource_temp_dict["children"] = children
        formated_scopes.append(resource_temp_dict)
    return formated_scopes


def signed_token_generator(private_pem, **kwargs):
    """
    :param private_pem:
    """

    def signed_token_generator(request):
        from core.settings.base import DEFAULT_CLIENT_ID, DEFAULT_CLIENT_SECRET, NBF_TIME

        now = datetime.utcnow()
        all = {"__all__"}
        client_scopes = set(
            get_scopes_backend().get_available_scopes(
                application=request.client, request=request
            )
        )
        scopes = set(request.scopes) if request.scopes is not None else set()

        # Override scope for the default client
        if (
            request.client_id == DEFAULT_CLIENT_ID
            and request.client_secret == DEFAULT_CLIENT_SECRET
            and request.user.roles
        ):
            scopes = set()
            for role in request.user.roles.all():
                scopes = scopes.union(set(scope_to_list(role.scope)))
            default_scopes = set(
                get_scopes_backend().get_default_scopes(
                    application=request.client, request=request
                )
            )
            scopes = scopes.union(default_scopes)

        # limit request scopes
        if all.issubset(scopes):
            scopes = client_scopes
        valid_scopes = scopes.intersection(client_scopes)

        request.scope = list(valid_scopes)

        request.claims = kwargs

        payload = {
            "iat": now,
            "exp": now + timedelta(seconds=request.expires_in),
            "nbf": now + timedelta(seconds=float(NBF_TIME)),
        }

        try:
            user_id = str(request.user.id)
            payload.update({"sub": user_id})
        except:
            user_id = None

        request.claims.update(
            payload,
        )
        return generate_signed_token(private_pem, request)

    return signed_token_generator


def get_scopes_backend():
    from oauth2_provider.settings import oauth2_settings

    scopes_class = oauth2_settings.SCOPES_BACKEND_CLASS
    return scopes_class()
