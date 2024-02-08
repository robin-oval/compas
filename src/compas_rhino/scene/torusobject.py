from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas_rhino.conversions import torus_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from .helpers import attributes


class TorusObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        A COMPAS torus.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, torus, **kwargs):
        super(TorusObject, self).__init__(geometry=torus, **kwargs)

    def draw(self):
        """Draw the torus associated with the scene object.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        attr = attributes(name=self.geometry.name, color=self.color, layer=self.layer)
        brep = torus_to_rhino_brep(self.geometry)
        brep.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddBrep(brep, attr)]
        return self.guids
