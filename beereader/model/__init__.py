from pylons import config
from melk.model import create_model_context
from melk.model import ObjectNotFoundError, DuplicateObjectError

model = create_model_context(config)
