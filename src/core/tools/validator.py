
def validate_arguments(arguments: dict[str, object], parameters: dict[str, type]) -> None:
    # Reject unexpected arguments
    for name in arguments:
        if name not in parameters:
            raise ValueError(f"Unexpected argument: {name}")

    # Check required arguments and their types
    for name, expected_type in parameters.items():
        if name not in arguments:
            raise ValueError(f"Missing argument: {name}")

        value = arguments[name]

        if type(value) is not expected_type:
            raise TypeError(f"Argument '{name}' must be {expected_type.__name__}")
