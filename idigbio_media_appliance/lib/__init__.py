import uuid


def get_uuid_unicode():
    u = uuid.uuid4()
    try:
        return unicode(u)
    except NameError:
        return str(u)
