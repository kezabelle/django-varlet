try:
    from adminlinks.views import ModelContext
except ImportError:
    class ModelContext(object): pass

try:
    from editregions.views import EditRegionResponseMixin
except ImportError:
    class EditRegionResponseMixin(object): pass

# try:
#     from menuhin.models import ModelMenuItemGroup
# except ImportError:
#     class ModelMenuItemGroup(object): pass

try:
    from parsley.mixins import ParsleyAdminMixin
except ImportError:
    class ParsleyAdminMixin(object): pass

try:
    from thadminjones.admin import SupportsQuickAdd
except ImportError:
    class SupportsQuickAdd(object): pass
