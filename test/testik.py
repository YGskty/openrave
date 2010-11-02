# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# random code that helps with debugging/testing the python interfaces and examples
# this is not meant to be run by normal users
from __future__ import with_statement # for python 2.5
__copyright__ = 'Copyright (C) 2009-2010'
__license__ = 'Apache License, Version 2.0'

# random code that helps with debugging/testing the python interfaces and examples
# this is not meant to be run by normal users
from openravepy import *
import openravepy.examples
from openravepy.interfaces import *
from numpy import *
import numpy,time

def test_ikgeneration():
    import inversekinematics
    env = Environment()
    env.SetDebugLevel(DebugLevel.Debug)
    #robot = env.ReadRobotXMLFile('robots/barrettsegway.robot.xml')
    robot = env.ReadRobotXMLFile('robots/barrettwam4.robot.xml')
    robot.SetActiveManipulator('arm')
    env.AddRobot(robot)
    self = inversekinematics.InverseKinematicsModel(robot=robot,iktype=IkParameterization.Type.Translation3D)

    freejoints=None
    usedummyjoints=False
    accuracy = None
    precision = None
    iktype=inversekinematics.InverseKinematicsModel.Type_Direction3D
    self.generate(freejoints=freejoints,usedummyjoints=usedummyjoints,iktype=iktype)

    baselink=self.manip.GetBase().GetIndex()
    eelink = self.manip.GetEndEffector().GetIndex()
    solvejoints=solvejoints
    freeparams=freejoints
    usedummyjoints=usedummyjoints
    solvefn=solvefn

def test_ik():
    import inversekinematics
    env = Environment()
    env.SetDebugLevel(DebugLevel.Debug)
    robot = env.ReadRobotXMLFile('/home/rdiankov/ros/honda/binpicking/robots/tx90.robot.xml')
    env.AddRobot(robot)
    manip=robot.GetActiveManipulator()
    #manip=robot.SetActiveManipulator('leftarm_torso')
    self = inversekinematics.InverseKinematicsModel(robot=robot,iktype=IkParameterization.Type.Transform6D)
    self.load()
    self.perftiming(10)
    robot.SetJointValues([-2.62361, 1.5708, -0.17691, -3.2652, 0, -3.33643],manip.GetArmJoints())
    T=manip.GetEndEffectorTransform()
    print robot.CheckSelfCollision()
    #[j.SetJointLimits([-pi],[pi]) for j in robot.GetJoints()]
    robot.SetJointValues(zeros(robot.GetDOF()))
    values=manip.FindIKSolution(T,False)
    Tlocal = dot(dot(linalg.inv(manip.GetBase().GetTransform()),T),linalg.inv(manip.GetGraspTransform()))
    print ' '.join(str(f) for f in Tlocal[0:3,0:4].flatten())
    robot.SetJointValues (values,manip.GetArmJoints())
    print manip.GetEndEffectorTransform()
    
    sols=manip.FindIKSolutions(T,False)
    for i,sol in enumerate(sols):
        robot.SetJointValues(sol)
        Tnew = manip.GetEndEffectorTransform()
        if sum((Tnew-T)**2) > 0.0001:
            print i
            break
        
def debug_ik():
    env = Environment()
    env.Reset()
    robot = env.ReadRobotXMLFile('robots/man1.robot.xml')
    env.AddRobot(robot)
    manip=robot.SetActiveManipulator('rightarm')
    prob=interfaces.BaseManipulation(robot)
    prob.DebugIK(10)

def test_ik():
    from sympy import *
    import __builtin__
    from openravepy.ikfast import SolverStoreSolution, SolverSolution, combinations, SolverSequence, fmod
    ikmodel=self
    self = solver
    alljoints = self.getJointsInChain(baselink, eelink)
    chain = []
    for joint in alljoints:
        issolvejoint = any([i == joint.jointindex for i in solvejoints])
        if usedummyjoints and not issolvejoint and not any([i == joint.jointindex for i in freejointinds]):
            joint.isdummy = True
        joint.isfreejoint = not issolvejoint and not joint.isdummy
        chain.append(joint)
    Tee = eye(4)
    for i in range(0,3):
        for j in range(0,3):
            Tee[i,j] = Symbol("r%d%d"%(i,j))
    Tee[0,3] = Symbol("px")
    Tee[1,3] = Symbol("py")
    Tee[2,3] = Symbol("pz")

    chaintree = solvefn(self,chain,Tee)
    code=ikfast_generator_cpp.CodeGenerator().generate(chaintree)
    
