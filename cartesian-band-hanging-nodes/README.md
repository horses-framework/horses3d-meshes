# cartesian-band-hanging-nodes

Cartesian hexahedral mesh of a square box with a refined horizontal band
across the middle. **The mesh is non-conforming: it has hanging nodes.**
Refinement levels meet at 2:1 (1-to-4 face) mortar interfaces, so it can be
used to test the h-nonconforming (mortar) treatment in HORSES3D.

- Geometry and mesh origin: box `[-3, 3] x [-3, 3] x [0, 1]`, built from a
  uniform Cartesian base mesh with octree-like refinement towards the band
  `|y| <= 1.5`. Each refinement level halves the element size in `x`, `y`
  and `z`:

  | Level | Region in `y`        | Elements (`x * y * z`) | Element size `dx x dy x dz` |
  | ----- | -------------------- | ---------------------- | --------------------------- |
  | 0     | `1.95 <= abs(y) <= 3`   | `41 x 14 x 1 = 574`      | `6/41 x 0.15 x 1`           |
  | 1     | `1.5 <= abs(y) <= 1.95` | `82 x 12 x 2 = 1968`     | `6/82 x 0.075 x 0.5`        |
  | 2     | `abs(y) <= 1.5` (band)  | `164 x 80 x 4 = 52480`   | `6/164 x 0.0375 x 0.25`     |

- Hanging nodes: the level changes at `y = +-1.95` and `y = +-1.5`, giving
  410 non-conforming faces where one coarse face is coupled to four fine
  faces (HOPR mortar type 1). These interfaces span the whole `x` and `z`
  extent of the domain.
- Number of elements: 55022 hexahedra.
- Polynomial/geometrical order: 1 (`Ngeo = 1`, straight-sided hexahedra).
- Mesh format: HDF5 / HOPR (written by HOPR 1.6.0), `BAND_mesh.h5`.
- HORSES3D test case using the mesh: `Solver/test/Euler/DensityPulse_hMortars`
  (`mesh file name = "MESH/BAND_mesh.h5"`).
- Reference or source: none (simple analytical geometry).

## Boundary names

| Boundary | Location | Pairing used in `DensityPulse_hMortars` |
| -------- | -------- | --------------------------------------- |
| `left`   | `x = -3` | periodic with `right`                   |
| `right`  | `x = 3`  | periodic with `left`                    |
| `bottom` | `y = -3` | periodic with `top`                     |
| `top`    | `y = 3`  | periodic with `bottom`                  |
| `back`   | `z = 0`  | periodic with `front`                   |
| `front`  | `z = 1`  | periodic with `back`                    |
