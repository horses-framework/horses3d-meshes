# cartesian-box

Structured Cartesian hexahedral mesh of a box with `NX x NY x NZ` uniform
elements, generated on the fly by `generate_cartesian_box_mesh.py`. Any
number of elements can be used in each direction; with `NZ = 1` the mesh
is a one-element-thick slab for quasi-2D cases. No mesh files are stored in
this directory; the CI generates them when it needs them.

- Geometry and mesh origin: box `[x0, x1] x [y0, y1] x [z0, z1]`, by default
  `[-3, 3] x [-3, 3] x [0, 1]`. Generated with the Gmsh Python API by
  extruding a line along `y` and then along `z` (transfinite, recombined).
  This gives a uniform, conforming hexahedral mesh.
- Number of elements: `NX x NY x NZ`, set on the command line (for example
  `235 x 235 x 1 = 55225` hexahedra).
- Polynomial/geometrical order: 1 (linear, straight-sided hexahedra).
- Mesh format: GMSH, MSH 2.2 ASCII (`.msh`).
- HORSES3D test case using the mesh: TODO
- Reference or source: none (simple analytical geometry).

## Boundary names

| Physical group | Location | Dimension |
| -------------- | -------- | --------- |
| `Left`         | `x = x0` | 2         |
| `Right`        | `x = x1` | 2         |
| `Bottom`       | `y = y0` | 2         |
| `Top`          | `y = y1` | 2         |
| `Back`         | `z = z0` | 2         |
| `Front`        | `z = z1` | 2         |
| `Volume`       | domain   | 3         |

## Generating the mesh

Requirements: Python 3 and the Gmsh Python API (`pip install gmsh`).

```bash
python3 generate_cartesian_box_mesh.py NX NY NZ [--xlim X0 X1] [--ylim Y0 Y1] \
        [--zlim Z0 Z1] [-o OUTPUT] [--geo] [-v]
```

| Option         | Description                                       | Default                   |
| -------------- | ------------------------------------------------- | ------------------------- |
| `NX NY NZ`     | number of elements in `x`, `y`, `z` (required)    | -                         |
| `--xlim`       | domain extent in `x`                              | `-3 3`                    |
| `--ylim`       | domain extent in `y`                              | `-3 3`                    |
| `--zlim`       | domain extent in `z`                              | `0 1`                     |
| `-o/--output`  | output mesh file                                  | `cartesian_box_NX_NY_NZ.msh` |
| `--geo`        | also write the `.geo_unrolled` geometry           | off                       |
| `-v/--verbose` | print Gmsh log messages                           | off                       |

Examples:

```bash
# 235 x 235 x 1 elements on [-3, 3] x [-3, 3] x [0, 1] -> cartesian_box_235_235_1.msh
python3 generate_cartesian_box_mesh.py 235 235 1

# 32 x 16 x 1 elements on [0, 2] x [0, 1] x [0, 1]
python3 generate_cartesian_box_mesh.py 32 16 1 --xlim 0 2 --ylim 0 1 -o mesh.msh
```

The script exits with a non-zero status if the arguments are invalid, so
CI jobs can call it directly before running the solver.
