from pylons import config
from melkman.context import Context

context = Context.from_yaml(config['melkman.yamlconfig'])
