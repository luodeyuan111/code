"""Drone_Interface package initializer.

Exports the main classes provided by this package for convenient import:
- `RGBDataExtractor` : 图像采集与保存工具
- `FrameBuffer` : 简单的两帧缓存用于视觉处理
"""

from .rgb_data_extractor import RGBDataExtractor, FrameBuffer

__all__ = ["RGBDataExtractor", "FrameBuffer"]
