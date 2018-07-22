import importlib


empty = object()


class Settings:
    def __init__(self):
        mod = importlib.import_module('core.settings')

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)


class LazySettings:
    def __init__(self):
        self._wrapped = empty

    def _setup(self):
        self._wrapped = Settings()

    def __getattr__(self, name):
        """Return the value of a setting and cache it in self.__dict__."""
        if self._wrapped is empty:
            self._setup()
        val = getattr(self._wrapped, name)
        self.__dict__[name] = val
        return val


settings = LazySettings()
