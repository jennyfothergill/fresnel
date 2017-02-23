import fresnel
import numpy
from collections import namedtuple
import PIL
import conftest

def test_render(scene_hex_sphere, generate=False):
    tracer = fresnel.tracer.Direct(device=scene_hex_sphere.device, w=100, h=100)
    buf = tracer.output[:]
    assert buf.shape == (100,100,4)

    buf_proxy = tracer.render(scene_hex_sphere)

    if generate:
        PIL.Image.fromarray(buf_proxy[:], mode='RGBA').save(open('output/test_tracer_direct.test_render.png', 'wb'), 'png');
    else:
        conftest.assert_image_approx_equal(buf_proxy[:], 'reference/test_tracer_direct.test_render.png')

def test_resize(scene_hex_sphere, generate=False):
    tracer = fresnel.tracer.Direct(device=scene_hex_sphere.device, w=100, h=100)
    buf = tracer.output[:]
    assert buf.shape == (100,100,4)

    tracer.resize(w=200, h=300)
    buf = tracer.output[:]
    assert buf.shape == (300,200,4)

if __name__ == '__main__':
    struct = namedtuple("struct", "param")
    device = conftest.device(struct(('cpu', None)))

    scene_hex_sphere = conftest.scene_hex_sphere(device)
    test_render(scene_hex_sphere, generate=True)
