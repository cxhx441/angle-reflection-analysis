import math
from geometric_elements import Source, Receiver, Ray, Reflector

class Room:
    def __init__(self, length: int, height: int):
        self._length = length
        self._height = height

        self._sources = set()
        self._rays = list()
        self._reflectors = set()
        self._receivers = set()

    # adders
    def add_source(self, coords):
        self._sources.add(Source(coords))

    def add_receiver(self, coords):
        self._receivers.add(Receiver(coords))

    def add_reflector(self, start_coords, end_coords):
        self._reflectors.add(Reflector(start_coords, end_coords))

    # generate rays
    def re_generate_rays(self):
        self._rays.clear()
        for source in self._sources:
            for reflector in self._reflectors:
                # create rays from source to reflector
                self._rays.append(Ray(source.get_coords(), reflector.get_start_coords()))
                self._rays.append(Ray(source.get_coords(), reflector.get_center_coords()))
                self._rays.append(Ray(source.get_coords(), reflector.get_end_coords()))

                # create rays from reflector to room edge
                rays_thru_reflector = self._get_reflected_rays_helper(source, reflector)
                for ray in rays_thru_reflector:
                    self._rays.append(ray)

    def _get_reflected_rays_helper(self, source: Source, reflector: Reflector):
        """
        helper function for generated rays reflected of reflectors
        """
        ray_temp = Ray(reflector.get_start_coords(), reflector.get_end_coords())
        ray_temp.rotate(angle=-math.pi/2)
        ray_temp.move(source.get_coords())
        intersection = reflector.get_intersection_of_2_lines(ray_temp)
        ray_temp.set_end_coords(intersection)
        ray_temp.rotate(pivot=ray_temp.get_end_coords(), angle=math.pi)
        reflector_ray_through_start = ray_temp.copy()
        reflector_ray_through_center = ray_temp.copy()
        reflector_ray_through_end = ray_temp.copy()

        reflector_ray_through_start.set_end_coords(reflector.get_start_coords())
        reflector_ray_through_center.set_end_coords(reflector.get_center_coords())
        reflector_ray_through_end.set_end_coords(reflector.get_end_coords())

        reflector_ray_through_start.move(reflector.get_start_coords())
        reflector_ray_through_center.move(reflector.get_center_coords())
        reflector_ray_through_end.move(reflector.get_end_coords())

        reflector_ray_through_start.extend((self._length, self._height))
        reflector_ray_through_center.extend((self._length, self._height))
        reflector_ray_through_end.extend((self._length, self._height))

        return reflector_ray_through_start, reflector_ray_through_center, reflector_ray_through_end

    # getters 
    def get_length(self):
        return self._length

    def get_height(self):
        return self._height

    def get_sources(self):
        return self._sources

    def get_rays(self):
        self.re_generate_rays()
        return self._rays

    def get_reflectors(self):
        return self._reflectors

    def get_receivers(self):
        return self._receivers
    
