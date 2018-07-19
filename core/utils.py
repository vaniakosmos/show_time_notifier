import glob
import logging
import sys
from importlib import import_module
from os.path import join


def load_models(base_dir, logger=None):
    logger = logger or logging.getLogger(__name__)
    modules = glob.glob(join(base_dir, '**', "*.py"), recursive=True)
    prefix_size = len(base_dir) + 1
    postfix_size = len('.py')
    for module in modules:
        module = module[prefix_size:-postfix_size]
        module = '.'.join(module.split('/'))
        logger.log(5, 'try > %s', module)
        if not module.endswith('models') or module in sys.modules:
            continue
        logger.info('> import %s', module)
        import_module(module)
