# circle-sliding

Structured O-grid hexahedral mesh of a square box with an octagonal core and
two concentric circles, intended for sliding-mesh cases (a rotating circular
region inside a fixed outer region). The same mesh is provided with the
rotation axis along `x`, `y` or `z`. No mesh files are stored in this
directory; they are generated on the fly by the Python scripts.

- Geometry and mesh origin: square `[-3, 3] x [-3, 3]` in the plane normal to
  the rotation axis, extruded one unit (`[0, 1]`) along the rotation axis.
  Defined in `circle_sliding_{x,y,z}.geo` (Gmsh, OpenCASCADE kernel) with
  transfinite, recombined surfaces extruded with one layer:

  | Region                     | Radius               | Elements (in-plane)       |
  | -------------------------- | -------------------- | ------------------------- |
  | Octagonal core             | `r <= 0.8`           | `4 x 10 x 10 = 400`       |
  | Octagon to first circle    | `0.8 <= r <= 1.8`    | `8 x 10 x 19 = 1520`      |
  | First to second circle     | `1.8 <= r <= 2.5`    | `8 x 10 x 19 = 1520`      |
  | Second circle to square    | `r >= 2.5`           | `8 x 10 x 10 = 800`       |

  The 19 radial elements of each annular layer are graded with progression
  `0.9`, so they get finer outwards, towards `r = 1.8` and `r = 2.5`.
  These parameters (`inner_radius`, `middle_radius`, `second_radius`,
  `quad_corner`, `NPointsRadial`, `RadialProgression`, `NPointsCircle`) are
  set at the top of the `.geo` files.
- Number of elements: 4240 hexahedra (8562 nodes), one element thick.
- Polynomial/geometrical order: 1 (linear, straight-sided hexahedra).
- Mesh format: GMSH, MSH 4.1 (`.msh`).
- HORSES3D test case using the mesh: `DensityPulse_Sliding` (rotation axis
  along `z`).
- Reference or source: none (simple analytical geometry).

## Rotation axis variants

The `x` and `y` variants are the `z` mesh rotated rigidly: only the point
coordinates and the extrusion direction change. Curves, surfaces, number of
elements, grading and entity tags are identical in all three. The rotation
is a cyclic permutation of the coordinates, so orientations are preserved.

| Files                   | Rotation axis | In-plane point `(u, v)` | Extrusion |
| ----------------------- | ------------- | ----------------------- | --------- |
| `circle_sliding_z.*`    | `z`           | `(u, v, 0)`             | `+z`      |
| `circle_sliding_x.*`    | `x`           | `(0, u, v)`             | `+x`      |
| `circle_sliding_y.*`    | `y`           | `(v, 0, u)`             | `+y`      |

## Boundary names

The boundary names rotate with the mesh: `front` and `back` are always the
faces normal to the rotation axis.

| Physical group | `z` axis | `x` axis | `y` axis | Dimension |
| -------------- | -------- | -------- | -------- | --------- |
| `front`        | `z = 0`  | `x = 0`  | `y = 0`  | 2         |
| `back`         | `z = 1`  | `x = 1`  | `y = 1`  | 2         |
| `left`         | `x = -3` | `y = -3` | `z = -3` | 2         |
| `right`        | `x = 3`  | `y = 3`  | `z = 3`  | 2         |
| `bottom`       | `y = -3` | `z = -3` | `x = -3` | 2         |
| `top`          | `y = 3`  | `z = 3`  | `x = 3`  | 2         |
| `fluid`        | domain   | domain   | domain   | 3         |

## Generating the mesh

Requirements: Python 3 and the Gmsh Python API (`pip install gmsh`).

```bash
python3 circle_sliding_z.py [-o circle_sliding_z.msh]
python3 circle_sliding_x.py [-o circle_sliding_x.msh]
python3 circle_sliding_y.py [-o circle_sliding_y.msh]
```

Use the Python scripts rather than meshing the `.geo` files directly. The
scripts rebuild the boundary physical groups from the bounding box of the
domain. The groups hard-coded at the end of the `.geo` files depend on the
entity numbering of the Gmsh version: with Gmsh 4.15.1 their `top` and
`bottom` groups are swapped.
