#!/usr/bin/env python3
#
# Copyright 2021 Graviti. Licensed under MIT License.
#

"""Label related classes."""

from .attributes import AttributeInfo, Items
from .basic import LabelType
from .catalog import Catalog, Subcatalogs
from .label import Label
from .label_box import Box2DSubcatalog, Box3DSubcatalog, LabeledBox2D, LabeledBox3D
from .label_classification import Classification, ClassificationSubcatalog
from .label_keypoints import Keypoints2DSubcatalog, LabeledKeypoints2D
from .label_polygon import LabeledPolygon, PolygonSubcatalog
from .label_polyline import (
    LabeledMultiPolyline2D,
    LabeledPolyline2D,
    MultiPolyline2DSubcatalog,
    Polyline2DSubcatalog,
)
from .label_sentence import LabeledSentence, SentenceSubcatalog, Word
from .supports import CategoryInfo, KeypointsInfo

__all__ = [
    "AttributeInfo",
    "Box2DSubcatalog",
    "Box3DSubcatalog",
    "Catalog",
    "CategoryInfo",
    "Classification",
    "ClassificationSubcatalog",
    "Items",
    "Keypoints2DSubcatalog",
    "KeypointsInfo",
    "Label",
    "LabelType",
    "LabeledBox2D",
    "LabeledBox3D",
    "LabeledKeypoints2D",
    "LabeledMultiPolyline2D",
    "LabeledPolygon",
    "LabeledPolyline2D",
    "LabeledSentence",
    "MultiPolyline2DSubcatalog",
    "PolygonSubcatalog",
    "Polyline2DSubcatalog",
    "SentenceSubcatalog",
    "Subcatalogs",
    "Word",
]
