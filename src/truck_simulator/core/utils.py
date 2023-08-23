from core.types import Icon, Model

def icon_from_model(model: Model) -> Icon:
    """
    Get icon from model.

    Args:
        model (Model): Car model.

    Returns:
        Icon: Car icon.
    """
    return {"car": "🚗", "bus": "🚌", "truck": "🚚"}[model]