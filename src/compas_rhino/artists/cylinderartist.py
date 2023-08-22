from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import cylinder_to_rhino_brep
from .artist import RhinoArtist
from ._helpers import attributes


class CylinderArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, cylinder, **kwargs):
        super(CylinderArtist, self).__init__(geometry=cylinder, **kwargs)

    def draw(self, color=None):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cylinder.
            Default is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        guid = sc.doc.Objects.AddBrep(cylinder_to_rhino_brep(self.geometry), attr)
        return [guid]
