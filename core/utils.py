import glob
import logging
import os
from importlib import import_module


def load_modules(target, base_dir=None, logger=None):
    base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
    logger = logger or logging.getLogger(__name__)
    modules = glob.glob(os.path.join(base_dir, '**', "*.py"), recursive=True)
    prefix_size = len(base_dir) + 1
    postfix_size = len('.py')
    for module in modules:
        module = module[prefix_size:-postfix_size]
        module = '.'.join(module.split('/'))
        logger.log(5, 'try > %s', module)
        if not module.endswith(target):
            continue
        logger.info('> import %s', module)
        import_module(module)
