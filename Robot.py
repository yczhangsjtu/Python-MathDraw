from ThreeDObject import ThreeDObject

class Robot:
    def __init__(self):
        self.foot = ThreeDObject()
        self.foot.scale([2.0,0.0,0.0])
        self.foot.move([0.5,0.0,0.0])
        self.foot.addDraw("glutSolidSphere(1.0,20,20)")

        self.sleg = ThreeDObject()
        self.sleg.move([0.0,0.0,-1.0])
        self.sleg.addChild([[[0.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.foot])
        self.sleg.addDraw("glutSolidCylinder(0.5,1.0,20,20)")

        self.leg = ThreeDObject()
        self.leg.move([0.0,0.0,-0.5])
        self.leg.addChild([[[0.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.sleg])
        self.leg.addDraw("glutSolidCylinder(0.25,0.5,20,20)")

        self.hand = ThreeDObject()
        self.hand.move([0.0,0.0,-0.8])
        self.hand.addDraw("glutSolidSphere(1.2,20,20)")

        self.sarm = ThreeDObject()
        self.sarm.move([0.0,0.0,-1.0])
        self.sarm.addChild([[[0.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.hand])
        self.sarm.addDraw("glutSolidCylinder(0.5,1.0,20,20)")

        self.arm = ThreeDObject()
        self.arm.move([0.0,0.0,-0.5])
        self.arm.addChild([[[0.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.sarm])
        self.arm.addDraw("glutSolidCylinder(0.25,0.5,20,20)")

        self.eye = ThreeDObject()
        self.eye.addDraw("glutSolidSphere(0.1,10,10)")

        self.head = ThreeDObject()
        self.head.addChild([[[0.5,0.25,0.25],[0.0,1.0,0.0,0.0],[1.0,1.0,1.0]],\
                            self.eye])
        self.head.addChild([[[0.5,-0.25,0.25],[0.0,1.0,0.0,0.0],[1.0,1.0,1.0]],\
                            self.eye])
        self.head.addDraw("glutSolidSphere(0.5,20,20)")

        self.body = ThreeDObject()
        self.body.move([0.0,0.0,0.5])
        self.body.addChild([[[0.0,-0.125,0.0],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.leg])
        self.body.addChild([[[0.0, 0.125,0.0],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.leg])
        self.body.addChild([[[0.0,-0.375,0.5],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.arm])
        self.body.addChild([[[0.0, 0.375,0.5],[0.0,0.0,1.0,0.0],[0.5,0.5,0.5]],\
                            self.arm])
        self.body.addChild([[[0.0,0.0,0.75],[0.0,0.0,0.0,1.0],[0.5,0.5,0.5]],\
                            self.head])
        self.body.addDraw("glutSolidCylinder(0.25,0.5,20,20)")

    def draw(self):
        self.body.draw()
