from cerr_curate_app.components.productclass.models import ProductClass


def get_by_id(productclass_id):
    """

    :param productclass_id:
    :return: ProductClass
    """
    return ProductClass.get_by_id(productclass_id)


def get_list_by_id(id_list):
    """

    :param id_list: list of productclass ids
    :return: list of productclass objects
    """
    productclasss = []
    for id in id_list:
        productclasss.append(ProductClass.get_by_id(id))
    return productclasss


def get_all():
    """List of all productclass

    Returns:

        List of all productclass
    """
    return ProductClass.get_all()
