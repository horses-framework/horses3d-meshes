"""
Generate the DensityPulse_Sliding mesh (rotation axis along x) with the gmsh Python API.

The geometry and the structured (transfinite) meshing are defined in
circle_sliding_x.geo. The boundary physical groups are rebuilt here from the
bounding box of the domain, so they do not depend on the entity numbering of
a particular gmsh version.

Usage (from the MESH directory):
    python3 circle_sliding_x.py [-o circle_sliding_x.msh]
"""
import argparse
import os

import gmsh

here = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-o", "--output", default=os.path.join(here, "circle_sliding_x.msh"),
                    help="output mesh file (default: circle_sliding_x.msh next to this script)")
args = parser.parse_args()

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.open(os.path.join(here, "circle_sliding_x.geo"))

#
# Boundary physical groups: faces lying on the planes of the bounding box
#
xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(-1, -1)
tol = 1.0e-6

def surfaces_on_plane(x0, y0, z0, x1, y1, z1):
    entities = gmsh.model.getEntitiesInBoundingBox(x0 - tol, y0 - tol, z0 - tol,
                                                   x1 + tol, y1 + tol, z1 + tol, dim=2)
    return [tag for (_, tag) in entities]

# Original (x, y, z) planes mapped to (y, z, x): the rotation axis is x
boundaries = {
    "front":  surfaces_on_plane(xmin, ymin, zmin, xmin, ymax, zmax),
    "back":   surfaces_on_plane(xmax, ymin, zmin, xmax, ymax, zmax),
    "left":   surfaces_on_plane(xmin, ymin, zmin, xmax, ymin, zmax),
    "right":  surfaces_on_plane(xmin, ymax, zmin, xmax, ymax, zmax),
    "bottom": surfaces_on_plane(xmin, ymin, zmin, xmax, ymax, zmin),
    "top":    surfaces_on_plane(xmin, ymin, zmax, xmax, ymax, zmax),
}

#
# The physical tags are given explicitly: after removePhysicalGroups() gmsh keeps
# counting from the removed tags, and the $Entities section would then reference
# tags that do not match the ones in $PhysicalNames.
#
gmsh.model.removePhysicalGroups()
for physTag, (name, tags) in enumerate(boundaries.items(), start=1):
    if not tags:
        raise RuntimeError(f"No surfaces found for boundary '{name}'")
    gmsh.model.addPhysicalGroup(2, tags, tag=physTag, name=name)
gmsh.model.addPhysicalGroup(3, [tag for (_, tag) in gmsh.model.getEntities(3)],
                            tag=len(boundaries) + 1, name="fluid")

gmsh.model.mesh.generate(3)
gmsh.option.setNumber("Mesh.MshFileVersion", 4.1)
gmsh.write(args.output)
gmsh.finalize()
