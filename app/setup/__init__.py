import os
from .log import init_logging
from .db import get_db_session, DBSessionDep
from .exceptions import exception_handlers
from ..config.consts import PATH_LOGO_SVG, SERVICE_NAME
from ..utils.text_conversion import save_logo_svg_from_text

__all__ = (
    "init_logging",
    "get_db_session",
    "DBSessionDep",
    "exception_handlers",
)

if os.path.isfile(PATH_LOGO_SVG):
    pass
else:
    save_logo_svg_from_text(SERVICE_NAME)