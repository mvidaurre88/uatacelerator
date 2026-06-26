from screens.screen_init import screen_init
from screens.screen_select_document import screen_select_document
from screens.screen_load_files import screen_load_files
from screens.screen_connect_ai import screen_connect_ai
from screens.screen_verify import screen_verify
from screens.screen_final import screen_final

def get_screens(BASE_DIR):
    return {
        "init": lambda: screen_init(BASE_DIR),
        "select": screen_select_document,
        "load": screen_load_files,
        "ai": screen_connect_ai,
        "verify": screen_verify,
        "final": screen_final,
    }