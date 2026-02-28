import yaml


class ConfigError(Exception):
    pass


class Main:
    @classmethod
    def load_config(cls, yaml_path):
        try:
            with open(yaml_path) as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise ConfigError(f"Error reading YAML file {yaml_path}: {exc}") from exc
        except FileNotFoundError as exc:
            raise ConfigError(f"YAML file not found: {yaml_path}") from exc
