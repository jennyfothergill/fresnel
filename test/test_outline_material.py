import fresnel
import numpy
from collections import namedtuple
import PIL
import conftest

def test_set_material(scene_hex_sphere, generate=False):
    geometry = scene_hex_sphere.geometry[0]
    geometry.outline_width = 0.3
    geometry.outline_material = fresnel.material.Material(solid=0.0, color=fresnel.color.linear([1,0,0]), primitive_color_mix=0.0)
    assert geometry.outline_material.solid == 0.0
    assert geometry.outline_material.color == tuple(fresnel.color.linear([1,0,0]))
    assert geometry.outline_material.primitive_color_mix == 0.0

    buf_proxy = fresnel.render(scene_hex_sphere, w=100, h=100)

    if generate:
        PIL.Image.fromarray(buf_proxy[:], mode='RGBA').save(open('output/test_outline_material.test_set_material.png', 'wb'), 'png');
    else:
        conftest.assert_image_approx_equal(buf_proxy[:], 'reference/test_outline_material.test_set_material.png')

def test_solid(scene_hex_sphere, generate=False):
    geometry = scene_hex_sphere.geometry[0]
    geometry.outline_width = 0.3
    geometry.outline_material.solid = 1.0
    assert geometry.outline_material.solid == 1.0

    buf_proxy = fresnel.render(scene_hex_sphere, w=100, h=100)

    if generate:
        PIL.Image.fromarray(buf_proxy[:], mode='RGBA').save(open('output/test_outline_material.test_solid.png', 'wb'), 'png');
    else:
        conftest.assert_image_approx_equal(buf_proxy[:], 'reference/test_outline_material.test_solid.png')

def test_color(scene_hex_sphere, generate=False):
    geometry = scene_hex_sphere.geometry[0]
    geometry.outline_width = 0.3
    geometry.outline_material.color = fresnel.color.linear([0,0,1])
    assert geometry.outline_material.color == tuple(fresnel.color.linear([0,0,1]))

    buf_proxy = fresnel.render(scene_hex_sphere, w=100, h=100)

    if generate:
        PIL.Image.fromarray(buf_proxy[:], mode='RGBA').save(open('output/test_outline_material.test_color.png', 'wb'), 'png');
    else:
        conftest.assert_image_approx_equal(buf_proxy[:], 'reference/test_outline_material.test_color.png')

def test_primitive_color_mix(scene_hex_sphere, generate=False):
    geometry = scene_hex_sphere.geometry[0]
    geometry.outline_width = 0.3
    geometry.outline_material = fresnel.material.Material(solid=1.0, color=fresnel.color.linear([1,0,0]), primitive_color_mix=1.0)

    geometry.color[0] = fresnel.color.linear([1,0,0])
    geometry.color[1] = fresnel.color.linear([0,1,0])
    geometry.color[2] = fresnel.color.linear([0,0,1])
    geometry.color[3] = fresnel.color.linear([1,0,1])
    geometry.color[4] = fresnel.color.linear([0,1,1])
    geometry.color[5] = fresnel.color.linear([0,0,0])

    buf_proxy = fresnel.render(scene_hex_sphere, w=100, h=100)

    if generate:
        PIL.Image.fromarray(buf_proxy[:], mode='RGBA').save(open('output/test_outline_material.test_primitive_color_mix.png', 'wb'), 'png');
    else:
        conftest.assert_image_approx_equal(buf_proxy[:], 'reference/test_outline_material.test_primitive_color_mix.png')

if __name__ == '__main__':
    struct = namedtuple("struct", "param")
    device = conftest.device(struct(('cpu', None)))

    scene_hex_sphere = conftest.scene_hex_sphere(device)
    test_set_material(scene_hex_sphere, generate=True)

    scene_hex_sphere = conftest.scene_hex_sphere(device)
    test_solid(scene_hex_sphere, generate=True)

    scene_hex_sphere = conftest.scene_hex_sphere(device)
    test_color(scene_hex_sphere, generate=True)

    scene_hex_sphere = conftest.scene_hex_sphere(device)
    test_primitive_color_mix(scene_hex_sphere, generate=True)
