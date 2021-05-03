import sys
import os
import shutil
import Genomics
import csv
import ast

sys.path.append("C:/Program Files/Side Effects Software/Houdini 18.5.499/houdini/python2.7libs")

import hou
#pcommand = "set PATH=C:\\Program Files\\Side Effects Software\\Houdini 18.5.499\\bin;C:\\Program Files\\Side Effects Software\\Houdini 18.5.499\\python27;$PATH$"
#os.system("%s" % pcommand)

curdir = os.getcwd()
subfolder = ""
results = curdir +"/results/" + subfolder

origCodeBottom = """;
    
    float stepSize = fit(expression, -20, 20, -.42, .42);
    
    if (@restlength > minLength && @restlength < maxLength){
        restlength = stepSize + @restlength;
    }
    else {
    restlength += (@restlengthorig - @restlength)/4;
    }
}"""

origCodeTop = """vector target = set(`chs("../../../../controller/Targetx")`,`chs("../../../../controller/Targety")`,`chs("../../../../controller/Targetz")`);

restlength = @restlength;

if (@stiffness==`chs("../../../../controller/tensionCable_stiffness")`){
    float p1 = primpoints(0,@primnum)[0];
    float p2 = primpoints(0,@primnum)[1];
    float p1C[] = point(0, "P", p1);
    float p2C[] = point(0, "P", p2);
    vector p1pos = set(p1C[0],p1C[1],p1C[2]);
    vector p2pos = set(p2C[0],p2C[1],p2C[2]);
    float pOrient = p1pos.y > p2pos.y;
    
    float p1Hits = point(0, "hits", p1);
    float p2Hits = point(0, "hits", p2);
    
    vector primCenter = (p1pos +p2pos)/2;
    
    //new variables section start
    
    float p1LocalX = point(0, "localX", p1);
    float p2LocalX = point(0, "localX", p2);
    
    float p1LocalY = point(0, "localY", p1);
    float p2LocalY = point(0, "localY", p2);
    
    float p1LocalZ = point(0, "localZ", p1);
    float p2LocalZ = point(0, "localZ", p2);
    
    float objX = detail(geoself(), "objX");
    float objY = detail(geoself(), "objY");
    float objZ = detail(geoself(), "objZ");
    
    float vObjX = detail(geoself(), "vObjX");
    float vObjY = detail(geoself(), "vObjY");
    float vObjZ = detail(geoself(), "vObjZ");
    
    float p1VX = point(0, "vX", p1);
    float p2VX = point(0, "vX", p2);
    
    float p1VY = point(0, "vY", p1);
    float p2VY = point(0, "vY", p2);
    
    float p1VZ = point(0, "vZ", p1);
    float p2VZ = point(0, "vZ", p2);
    
    float p1Upside = point(0, "upside", p1);
    float p2Upside = point(0, "upside", p2);
    
    float p1Down = point(0, "down", p1);
    float p2Down = point(0, "down", p2);
    
    float p1UpsideDown = point(0, "upsidedown", p1);
    float p2UpsideDown = point(0, "upsidedown", p2);
    
    //new variables section end
    
    float error = distance(primCenter,target);
    
    float minLength = .44;
    float maxLength = 1.21;
    
    float expression ="""

def expressionize(expression):
    simReplace()
    newCode = origCodeTop + expression + origCodeBottom
    hou.hipFile.load(curdir + "\\TesterTesnegrities.hipnc")
    constraintNode = hou.node('/obj/platonic1/vellumsolver1/dopnet1/forces/vellumconstraintproperty1')
    constraintNode2 = hou.node('/obj/platonic1/vellumsolver2/dopnet1/forces/vellumconstraintproperty3')
    code = constraintNode.parm('localexpression')
    code2 = constraintNode2.parm('localexpression')
    code.set(newCode)
    code2.set(newCode)
    hou.hipFile.save()

def simReplace():
    oldtt = curdir + "/TesterTesnegrities.hipnc"
    os.remove(oldtt)
    tt = curdir + "/TesterTesnegrities2.hipnc"
    newdir = curdir + "/ttemp"
    shutil.copy(tt,newdir)
    os.rename(curdir + '/ttemp\\TesterTesnegrities2.hipnc',curdir + '/TesterTesnegrities.hipnc')

def generateIndividual(geneDatabase, generationNumber, id):
    with open(results + geneDatabase) as f:
        reader = csv.reader(f)
        i= 1
        for row in reader:
            if (i==generationNumber):
                generation = ', '.join(row)
            i += 1
        f.close
    generation = generation[:-2]
    generation = ast.literal_eval(generation)
    specimen = generation[id]
    expressionize(Genomics.genomeToString(specimen))
