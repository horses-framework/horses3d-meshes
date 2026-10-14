#!/usr/bin/env python3
"""Generate a structured Cartesian hexahedral mesh of a box with Gmsh.

The domain [x0, x1] x [y0, y1] x [z0, z1] is meshed with nx x ny x nz
uniform, linear hexahedra. The mesh is built by extrusion:

    1. a line from (x0, y0, z0) to (x1, y0, z0), split into nx segments,
    2. extruded along y into a quad surface with ny layers,
    3. extruded along z into a hex volume with nz layers.

Any number of elements can be used in each direction. With nz = 1 the mesh
is a single-element-thick slab, which is the usual way of running quasi-2D
cases in HORSES3D.

The mesh is written in Gmsh MSH 2.2 ASCII format with the following
physical groups (the names are the boundary names used in the HORSES3D
control file):

    Back    z = z0        Front   z = z1
    Bottom  y = y0        Top     y = y1
    Left    x = x0        Right   x = x1
    Volume  the whole hexahedral domain

Usage:
    python3 generate_cartesian_box_mesh.py NX NY NZ [options]

Examples:
    # 235 x 235 x 1 elements on the default [-3, 3] x [-3, 3] x [0, 1] box,
    # written to cartesian_box_235_235_1.msh
    python3 generate_cartesian_box_mesh.py 235 235 1

    # Custom extents and output file
    python3 generate_cartesian_box_mesh.py 32 16 1 --xlim 0 2 --ylim 0 1 -o mesh.msh

Requires the Gmsh Python API (``pip install gmsh``).
"""

import argparse
import sys

import gmsh


def positive_int(value):
    """argparse type: an integer strictly greater than zero."""
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError(f"must be a positive integer, got {value}")
    return number


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a structured Cartesian hexahedral Gmsh mesh of a box.",
    )
    parser.add_argument("nx", type=positive_int, help="number of elements in x")
    parser.add_argument("ny", type=positive_int, help="number of elements in y")
    parser.add_argument("nz", type=positive_int, help="number of elements in z")
    parser.add_argument("--xlim", type=float, nargs=2, default=(-3.0, 3.0),
                        metavar=("X0", "X1"), help="domain extent in x (default: -3 3)")
    parser.add_argument("--ylim", type=float, nargs=2, default=(-3.0, 3.0),
                        metavar=("Y0", "Y1"), help="domain extent in y (default: -3 3)")
    parser.add_argument("--zlim", type=float, nargs=2, default=(0.0, 1.0),
                        metavar=("Z0", "Z1"), help="domain extent in z (default: 0 1)")
    parser.add_argument("-o", "--output",
                        help="output .msh file (default: cartesian_box_NX_NY_NZ.msh)")
    parser.add_argument("--geo", action="store_true",
                        help="also write the unrolled geometry (.geo_unrolled)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print Gmsh log messages")
    args = parser.parse_args(argv)

    for name in ("xlim", "ylim", "zlim"):
        lo, hi = getattr(args, name)
        if not lo < hi:
            parser.error(f"--{name}: lower bound must be smaller than upper bound")

    if args.output is None:
        args.output = f"cartesian_box_{args.nx}_{args.ny}_{args.nz}.msh"
    return args


def build_mesh(nx, ny, nz, xlim, ylim, zlim):
    """Build the geometry, physical groups and 3D mesh in the current Gmsh model."""
    (x0, x1), (y0, y1), (z0, z1) = xlim, ylim, zlim
    geo = gmsh.model.geo

    # Bottom edge (y = y0, z = z0), split into nx segments. The characteristic
    # length passed to addPoint is irrelevant: the mesh is fully structured.
    p0 = geo.addPoint(x0, y0, z0)
    p1 = geo.addPoint(x1, y0, z0)
    edge = geo.addLine(p0, p1)
    geo.mesh.setTransfiniteCurve(edge, nx + 1)

    # Extrude the edge along y into a quad surface (z = z0).
    # Returns [(1, opposite edge), (2, surface), (1, side), (1, side)].
    out = geo.extrude([(1, edge)], 0.0, y1 - y0, 0.0,
                      numElements=[ny], recombine=True)
    back = out[1][1]

    # Extrude the surface along z into a hex volume. Returns
    # [(2, opposite face), (3, volume), (2, lateral faces...)], where the
    # lateral faces follow the boundary of the extruded surface: the original
    # edge (y = y0), then x = x1, y = y1 and x = x0.
    out = geo.extrude([(2, back)], 0.0, 0.0, z1 - z0,
                      numElements=[nz], recombine=True)
    front, volume = out[0][1], out[1][1]
    bottom, right, top, left = (tag for _, tag in out[2:6])

    geo.synchronize()

    # Only entities in physical groups are written to the .msh file.
    for name, tag in (("Front", front), ("Back", back),
                      ("Left", left), ("Right", right),
                      ("Top", top), ("Bottom", bottom)):
        gmsh.model.addPhysicalGroup(2, [tag], name=name)
    gmsh.model.addPhysicalGroup(3, [volume], name="Volume")

    gmsh.model.mesh.generate(3)


def main(argv=None):
    args = parse_args(argv)

    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 1 if args.verbose else 0)
        gmsh.model.add("cartesian-box")

        build_mesh(args.nx, args.ny, args.nz, args.xlim, args.ylim, args.zlim)

        gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
        gmsh.write(args.output)
        if args.geo:
            gmsh.write(args.output.rsplit(".", 1)[0] + ".geo_unrolled")

        num_hexes = sum(len(tags) for tags in gmsh.model.mesh.getElements(3)[1])
    finally:
        gmsh.finalize()

    print(f"Mesh with {num_hexes} hexahedra "
          f"({args.nx} x {args.ny} x {args.nz}) written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
