from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from copy import deepcopy

from compas.utilities import geometric_key

from compas.datastructures.mesh.clean import mesh_delete_duplicate_vertices


__all__ = [
    'meshes_join',
]


def meshes_join(meshes, delete_duplicates=False, precision='3f'):
    """Join multiple meshes. These meshes are usually assumed
    to be mesh patches that nicely align along their boundaries.

    Parameters
    ----------
    meshes : list of Mesh
        A list of mesh objects.
    delete_duplicates: bool
        True, if resulting duplicate vertices should be deleted.
        False, otherwise.

    """
    count = 0
    mesh_all = deepcopy(meshes[0])
    mesh_all.clear()
    key_map = {}
    for mesh in meshes:
        faces = list(mesh.faces())
        vertices = list(mesh.faces())

        for key, attr in mesh.vertices(True):
            mesh_all.add_vertex(count, x=attr['x'], y=attr['y'], z=attr['z'], attr_dict=attr)
            key_map[key] = count
            count += 1

        for fkey,attr in mesh.faces(True):
            vertices = mesh.face_vertices(fkey)
            new_vertices = [key_map[key] for key in vertices]
            mesh_all.add_face(new_vertices)

    if delete_duplicates:
        mesh_deletes_duplicate_vertices(mesh_all, precision)

    return mesh_all


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
