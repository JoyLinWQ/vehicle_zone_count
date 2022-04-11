"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List

from peekingduck.pipeline.nodes.dabble.zoningv1.zone import Zone
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        self.logger.info(f"\nmodel loaded with configs: {config}")
        try:
            self.zones = [
                self._create_zone(zone, config["resolution"]) \
                    for zone in self.zones # type: ignore
            ]
            # self.ids = config["input"]["my_ids"] # new - TODO: not working
            # print("custom key ids", self.ids)
            # self.logger.info("logger custom key ids", self.ids)
            # self.ids = ["car", "motorcycle", "truck", "bus"]
        except TypeError as error:
            self.logger.warning(error)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "__", "__".

        Returns:
            outputs (dict): Dictionary with keys "__".
        """

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs

        num_of_zones = len(self.zones)                  # eg. 2 zones
        # ids = inputs["ids"]
        # num_of_ids = len(ids)                      # eg. 4 class ids
        # zone_counts = [[0]*num_of_ids] * num_of_zones   # eg. 2D array 2 zones (row) x 4 class ids (cols)
        zone_counts = [0] * num_of_zones

        # for each x, y point, check if it is in any zone and add count in format below
        # zone_counts = [
        #   [zone_1|id_1, zone_1|id_2, zone_1|id_3, zone_1|id_4],
        #   [zone_2|id_1, zone_2|id_2, zone_2|id_3, zone_2|id_4]
        # ]
        for point in inputs["btm_midpoint"]:
            for i, zone in enumerate(self.zones):
                # for j, ids in enumerate(self.ids):
                if zone.point_within_zone(*point):
                    zone_counts[i] += 1
        print("--ZONECOUNT--")
        print("check zone count", zone_counts)
        print("zones", [zone.get_all_points_of_area() for zone in self.zones])
        print("my ids", inputs["my_ids"])
        print("inputs", inputs)
        return {
            "obj_attrs": inputs["obj_attrs"],
            "bboxes": inputs["bboxes"],
            "bbox_labels": inputs["bbox_labels"],
            "bbox_scores": inputs["bbox_scores"],
            "zones": [zone.get_all_points_of_area() for zone in self.zones],
            "zone_count": zone_counts,
            "my_ids": inputs["my_ids"]
        }

    # def ori_run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # """Counts all detected objects that falls within any specified zone,
        # and return the total object count in each zone.
        # """
        # num_of_zones = len(self.zones)
        # zone_counts = [0] * num_of_zones
# 
        # for each x, y point, check if it is in any zone and add count
        # for point in inputs["btm_midpoint"]:
            # for i, zone in enumerate(self.zones):
                # if zone.point_within_zone(*point):
                    # zone_counts[i] += 1
# 
        # return {
            # "zones": [zone.get_all_points_of_area() for zone in self.zones],
            # "zone_count": zone_counts,
        # }

    def _create_zone(self, zone: List[Any], resolution: List[int]) -> Any:
        """Creates the appropriate Zone given either the absolute pixel values
        or % of resolution as a fraction between [0, 1].
        """
        created_zone = None

        if all(all(0 <= i <= 1 for i in coords) for coords in zone):
            # coordinates are in fraction. Use resolution to get correct coords
            pixel_coords = [
                self._get_pixel_coords(coords, resolution) for coords in zone
            ]
            created_zone = Zone(pixel_coords)
        if all(all((isinstance(i, int) and i >= 0) for i in coords) for coords in zone):
            # when 1st-if fails and this statement passes, list is in pixel
            # value.
            created_zone = Zone(zone)

        # if neither, something is wrong
        if not created_zone:
            assert False, (
                "Zone %s needs to be all pixel-wise points or "
                "all fractions of the frame between 0 and 1. "
                "please check zone_count configs." % zone
            )

        return created_zone

    @staticmethod
    def _get_pixel_coords(coords: List[float], resolution: List[int]) -> List[float]:
        """Returns the pixel position of the zone points."""
        return [int(coords[0] * resolution[0]), int(coords[1] * resolution[1])]
