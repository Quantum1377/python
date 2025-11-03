# utilitários gerais (atualize conforme necessidade)

def safe_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default
