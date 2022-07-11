from cerr_curate_app.components.lifecycle.models import Lifecycle


def get_by_id(lifecycle_id):
    """

    :param lifecycle_id:
    :return: Lifecycle
    """
    return Lifecycle.get_by_id(lifecycle_id)


def get_list_by_id(id_list):
    """

    :param id_list: list of lifecycle ids
    :return: list of lifecycle objects
    """
    lifecycle = []
    for id in id_list:
        lifecycle.append(Lifecycle.get_by_id(id))
    return lifecycle


def get_all():
    """List of all lifecycle

    Returns:

        List of all lifecycle
    """
    return Lifecycle.get_all()
