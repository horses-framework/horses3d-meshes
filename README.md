# HORSES3D Meshes

Mesh repository for [HORSES3D](https://github.com/horses-framework/horses3d).

This repository contains meshes used for verification, validation, tutorials,
benchmarks, and regression tests of HORSES3D.

## Mesh formats

HORSES3D supports curvilinear hexahedral meshes in formats including:

- HDF5 / HOPR
- GMSH
- SpecMesh / HOHQMesh

## Repository structure

Each directory corresponds to a HORSES3D test or validation case and contains
the meshes required to reproduce the case. The directory names should mirror
HORSES3D test-case names whenever possible.

Whenever possible, each case should include information about:

- Geometry and mesh origin
- Number of elements
- Polynomial/geometrical order
- Mesh format
- HORSES3D test case using the mesh
- Reference or source, when applicable

## Git LFS

Binary HDF5 meshes should be stored with Git LFS to keep repository history
manageable as the mesh collection grows.

## Initial layout

- `channel-flow/`
- `cylinder/`
- `lid-driven-cavity/`
- `naca0012/`
- `taylor-green-vortex/`

Each case directory includes a small `README.md` describing provenance and mesh
generation details.

## License

See `LICENSE`.
