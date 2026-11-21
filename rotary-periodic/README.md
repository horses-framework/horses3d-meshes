# rotary-periodic

Structured hexahedral mesh of a 120 degree sector of an annulus around the `x`
axis, for periodic revolution (rotary periodic) boundary conditions. No mesh
files are stored in this directory; they are generated on the fly by the
Python script.

- Geometry and mesh origin: the rectangle `x in [0, 1]`, `y in [1, 11]` of the
  plane `z = 0`, revolved by `2 pi / 3` around the `x` axis through the origin.
  Defined in `rotary_periodic.geo` (Gmsh, built-in kernel) with structured
  layers: `Nx = 5` axial, `N = 16` radial and `Na = 30` azimuthal elements.
- Number of elements: `5 x 16 x 30 = 2400` hexahedra.
- Polynomial/geometrical order: 3 (`Mesh.ElementOrder = 3`).
- Mesh format: GMSH, MSH 4.1 (`.msh`).
- HORSES3D test case using the mesh: `NavierStokes/RotaryPeriodic`
  (`periodic enabled = .true.`, rotation axis `[1, 0, 0]`, `sidea` and `sideb`
  coupled as Periodic boundaries).
- Reference or source: none (simple analytical geometry).

## Boundary names

| Physical group | Location                  | Dimension |
| -------------- | ------------------------- | --------- |
| `inflow`       | `x = 0`                   | 2         |
| `outflow`      | `x = 1`                   | 2         |
| `bottom`       | `r = 1`                   | 2         |
| `top`          | `r = 11`                  | 2         |
| `sidea`        | `theta = 0` (plane `z = 0`) | 2       |
| `sideb`        | `theta = 120 deg`         | 2         |
| `fluid`        | domain                    | 3         |

`r` and `theta` are the radius and the angle around the `x` axis in the `y-z`
plane (`theta = atan2(z, y)`).

## Generating the mesh

Requirements: Python 3 and the Gmsh Python API (`pip install gmsh`).

```bash
python3 rotary_periodic.py [-o rotary_periodic.msh]
```

Use the Python script rather than meshing the `.geo` file directly. The
script rebuilds the boundary physical groups from the position of each
surface (axial position, radius and angle), so they do not depend on the
entity numbering of the Gmsh version.
