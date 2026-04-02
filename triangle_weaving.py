import ghpythonlib.components as gh
import random

# -----------------------------------------------------------
# INPUTS (from Grasshopper)
# -----------------------------------------------------------
"""
pts    → Triangle vertices 
count  → Number of generated woven patterns
r_seed → Random seed for reproducibility
Ampli  → Deformation strength
dir    → Direction vector for deformation
"""

# Set random seed for reproducibility
random.seed(r_seed)


# -----------------------------------------------------------
# 1. CREATE TRIANGLE EDGES
# -----------------------------------------------------------
def create_ln(pts):
    """
    Create the three edges of a triangle from input vertices.

    Parameters:
        pts (list): List of 3 points defining a triangle

    Returns:
        tuple: Three lines representing triangle edges
    """
    ln1 = gh.Line(pts[0], pts[1])
    ln2 = gh.Line(pts[0], pts[2])
    ln3 = gh.Line(pts[1], pts[2])
    return ln1, ln2, ln3


# Generate triangle edges
lns = create_ln(pts)


# -----------------------------------------------------------
# 2. GENERATE WOVEN CURVES INSIDE TRIANGLE
# -----------------------------------------------------------
def weave_pts(lns, count, Ampli, dir):
    """
    Generate a weaving pattern inside a triangle.

    Logic:
    - Randomly sample points along triangle edges
    - Connect points to form triangular subdivisions
    - Apply deformation to midpoints
    - Reconstruct curves using interpolation

    Parameters:
        lns (tuple): Triangle edges
        count (int): Number of generated patterns
        Ampli (float): Deformation strength
        dir (vector): Direction of deformation

    Returns:
        list: List of tuples (line1, line2, line3)
    """
    result = []

    for i in range(count):

        # ---------------------------------------------------
        # Evaluate random points along each edge
        # ---------------------------------------------------
        pt1 = gh.EvaluateCurve(lns[0], random.random())[0]
        pt2 = gh.EvaluateCurve(lns[1], random.random())[0]
        pt3 = gh.EvaluateCurve(lns[2], random.random())[0]

        # ---------------------------------------------------
        # Create base triangle lines
        # ---------------------------------------------------
        line1 = gh.Line(pt1, pt2)
        line2 = gh.Line(pt1, pt3)
        line3 = gh.Line(pt2, pt3)

        # ---------------------------------------------------
        # Deform midpoints of selected lines
        # ---------------------------------------------------
        m1 = gh.Move(
            gh.CurveMiddle(line2),
            gh.Amplitude(dir, Ampli)
        )[0]

        m2 = gh.Move(
            gh.CurveMiddle(line3),
            gh.Amplitude(dir, -Ampli)
        )[0]

        # ---------------------------------------------------
        # Rebuild curves using interpolation
        # ---------------------------------------------------
        line2 = gh.Interpolate((pt1, m1, pt3), 3, False, 1)[0]
        line3 = gh.Interpolate((pt2, m2, pt3), 3, False, 1)[0]

        # Store results
        result.append((line1, line2, line3))

    return result


# Generate weaving geometry
lines = weave_pts(lns, count, Ampli, dir)


# -----------------------------------------------------------
# 3. OUTPUT (to Grasshopper)
# -----------------------------------------------------------
cutter1 = [x[0] for x in lines]
cutter2 = [x[1] for x in lines]
cutter3 = [x[2] for x in lines]
