# isentropic-vortex

Structured Cartesian hexahedral mesh of a square box, one element thick, for
the translating isentropic vortex. No mesh files are stored in this
directory; they are generated on the fly by the Python script.

- Geometry and mesh origin: box `[-15, 15] x [-15, 15] x [-1, 1]`, centred at
  the origin. Defined in `isentropic_vortex_2d.geo` (Gmsh, built-in kernel) by
  extruding a point along `x`, a line along `y` and a surface along `z`, with
  `Nx = 24`, `Ny = 24` and `Nz = 1` layers (recombined).
- Number of elements: `24 x 24 x 1 = 576` hexahedra.
- Polynomial/geometrical order: 1 (linear, straight-sided hexahedra).
- Mesh format: GMSH, MSH 4.1 (`.msh`).
- HORSES3D test case using the mesh: `Euler/IsentropicVortex` (horses3d-gpu).
- Reference or source: none (simple analytical geometry).

## Boundary names

| Physical group | Location  | Dimension |
| -------------- | --------- | --------- |
| `left`         | `x = -15` | 2         |
| `right`        | `x = 15`  | 2         |
| `bottom`       | `y = -15` | 2         |
| `top`          | `y = 15`  | 2         |
| `back`         | `z = -1`  | 2         |
| `front`        | `z = 1`   | 2         |
| `fluid`        | domain    | 3         |

## Generating the mesh

Requirements: Python 3 and the Gmsh Python API (`pip install gmsh`).

```bash
python3 isentropic_vortex_2d.py [-o isentropic_vortex_2d.msh]
```

Use the Python script rather than meshing the `.geo` file directly. The
script rebuilds the boundary physical groups from the bounding box of the
domain, so they do not depend on the entity numbering of the Gmsh version.
