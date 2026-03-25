import ghpythonlib.components as gh
import random
random.seed(r_seed)

#input
#pts → Triangle vertices
#count → Number of generated patterns
#r_seed → Random seed
#Ampli → Deformation strength
#dir → direction vector

# Create triangle edges from input points
def create_ln(pts):
    ln1 = gh.Line(pts[0],pts[1])
    ln2 = gh.Line(pts[0],pts[2])
    ln3 = gh.Line(pts[1],pts[2])
    return ln1,ln2,ln3

lns = create_ln(pts)

#Generate woven curves inside triangle

def weave_pts(lns,count,Ampli,dir):
    result = []
    for i in range(count):
    #Evaluate Crvs
        pt1 = gh.EvaluateCurve(lns[0],random.random())[0]
        pt2 = gh.EvaluateCurve(lns[1],random.random())[0]
        pt3 = gh.EvaluateCurve(lns[2],random.random())[0]
    #create Crvs
        line1 = gh.Line(pt1, pt2)
        line2 = gh.Line(pt1, pt3)
        line3 = gh.Line(pt2, pt3)
    #move mid point of (line2,line3)
        m1 = gh.Move(gh.CurveMiddle(line2),gh.Amplitude(dir, Ampli))[0] 
        m2 = gh.Move(gh.CurveMiddle(line3),gh.Amplitude(dir, -Ampli))[0] 
    #updated crvs
        line2 = gh.Interpolate((pt1,m1,pt3),3,False,1)[0] 
        line3 = gh.Interpolate((pt2,m2,pt3),3,False,1)[0]
        result.append((line1,line2,line3))
    return result

lines = weave_pts(lns,count,Ampli,dir)

#output
cutter1 = [x[0] for x in lines]
cutter2 = [x[1] for x in lines]
cutter3 = [x[2] for x in lines]


