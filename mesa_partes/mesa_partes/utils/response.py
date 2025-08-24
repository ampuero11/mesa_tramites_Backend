def custom_response(type="success", dto=None, listMessages=None):
    """
    Wrapper para respuestas unificadas.
    type: 'success', 'error', 'warning', etc.
    dto: objeto o lista con datos
    listMessages: lista de strings con mensajes
    """
    if listMessages is None:
        listMessages = []

    return {
        "type": type,
        "dto": dto,
        "listMessages": listMessages
    }
