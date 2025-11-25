
import numpy as np
import pandas as pd

def sample_pores(n_pores:int,
                 size_dist=("lognormal", {"mean": -11.0, "sigma": 0.5}),
                 aspect_dist=("beta", {"a":2.0, "b":5.0}),
                 surface_prob=0.4,
                 min_depth=2e-6,
                 seed=None):
    rng = np.random.default_rng(seed)
    if size_dist[0] == "lognormal":
        sa = rng.lognormal(mean=size_dist[1]["mean"], sigma=size_dist[1]["sigma"], size=n_pores)
    else:
        raise ValueError("Only lognormal implemented for size_dist")
    if aspect_dist[0] == "beta":
        ar = rng.beta(aspect_dist[1]["a"], aspect_dist[1]["b"], size=n_pores)
    else:
        raise ValueError("Only beta implemented for aspect_dist")
    is_surface = (rng.random(n_pores) < surface_prob).astype(int)
    depth = np.where(is_surface==1, rng.uniform(0.0, min_depth, size=n_pores),
                     rng.uniform(min_depth, 200e-6, size=n_pores))
    return pd.DataFrame({
        "sqrt_area": sa,
        "aspect_ratio": ar,
        "is_surface": is_surface,
        "depth": depth
    })

def effective_initial_crack_length(df, material_props):
    k_sub = 0.25
    k_surf = 0.35
    a0 = np.where(df["is_surface"]==1, k_surf*df["sqrt_area"], k_sub*df["sqrt_area"])
    a0 = np.maximum(a0, material_props.get("a0_min", 1e-6))
    return a0
