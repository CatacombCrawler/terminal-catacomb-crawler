""" Base Module for each entity class """

class BaseClass:
    def _to_dict(self, obj):
        """
        Converts any object to a dictionary
        :param obj:
        :return: dictionary
        """
        if isinstance(obj, list):
            return [self._to_dict(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._to_dict(item) for item in obj)
        elif isinstance(obj, dict):
            return {k: self._to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, "__dict__"):
            return {k: self._to_dict(v) for k, v in obj.__dict__.items()}
        else:
            return obj