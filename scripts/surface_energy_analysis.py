from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_INPUTS = [
    REPO_ROOT / "inputs" / "energies" / "energies_sym.txt",
    REPO_ROOT / "data" / "CsPbBr3" / "energies_sym.txt",
    REPO_ROOT / "inputs" / "energies_sym.txt",
    Path("inputs/energies/energies_sym.txt"),
    Path("data/CsPbBr3/energies_sym.txt"),
]
E_BULK = -16.87567675
CORRESPONDENCES = {
    1: {0: (1, 1), 1: (1, 0)},
    11: {0: (11, 1), 1: (11, 0), 2: (11, 3), 3: (11, 2), 4: (11, 4)},
    111: {0: (111, 1), 1: (111, 0), 2: (111, 3), 3: (111, 2)},
}


def surface_energy(Eb: float, Eslab: float, N: int, A: float) -> float:
    """Compute the surface energy in J m^-2 for a slab configuration."""
    return 16.0217733 * (Eslab - N * Eb) / (4 * A)


def surf_energ_from_df_row(df_row, column_name: str):
    Eb = E_BULK
    Eslab = df_row[column_name]
    N = -1
    for digit in str(df_row["Slab_size"]):
        N += int(digit)
    A = df_row["Slab_area"]

    if df_row["Term"] in (0, 1):
        N_eff = 2 * N + 1
    elif (df_row["Facet"] == 11) and (df_row["Term"] not in (0, 1)):
        N_eff = 2 * N
    elif (df_row["Facet"] == 111) and (df_row["Term"] not in (0, 1)):
        N_eff = 2 * N - 1
    else:
        N_eff = N

    return N, surface_energy(Eb, Eslab, N_eff, A)


def df_surf_creating(df: pd.DataFrame, column_name: str = "Termination Energy") -> pd.DataFrame:
    data = {}
    for facet in CORRESPONDENCES:
        for term in CORRESPONDENCES[facet]:
            subset = df.loc[(df["Facet"] == facet) & (df["Term"] == term)]
            N_values = []
            energies = []
            for _, row in subset.iterrows():
                n, surf_energ = surf_energ_from_df_row(row, column_name)
                N_values.append(n)
                energies.append(surf_energ)
            data[f"{facet}-{term}"] = energies
    data["n"] = N_values
    return pd.DataFrame(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute surface energies from a slab-energy table.")
    default_input = next((candidate for candidate in LEGACY_INPUTS if candidate.exists()), LEGACY_INPUTS[0])
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input,
        help="Path to the slab-energy file. The script also accepts the legacy data/CsPbBr3 path.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    df = pd.read_csv(args.input, sep=" ", header=0)
    df["Cleavage Energy"] = None
    for facet, terms in CORRESPONDENCES.items():
        for term, pair in terms.items():
            left_facet, left_term = pair
            df.loc[(df["Facet"] == facet) & (df["Term"] == term), "Cleavage Energy"] = (
                df.loc[(df["Facet"] == facet) & (df["Term"] == term), "Froz_energ"].to_numpy()
                + df.loc[(df["Facet"] == left_facet) & (df["Term"] == left_term), "Froz_energ"].to_numpy()
            )
            df.loc[(df["Facet"] == facet) & (df["Term"] == term), "Relaxed Energy"] = (
                df.loc[(df["Facet"] == facet) & (df["Term"] == term), "Total_energ"].to_numpy()
                + df.loc[(df["Facet"] == left_facet) & (df["Term"] == left_term), "Total_energ"].to_numpy()
            )

    df["Termination Energy"] = (
        df["Cleavage Energy"].astype(float)
        + 2 * ((df["Total_energ"]) - df["Froz_energ"].astype(float))
    )

    result = df_surf_creating(df, column_name="Termination Energy")
    print(result.head())


if __name__ == "__main__":
    main()
