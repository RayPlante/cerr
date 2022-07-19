import logging
from core_main_app.commons import exceptions

logger = logging.getLogger("cerr_curate_app.discover")


def init_cerr():
    try:
        _create_material_list()
        _create_lifecycle_phase_list()
        _create_product_class_list()
        pass
    except Exception as e:
        logger.error("Impossible to init the registry: {0}".format(str(e)))


def _create_lifecycle_phase_list():
    from cerr_curate_app.components.lifecycle import api as lifecycle_api
    from cerr_curate_app.components.lifecycle.models import Lifecycle

    lifecycle = lifecycle_api.get_all()
    if lifecycle.exists() is False:
        materials_design = Lifecycle.objects.create(name="materials design")
        processing = Lifecycle.objects.create(name="processing")
        product_design = Lifecycle.objects.create(name="product design")
        use_reuse = Lifecycle.objects.create(name="use and reuse")
        repair_refurbishment = Lifecycle.objects.create(name="repair and refurbishment")
        collection_sortation = Lifecycle.objects.create(name="collection and sortation")
        recycling = Lifecycle.objects.create(name="recycling")
        solvent = Lifecycle.objects.create(name="recycling: solvents", parent=recycling)
        mechanical = Lifecycle.objects.create(
            name="recycling: mechanical", parent=recycling
        )
        chemical = Lifecycle.objects.create(
            name="recycling: chemical", parent=recycling
        )
        carbon_capture = Lifecycle.objects.create(name="carbon capture")
        end_life_management = Lifecycle.objects.create(name="end-of-life management")
        unwanted_outcomes = Lifecycle.objects.create(name="unwanted outcomes")
        material_losses = Lifecycle.objects.create(
            name="unwanted outcomes: material losses", parent=unwanted_outcomes
        )
        carbon_emissions = Lifecycle.objects.create(
            name="unwanted outcomes: carbon emissions", parent=unwanted_outcomes
        )
        public_health_impacts = Lifecycle.objects.create(
            name="unwanted outcomes: public health impacts", parent=unwanted_outcomes
        )
        environmental_impacts = Lifecycle.objects.create(
            name="unwanted outcomes: environmental impacts", parent=unwanted_outcomes
        )


def _create_material_list():
    from cerr_curate_app.components.material import api as material_api
    from cerr_curate_app.components.material.models import Material

    materials = material_api.get_all()
    if materials.exists() is False:
        # create method Add init materials
        biomass = Material.objects.create(name="biomass")
        cellulosic = Material.objects.create(name="biomass: cellulosic", parent=biomass)
        food = Material.objects.create(name="biomass: food", parent=biomass)
        compost = Material.objects.create(name="biomass: compost", parent=biomass)
        composites = Material.objects.create(name="composites")
        glass = Material.objects.create(name="glass")
        concrete = Material.objects.create(name="concrete")
        gases = Material.objects.create(name="gases")
        chemicals = Material.objects.create(name="chemicals")
        metals = Material.objects.create(name="metals and alloys")
        metals_rare = Material.objects.create(
            name="metals and alloys: rare earth elements", parent=metals
        )
        metals_ferrous = Material.objects.create(
            name="metals and alloys: ferrous", parent=metals
        )
        metals_non_ferrous = Material.objects.create(
            name="metals and alloys: non-ferrous", parent=metals
        )
        polymers = Material.objects.create(name="polymers: property-based")
        polymers_elastomers = Material.objects.create(
            name="polymers: property-based: elastomers", parent=polymers
        )
        polymers_liquid_crystals = Material.objects.create(
            name="polymers: property-based: liquid crystals", parent=polymers
        )
        polymers_marine_debris = Material.objects.create(
            name="polymers: property-based: marine_debris", parent=polymers
        )
        polymers_micro_nano_plastics = Material.objects.create(
            name="polymers: property-based: micro- and nano-plastics", parent=polymers
        )
        polymers_thermosets = Material.objects.create(
            name="polymers: property-based: thermosets", parent=polymers
        )
        polymers_thermoplastics = Material.objects.create(
            name="polymers: property-based: thermoplastics", parent=polymers
        )

        polymers_chemistry = Material.objects.create(name="polymers: chemistry-based")
        polymers_chemistry_polyolefins = Material.objects.create(
            name="polymers: chemistry-based: polyolefins", parent=polymers_chemistry
        )
        polymers_chemistry_polyesters = Material.objects.create(
            name="polymers: chemistry-based: polyesters", parent=polymers_chemistry
        )
        polymers_chemistry_polyamides = Material.objects.create(
            name="polymers: chemistry-based: polyamides", parent=polymers_chemistry
        )
        polymers_chemistry_polystyrenes = Material.objects.create(
            name="polymers: chemistry-based: polystyernes", parent=polymers_chemistry
        )
        polymers_chemistry_polycarbonates = Material.objects.create(
            name="polymers: chemistry-based: polycarbonates", parent=polymers_chemistry
        )
        polymers_chemistry_specialty = Material.objects.create(
            name="polymers: chemistry-based: specialty carbonates",
            parent=polymers_chemistry,
        )

        small_organic_compounds = Material.objects.create(
            name="small organic compounds"
        )


def _create_product_class_list():
    from cerr_curate_app.components.productclass import api as productclass_api
    from cerr_curate_app.components.productclass.models import ProductClass

    productclass = productclass_api.get_all()
    if productclass.exists() is False:
        batteries = ProductClass.objects.create(name="batteries")
        electronics = ProductClass.objects.create(name="electronics")
        durableplastics = ProductClass.objects.create(name="durable plastics")
        packaging = ProductClass.objects.create(name="packaging")
        solarpanels = ProductClass.objects.create(name="solar panels")
        packaging_glass = ProductClass.objects.create(
            name="packaging: glass", parent=packaging
        )
        packaging_plastic = ProductClass.objects.create(
            name="packaging: plastic", parent=packaging
        )
        packaging_metals = ProductClass.objects.create(
            name="packaging: metals", parent=packaging
        )
        packaging_fiber = ProductClass.objects.create(
            name="packaging: fiber", parent=packaging
        )
        building_materials = ProductClass.objects.create(name="building materials")
        building_materials_wood = ProductClass.objects.create(
            name="building materials: wood", parent=building_materials
        )
        building_materials_glass = ProductClass.objects.create(
            name="building materials: glass", parent=building_materials
        )
        building_materials_concrete = ProductClass.objects.create(
            name="building materials: concrete", parent=building_materials
        )
        building_materials_steel = ProductClass.objects.create(
            name="building materials: steel", parent=building_materials
        )
        textiles = ProductClass.objects.create(name="textiles")
