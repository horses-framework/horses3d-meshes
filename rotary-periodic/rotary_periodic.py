"""
Generate the RotaryPeriodic mesh (120 degree sector around the x axis) with the gmsh Python API.

The geometry and the structured meshing are defined in rotary_periodic.geo. The
boundary physical groups are rebuilt here from the position of each surface, so
they do not depend on the entity numbering of a particular gmsh version.

Usage (from the MESH directory):
    python3 rotary_periodic.py [-o rotary_periodic.msh]
"""
import argparse
import math
import os

import gmsh

here = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-o", "--output", default=os.path.join(here, "rotary_periodic.msh"),
                    help="output mesh file (default: rotary_periodic.msh next to this script)")
args = parser.parse_args()

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.open(os.path.join(here, "rotary_periodic.geo"))

#
# Boundary physical groups from the centre of each boundary surface:
# x (axial position), r (distance to the x axis) and theta (angle around the x axis)
#
def centre(tag):
    (u0, v0), (u1, v1) = gmsh.model.getParametrizationBounds(2, tag)
    x, y, z = gmsh.model.getValue(2, tag, [0.5 * (u0 + u1), 0.5 * (v0 + v1)])
    return x, math.hypot(y, z), math.degrees(math.atan2(z, y))

surfaces = {tag: centre(tag) for (_, tag) in gmsh.model.getBoundary(gmsh.model.getEntities(3), oriented=False)}
xs  = [c[0] for c in surfaces.values()]
rs  = [c[1] for c in surfaces.values()]
ths = [c[2] for c in surfaces.values()]
tol = 1.0e-6

def on(values, index, target):
    return [tag for tag, c in surfaces.items() if abs(c[index] - target) < tol * max(1.0, abs(target))]

boundaries = {
    "inflow":  on(xs,  0, min(xs)),
    "outflow": on(xs,  0, max(xs)),
    "bottom":  on(rs,  1, min(rs)),
    "top":     on(rs,  1, max(rs)),
    "sidea":   on(ths, 2, min(ths)),
    "sideb":   on(ths, 2, max(ths)),
}

#
# The physical tags are given explicitly: after removePhysicalGroups() gmsh keeps
# counting from the removed tags, and the $Entities section would then reference
# tags that do not match the ones in $PhysicalNames. The names of the groups of the
# .geo file are removed too: otherwise they stay attached to their old tags.
#
for dim, physTag in gmsh.model.getPhysicalGroups():
    gmsh.model.removePhysicalName(gmsh.model.getPhysicalName(dim, physTag))
gmsh.model.removePhysicalGroups()
for physTag, (name, tags) in enumerate(boundaries.items(), start=1):
    if len(tags) != 1:
        raise RuntimeError(f"Expected one surface for boundary '{name}', found {tags}")
    gmsh.model.addPhysicalGroup(2, tags, tag=physTag, name=name)
gmsh.model.addPhysicalGroup(3, [tag for (_, tag) in gmsh.model.getEntities(3)],
                            tag=len(boundaries) + 1, name="fluid")

gmsh.model.mesh.generate(3)
gmsh.option.setNumber("Mesh.MshFileVersion", 4.1)
gmsh.write(args.output)
gmsh.finalize()
