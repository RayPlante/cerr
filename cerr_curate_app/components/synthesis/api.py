from cerr_curate_app.components.synthesis.models import Synthesis


def get_by_id(synthesis_id):
    """

    :param synthesis_id:
    :return: Synthesis
    """
    return Synthesis.get_by_id(synthesis_id)


def get_list_by_id(id_list):
    """

    :param id_list: list of synthesis ids
    :return: list of synthesis objects
    """
    synthesis = []
    for id in id_list:
        synthesis.append(Synthesis.get_by_id(id))
    return synthesis


def get_all():
    """List of all synthesis

    Returns:

        List of all synthesis
    """
    return Synthesis.get_all()
