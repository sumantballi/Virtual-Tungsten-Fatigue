# Virtual Tungsten Fatigue — Defect-Aware Digital Twin (Lite, no lab required)

## Introduction
This mini-project is based on models for structural integrity and the lifetime of EB-PBF tungsten. It builds a digital twin: synthetic defect populations → Kitagawa/Murakami logic → short-crack Paris growth (MPa√m units) → Monte-Carlo life scatter. Outputs include a designer Kitagawa chart, S–N scatter with percentiles, and what-if studies (surface finishing, pore shape, clustering). 

## What to look for
Kitagawa designer chart: allowable Δσ vs. defect √area.

S–N (fixed Δσ): life scatter + median/5–95% markers.

What-ifs:

Surface finishing (remove top 100–300 μm) → life ↑, scatter ↓.

Elongated pores (low AR) → life ↓.

Clustering (size mixture) → more short-life outliers.

Sensitivity: ΔK_th, Paris (C, m), nominal Δσ.

## Scope
Defect → fatigue modelling with thresholded short-crack life and Monte-Carlo scatter.
No physical testing. FE-ready: you can later replace the SCF surrogate with FE hot-spots (Δσ) or ΔK/J fields.

## Method (Lite path)
- Synthetic pores (size, aspect ratio, surface/subsurface, depth)
- Stress concentration proxy, Kitagawa–Takahashi limit
- Short-crack growth (Paris-like) from `a0` to `a_crit`
- Monte Carlo across pore populations

## Results 
Designer chart (Kitagawa):


Baseline S–N with percentiles:


What-ifs (unit-corrected):
| Surface finishing *(remove top 100 µm)* | Pore shape *(round vs. elongated)* | Clustering *(isolated vs. size-mixture)* |
| --- | --- | --- |
| ![Finishing](outputs/effect_surface_finishing_corrected_100um.png) <br> *Removes near-surface pores → ↑ median life, ↓ scatter.* | ![Shape](outputs/effect_pore_shape_corrected.png) <br> *Elongated (low AR) pores raise Kt → ↓ life, wider scatter.* | ![Cluster](outputs/effect_clustering_corrected.png) <br> *Clusters increase chance of a critical defect → more short-life outliers.* |


## Optional Pro path
Plug FE fields (FEniCSx/CalculiX) into the same life model via `fem_stub.py` later.

## Talking point for applications
“Built a no-lab, no-commercial-FEA **digital twin** for tungsten-like fatigue: synthetic pore populations → Kitagawa/Murakami logic → short-crack growth and life predictions; produced design charts and what‑if studies (surface finishing, pore shape, clustering).”
