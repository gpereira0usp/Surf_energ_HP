# CsPbBr3 · workflow organization

This directory contains the files used in the local `CsPbBr3` surface-energy and morphology workflow, reorganized for easier reading and reuse.

## Directory map

- `raw_data/`: original or minimally curated source material from the local workflow.
- `inputs/`: curated scientific inputs used by the analysis.
  - `inputs/structure/`: structural inputs such as `POSCAR`, `CONTCAR`, and symmetry labels.
  - `inputs/energies/`: slab-energy tables and convergence files, including `energies_sym.txt`.
  - `inputs/bands/`: band-summary files (`*PBAND_SUM*.dat`).
- `analysis/`: notebooks and analysis-specific data.
  - `analysis/notebooks/`: Jupyter notebooks.
  - `analysis/soc_bands/`: SOC band-analysis outputs.
  - `analysis/soc_pots/`: planar-average and SOC-related potential outputs.
- `processed/`: generated results and figures.
  - `processed/figures/`: plots, convergence curves, and exported visual outputs.
- `data_archive/`: archive area for historical or reference material.

## Suggested workflow

1. Inspect the relevant inputs in `inputs/`.
2. Reproduce the calculation workflow with the notebooks in `analysis/notebooks/`.
3. Compare the interpretation with the outputs stored in `processed/figures/`.
4. Use `analysis/soc_bands/` and `analysis/soc_pots/` for SOC-related studies.

## Notes

- The original filenames were preserved wherever possible to maintain traceability.
- The structure separates raw inputs from analysis and processed outcomes.
- This organization is intended to improve navigation, reproducibility, and readability.
