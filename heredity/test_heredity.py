from heredity import *
import numpy as np

def test_joint_probability():
    """Test joint probability calculation"""
    people = {
        'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
        'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
        'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
        }
    
    assert joint_probability(people, {"Harry"}, {"James"}, {"James"}) == 0.0026643247488

