def load_env(filename=".env"):
  env_vars = {}
  try:
    with open(filename, "r") as f:
      for line in f:
        line = line.strip()
        if line and not line.startswith("#"):  # Ignore empty lines and comments
          key, value = line.split("=", 1)
          env_vars[key] = value
  except OSError:
    print(f"Could not open {filename}")
  return env_vars