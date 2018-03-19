from compas.utilities import color_to_colordict

import compas_rhino

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['CellArtist']


class CellArtist(object):

    def clear_cells(self, keys=None):
        if not keys:
            name = '{}.cell.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = self.datastructure.cell_name(key)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

    def draw_cells(self, ckeys=None, color=None, join_cells=False):
        """Draw a selection of cells of the mesh.

        Parameters
        ----------
        ckeys : list
            A list of cell keys identifying which cells to draw.
            The default is ``None``, in which case all cells are drawn.
        color : str, tuple, dict
            The color specififcation for the cells.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all cells, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default cell
            color (``self.defaults['cell.color']``).
            The default is ``None``, in which case all cells are assigned the
            default vertex color.

        Notes
        -----
        The cells are named using the following template:
        ``"{}.cell.{}".format(self.datastructure.attributes['name'], key)``.
        This name is used afterwards to identify cells of the mesh in the Rhino model.

        Examples
        --------
        >>>

        """
        ckeys = ckeys or list(self.datastructure.cells())
        colordict = color_to_colordict(color,
                                       ckeys,
                                       default=self.defaults['color.cell'],
                                       colorformat='rgb',
                                       normalize=False)
        cells = []
        for ckey in ckeys:
            cells.append({
                'points': self.datastructure.cell_coordinates(ckey),
                'name'  : self.datastructure.cell_name(ckey),
                'color' : colordict[ckey],
            })

        guids = compas_rhino.xdraw_cells(cells, layer=self.layer, clear=False, redraw=False)
        if not join_cells:
            return guids
        guid = rs.JoinMeshes(guids, delete_input=True)
        rs.ObjectLayer(guid, self.layer)
        rs.ObjectName(guid, '{}.mesh'.format(self.datastructure.name))
        return guid

    def draw_celllabels(self, text=None, color=None):
        """Draw labels for selected cells of the mesh.

        Parameters
        ----------

        Notes
        -----

        Examples
        --------

        """
        if text is None:
            textdict = {key: str(key) for key in self.datastructure.cells()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.defaults['color.cell'],
                                       colorformat='rgb',
                                       normalize=False)

        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos'  : self.datastructure.cell_center(key),
                'name' : self.datastructure.cell_name(key),
                'color': colordict[key],
                'text' : textdict[key],
            })
        return compas_rhino.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
