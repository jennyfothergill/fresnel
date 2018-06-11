// Copyright (c) 2016-2018 The Regents of the University of Michigan
// This file is part of the Fresnel project, released under the BSD 3-Clause License.

#include <stdexcept>
#include <pybind11/stl.h>

#include "GeometrySphere.h"
#include "common/IntersectSphere.h"

namespace fresnel { namespace cpu {

/*! \param scene Scene to attach the Geometry to
    \param N number of spheres to manage

    Initialize the sphere geometry.
*/
GeometrySphere::GeometrySphere(std::shared_ptr<Scene> scene, unsigned int N)
    : Geometry(scene)
    {
    // create the geometry
    m_geom_id = rtcNewUserGeometry(m_scene->getRTCScene(), N);
    m_device->checkError();

    // set default material
    setMaterial(Material(RGB<float>(1,0,1)));
    setOutlineMaterial(Material(RGB<float>(0,0,0), 1.0f));

    // initialize the buffers
    m_position = std::shared_ptr< Array< vec3<float> > >(new Array< vec3<float> >(N));
    m_radius = std::shared_ptr< Array< float > >(new Array< float >(N));
    m_color = std::shared_ptr< Array< RGB<float> > >(new Array< RGB<float> >(N));

    // register functions for embree
    rtcSetUserData(m_scene->getRTCScene(), m_geom_id, this);
    m_device->checkError();
    rtcSetBoundsFunction(m_scene->getRTCScene(), m_geom_id, &GeometrySphere::bounds);
    m_device->checkError();
    rtcSetIntersectFunction(m_scene->getRTCScene(), m_geom_id, &GeometrySphere::intersect);
    m_device->checkError();

    m_valid = true;
    }

GeometrySphere::~GeometrySphere()
    {
    }

/*! Compute the bounding box of a given primitive

    \param ptr Pointer to a GeometrySphere instance
    \param item Index of the primitive to compute the bounding box of
    \param bounds_o Output bounding box
*/
void GeometrySphere::bounds(void *ptr, size_t item, RTCBounds& bounds_o)
    {
    GeometrySphere *geom = (GeometrySphere*)ptr;
    vec3<float> p = geom->m_position->get(item);
    float radius = geom->m_radius->get(item);
    bounds_o.lower_x = p.x - radius;
    bounds_o.lower_y = p.y - radius;
    bounds_o.lower_z = p.z - radius;

    bounds_o.upper_x = p.x + radius;
    bounds_o.upper_y = p.y + radius;
    bounds_o.upper_z = p.z + radius;
    }

/*! Compute the intersection of a ray with the given primitive

    \param ptr Pointer to a GeometrySphere instance
    \param ray The ray to intersect
    \param item Index of the primitive to compute the bounding box of
*/
void GeometrySphere::intersect(void *ptr, RTCRay& ray, size_t item)
   {
    GeometrySphere *geom = (GeometrySphere*)ptr;
    const vec3<float> position = geom->m_position->get(item);
    const float radius = geom->m_radius->get(item);

    float t=0, d=0;
    vec3<float> N;
    bool hit = intersect_ray_sphere(t, d, N, ray.org, ray.dir, position, radius);

    if (hit && (ray.tnear < t) && (t < ray.tfar))
        {
        ray.u = 0.0f;
        ray.v = 0.0f;
        ray.tfar = t;
        ray.geomID = geom->m_geom_id;
        ray.primID = (unsigned int) item;
        ray.Ng = N;
        ray.shading_color = geom->m_color->get(item);
        ray.d = d;
        }
    }

/*! \param m Python module to export in
 */
void export_GeometrySphere(pybind11::module& m)
    {
    pybind11::class_<GeometrySphere, std::shared_ptr<GeometrySphere> >(m, "GeometrySphere", pybind11::base<Geometry>())
        .def(pybind11::init<std::shared_ptr<Scene>, unsigned int>())
        .def("getPositionBuffer", &GeometrySphere::getPositionBuffer)
        .def("getRadiusBuffer", &GeometrySphere::getRadiusBuffer)
        .def("getColorBuffer", &GeometrySphere::getColorBuffer)
        ;
    }

} } // end namespace fresnel::cpu
