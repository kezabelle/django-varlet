try:
    from adminlinks.views import ModelContext
except ImportError:
    class ModelContext(object): pass

try:
    from editregions.views import EditRegionResponseMixin
except ImportError:
    class EditRegionResponseMixin(object): pass
