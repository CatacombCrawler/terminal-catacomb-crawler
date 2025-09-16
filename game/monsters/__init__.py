"""
Monsters Package - Contains all monster-related functionality
"""

from .monster_database import MonsterDatabase
from .monsters import Monster, MonsterManager

__all__ = ['MonsterDatabase', 'Monster', 'MonsterManager']
