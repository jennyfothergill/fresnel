# Copyright (c) 2016-2017 The Regents of the University of Michigan
# This file is part of the Fresnel project, released under the BSD 3-Clause License.

R"""
Materials describe the way light interacts with surfaces.
"""

from fresnel import _common

class Material(object):
    R"""Define material properties.

    Args:

        solid (float): Set to 1 to pass through a solid color, regardless of the light and view angle.
        color (tuple): The linear RGB color of the material as a 3-tuple, list or other iterable.
        primitive_color_mix (float): Set to 1 to use the color provided in the Geometry, 0 to use the color
          specified in the material, or in the range (0,1) to mix the two colors.

    Colors are in the linearized sRGB color space. Use :py:func:`fresnel.color.linear` to convert standard sRGB colors
    into this space.
    """

    def __init__(self, solid=0, color=(0,0,0), primitive_color_mix=0):
        self._material = _common.Material();

        self.solid = solid;
        self.color = color;
        self.primitive_color_mix = primitive_color_mix;

    def __repr__(self):
        return "Material(solid={0}, color={1}, primitive_color_mix={2})".format(self.solid, self.color, self.primitive_color_mix);

    @property
    def solid(self):
        return self._material.solid;

    @solid.setter
    def solid(self, value):
        self._material.solid = float(value);

    @property
    def primitive_color_mix(self):
        return self._material.primitive_color_mix;

    @primitive_color_mix.setter
    def primitive_color_mix(self, value):
        self._material.primitive_color_mix = float(value);

    @property
    def color(self):
        return (self._material.color.r, self._material.color.g, self._material.color.b);

    @color.setter
    def color(self, value):
        if len(value) != 3:
            raise ValueError("colors must have length 3");
        self._material.color = _common.RGBf(*value);

    def _get_cpp_material(self):
        return self._material;

class _material_proxy(object):
    """ Proxy :py:class`Material` attached to a :py:class`fresnel.geometry.Geometry`
    """
    def __init__(self, geometry):
        self._geometry = geometry._geometry;

    @property
    def solid(self):
        m = self._geometry.getMaterial();
        return m.solid;

    @solid.setter
    def solid(self, value):
        m = self._geometry.getMaterial();
        m.solid = float(value);
        self._geometry.setMaterial(m);

    @property
    def primitive_color_mix(self):
        m = self._geometry.getMaterial();
        return m.primitive_color_mix;

    @primitive_color_mix.setter
    def primitive_color_mix(self, value):
        m = self._geometry.getMaterial();
        m.primitive_color_mix = float(value);
        self._geometry.setMaterial(m);

    @property
    def color(self):
        m = self._geometry.getMaterial();
        return (m.color.r, m.color.g, m.color.b);

    @color.setter
    def color(self, value):
        if len(value) != 3:
            raise ValueError("colors must have length 3");

        m = self._geometry.getMaterial();
        m.color = _common.RGBf(*value);
        self._geometry.setMaterial(m);

    def _get_cpp_material(self):
        return self._geometry.getMaterial();

class _outline_material_proxy(object):
    """ Proxy outline :py:class`Material` attached to a :py:class`fresnel.geometry.Geometry`
    """
    def __init__(self, geometry):
        self._geometry = geometry._geometry;

    @property
    def solid(self):
        m = self._geometry.getOutlineMaterial();
        return m.solid;

    @solid.setter
    def solid(self, value):
        m = self._geometry.getOutlineMaterial();
        m.solid = float(value);
        self._geometry.setOutlineMaterial(m);

    @property
    def primitive_color_mix(self):
        m = self._geometry.getOutlineMaterial();
        return m.primitive_color_mix;

    @primitive_color_mix.setter
    def primitive_color_mix(self, value):
        m = self._geometry.getOutlineMaterial();
        m.primitive_color_mix = float(value);
        self._geometry.setOutlineMaterial(m);

    @property
    def color(self):
        m = self._geometry.getOutlineMaterial();
        return (m.color.r, m.color.g, m.color.b);

    @color.setter
    def color(self, value):
        if len(value) != 3:
            raise ValueError("colors must have length 3");

        m = self._geometry.getOutlineMaterial();
        m.color = _common.RGBf(*value);
        self._geometry.setOutlineMaterial(m);

    def _get_cpp_material(self):
        return self._geometry.getOutlineMaterial();
