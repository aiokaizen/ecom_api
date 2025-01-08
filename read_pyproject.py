import toml

config = toml.load("pyproject.toml")

arconfig = config.get("tool", {}).get("ar", {})
print("arconfig:", type(arconfig), arconfig)
