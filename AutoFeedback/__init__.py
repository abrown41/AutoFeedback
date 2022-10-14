from . import _version
__version__ = _version.get_versions()['version']


from AutoFeedback.plotchecks import check_plot
from AutoFeedback.varchecks import check_vars
from AutoFeedback.funcchecks import check_func
