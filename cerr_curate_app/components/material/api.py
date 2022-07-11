from cerr_curate_app.components.material.models import Material


def get_by_id(material_id):
    """

    :param material_id:
    :return: Material
    """
    return Material.get_by_id(material_id)


def get_list_by_id(id_list):
    """

    :param id_list: list of material ids
    :return: list of material objects
    """
    materials = []
    for id in id_list:
        materials.append(Material.get_by_id(id))
    return materials


def get_all():
    """List of all materials

    Returns:

        List of all materials
    """
    return Material.get_all()
