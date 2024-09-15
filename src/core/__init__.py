# core/__init__.py

"""
Core package for BustedURL system.

This package includes essential components such as the decentralized coordination hub
responsible for facilitating communication and coordination among the various agents.
"""

from .coordination_hub import CoordinationHub

# You can add any common configuration or initialization logic here.
# Example: Initialize global variables or setup configurations that are shared across the core modules.

__all__ = ['CoordinationHub']
