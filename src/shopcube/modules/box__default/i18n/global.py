# global templates variables in here
from .helpers import get_current_lang
from .helpers import get_default_lang
from .helpers import langs

available_everywhere = {
    "get_i18n_langs": langs,
    "get_default_lang": get_default_lang,
    "get_current_lang": get_current_lang,
}
# global configs in here, defined by profile
# configs = {
#     "development": {
#         "CONFIG_VAR": "DEVVALUE"
#     },
#     "production": {
#         "CONFIG_VAR": "PRODVALUE"
#     },
#     "testing": {
#         "CONFIG_VAR": "TESTVALUE"
#     }
# }
