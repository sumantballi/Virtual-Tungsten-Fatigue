# Virtual Tungsten Fatigue — Defect-Aware Digital Twin (Lite, no lab required)

A fully computational project mirroring the LiU PhD posting: **defect-driven fatigue & lifetime modelling** for tungsten-like EB-PBF parts. No lab and no commercial FEM required.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_simulation --material tungsten --n-specimens 200 --seed 42
```
Outputs in `outputs/`:
- `results.csv` — pores, stress factors, initial crack `a0`, predicted life `Nf`
- `kitagawa.png` — allowable Δσ vs √area
- `sn_scatter.png` — life scatter at fixed Δσ
- `pore_hist.png` — pore size histogram

## Method (Lite path)
- Synthetic pores (size, aspect ratio, surface/subsurface, depth)
- Stress concentration proxy (no-FE), Kitagawa–Takahashi limit
- Short-crack growth (Paris-like) from `a0` to `a_crit`
- Monte Carlo across pore populations

## Optional Pro path
Plug FE fields (FEniCSx/CalculiX) into the same life model via `fem_stub.py` later.

## Talking point for applications
“Built a no-lab, no-commercial-FEA **digital twin** for tungsten-like fatigue: synthetic pore populations → Kitagawa/Murakami logic → short-crack growth and life predictions; produced design charts and what‑if studies (surface finishing, pore shape, clustering).”
