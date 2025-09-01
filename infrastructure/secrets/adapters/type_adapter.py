from typing import Any, Dict, List, Type, Union


class TypeConverter:
    """Handles type conversion for environment variables."""

    @staticmethod
    def convert_value(value: str, target_type: Type, var_name: str) -> Any:
        """Convert string value to target type with comprehensive error handling."""

        if target_type == str:
            return value

        try:
            if target_type == bool:
                return TypeConverter._convert_bool(value)

    @staticmethod
    def _convert_bool(value: str) -> bool:
        """Convert string to boolean."""

        value_lower = value.lower().strip()
        if value_lower in ("true", "1", "yes", "on", "enabled"):
            return True
        elif value_lower in ("false", "0", "no", "off", "disabled"):
            return False
        else:
            # TODO:
            raise ...

    @staticmethod
    def _convert_list(value: str) -> List[str]:
        """Convert comma-separated string to list."""

        if not value.strip():
            return []
        return [item.strip() for item in value.split(',') if item.strip()]


    @staticmethod
    def _convert_dict(value: str) -> Dict[str, str]:
        """Conver key=value, key2=value2 string to dictionary."""

        if not value.strip():
            return {}
        
        result = {}
        pairs = value.split(",")
        for pair in pairs:
            if "=" not in pair:
                # TODO:
                raise ...
            key, val = pair.split("=", 1)
            result[key.strip()] = val.strip()
        return result

    @staticmethod
    def _convert_generic(value: str, target_type: Type, var_name: str) -> Any:
        """Handle generic types like Optional, Union, etc."""

        origin = getattr(target_type, "__origin__", ())

        if origin is Union:
            # Handle optional types (Union[T, None])
            args = getattr(target_type, "__args__", ())
            if len(args) == 2 and type(None) in args:
                non_none_type = args[0] if args[1] is type(None) else args[1]
                return TypeConverter.convert_value(value, non_none_type, var_name)

        # TODO:
        raise ...
