from drf_yasg.views import get_schema_view
from documentation.monkey_patches import apply_monkey_patches

def get_schema_view_apply_monkey_patches(*args, **kwargs):
    apply_monkey_patches()
    return get_schema_view(*args, **kwargs)