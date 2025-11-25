
import argparse, json, numpy as np, pandas as pd, matplotlib.pyplot as plt
from .generate_pores import sample_pores, effective_initial_crack_length
from .scf_and_models import scf_for_pore, kitagawa_allowable_stress, paris_life

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--material", type=str, default="tungsten")
    parser.add_argument("--n-specimens", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--stress_mean", type=float, default=0.0, help="Mean stress, Pa")
    parser.add_argument("--stress_alt", type=float, default=250e6, help="Alternating stress amplitude (Pa)")
    parser.add_argument("--outdir", type=str, default="outputs")
    args = parser.parse_args()

    with open("src/materials.json","r") as f:
        mats = json.load(f)
    mat = mats[args.material]

    pores = sample_pores(args.n_specimens, seed=args.seed)

    Kt = scf_for_pore(pores["sqrt_area"].values,
                      pores["aspect_ratio"].values,
                      pores["is_surface"].values)
    delta_sigma_nom = args.stress_alt*2.0  # range Δσ
    delta_sigma_eff = Kt * delta_sigma_nom

    sa_grid = np.logspace(np.log10(1e-7), np.log10(2e-4), 200)
    kitagawa = kitagawa_allowable_stress(sa_grid, mat["sigma_u"], mat["deltaK_th"])

    a0 = effective_initial_crack_length(pores, mat)
    a_crit = mat["a_crit"]

    Y = np.where(pores["is_surface"].values==1, 1.12, 1.0)
    delta_sigma_eff_adj = delta_sigma_eff * Y

    Nf = np.array([paris_life(a0_i, a_crit, ds_i, mat["E"], mat["deltaK_th"], mat["C"], mat["m"])
                   for a0_i, ds_i in zip(a0, delta_sigma_eff_adj)])

    df = pores.copy()
    df["Kt"] = Kt
    df["delta_sigma_eff"] = delta_sigma_eff_adj
    df["a0"] = a0
    df["Nf"] = Nf
    os.makedirs(args.outdir, exist_ok=True)
    df.to_csv(f"{args.outdir}/results.csv", index=False)

    # Plots
    plt.figure()
    plt.loglog(sa_grid, kitagawa)
    plt.xlabel("sqrt(area) [m]")
    plt.ylabel("Allowable stress range Δσ_allow [Pa]")
    plt.title("Kitagawa–Takahashi (tungsten-like)")
    plt.grid(True, which="both", ls=":")
    plt.savefig(f"{args.outdir}/kitagawa.png", dpi=200)
    plt.close()

    plt.figure()
    plt.loglog(np.full_like(Nf, delta_sigma_nom), Nf, "o", alpha=0.5)
    plt.xlabel("Δσ_nom [Pa]")
    plt.ylabel("N_f [cycles]")
    plt.title("S–N scatter at fixed nominal Δσ (scatter from pores)")
    plt.grid(True, which="both", ls=":")
    plt.savefig(f"{args.outdir}/sn_scatter.png", dpi=200)
    plt.close()

    plt.figure()
    plt.hist(df["sqrt_area"].values*1e6, bins=30)
    plt.xlabel("sqrt(area) [µm]")
    plt.ylabel("count")
    plt.title("Pore size (sqrt(area)) distribution")
    plt.savefig(f"{args.outdir}/pore_hist.png", dpi=200)
    plt.close()

    print(f"Saved results to {args.outdir}/")

if __name__ == "__main__":
    import os
    main()
