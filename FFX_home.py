import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

def desert():
    FFX_memory.clickToControl()
    
    #Speed sphere stuff. Improve this later.
    needSpeed = False
    if FFX_memory.getSpeed() < 9:
        needSpeed = True
        #FFX_memory.setSpeed(9)
        #Reprogram battle logic to throw some kind of grenades.
    
    #Same for Power spheres
    if FFX_memory.getPower() < 23:
        needPower = True
    
    #Logic for finding Teleport Spheres x2 (only chest in this area)
    teleSlot = FFX_memory.getItemSlot(98)
    if teleSlot == 255:
        teleCount = 0
    else:
        teleCount = FFX_memory.getItemCountSlot(teleSlot)
    
    
    chargeState = False #Rikku charge, speed spheres
    #Bomb cores, sleeping powders, smoke bombs, silence grenades
    stealItems = [0,0,0,0]
    itemsNeeded = 0
    
    #Now to figure out how many items we need.
    stealItems = FFX_Battle.updateStealItemsDesert()
    #if stealItems[0] == 2: #Bomb Cores aren't working right.
    #    itemsNeeded = 5 - (stealItems[1] + stealItems[2] + stealItems[3])
    #else:
    #    itemsNeeded = 7 - (stealItems[1] + stealItems[2] + stealItems[3])
    itemsNeeded = 7 - (stealItems[1] + stealItems[2] + stealItems[3])
    
    FFX_menu.equipSonicSteel()
    
    checkpoint = 0
    firstFormat = False
    while FFX_memory.getMap() != 130:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint == 9:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint < 39 and FFX_memory.getMap() == 137:
                checkpoint = 39
            elif checkpoint < 50 and FFX_memory.getMap() == 138:
                checkpoint = 50
            
            #Other events
            elif checkpoint == 2 or checkpoint == 24: #Save sphere
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.2)
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 53:
                print("Going for first Sandragora and chest")
                teleSlot = FFX_memory.getItemSlot(98)
                if teleSlot == 255:
                    FFX_targetPathing.setMovement([-44,446])
                    FFX_Xbox.tapB()
                elif teleCount == FFX_memory.getItemCountSlot(teleSlot):
                    FFX_targetPathing.setMovement([-44,446])
                    FFX_Xbox.tapB()
                else:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
            elif checkpoint == 12 and firstFormat == False:
                firstFormat = True
                FFX_memory.fullPartyFormat('desert9')
            elif checkpoint == 59:
                if itemsNeeded >= 1: #Cannot move on if we're short on throwable items
                    checkpoint -= 2
                elif needSpeed == True: #Cannot move on if we're short on speed spheres
                    checkpoint -= 2
                else:
                    checkpoint += 1
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.desert(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.menuB()
            if FFX_memory.battleActive(): #Lots of battle logic here.
                FFX_Screen.clickToBattle()
                if checkpoint < 7 and FFX_memory.getBattleNum() == 197: #First battle in desert
                    FFX_Battle.zu()
                elif FFX_memory.getBattleNum() == 234: #Sandragora logic
                    print("Sandragora fight")
                    if checkpoint < 55:
                        FFX_Battle.sandragora(1)
                    else:
                        FFX_Battle.sandragora(2)
                else:
                    FFX_Battle.bikanelBattleLogic([chargeState, needSpeed, needPower, itemsNeeded])
                
                #After-battle logic
                FFX_memory.clickToControl()
                
                #First, check and update party format.
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        FFX_memory.fullPartyFormat('desert9')
                    elif chargeState == False:
                        FFX_memory.fullPartyFormat('desert1')
                    elif needPower == True:
                        FFX_memory.fullPartyFormat('desert1')
                    elif needSpeed == True:
                        FFX_memory.fullPartyFormat('desert1')
                    elif itemsNeeded >= 1:
                        FFX_memory.fullPartyFormat('desert1')
                    else: #Catchall
                        FFX_memory.fullPartyFormat('desert1')
                        #formerly desert2, but it works out better to have Kimahri in the fourth slot
                
                #Next, figure out how many items we need.
                stealItems = FFX_Battle.updateStealItemsDesert()
                print("-----------------------------")
                print("Items status: ", stealItems)
                print("-----------------------------")
                #if stealItems[0] == 2: #Bomb Cores aren't working right.
                #    itemsNeeded = 5 - (stealItems[1] + stealItems[2] + stealItems[3])
                #else:
                #    itemsNeeded = 7 - (stealItems[1] + stealItems[2] + stealItems[3])
                itemsNeeded = 7 - (stealItems[1] + stealItems[2] + stealItems[3])
                
                #Finally, check for other factors and report to console.
                if FFX_memory.overdriveState()[6] == 100:
                    chargeState = True
                if FFX_memory.getSpeed() >= 9:
                    needSpeed = False
                if FFX_memory.getPower() >= 23:
                    needPower = False
                print("-----------------------------Flag statuses")
                print("Rikku is charged up: ", chargeState)
                print("Need more Speed spheres: ", needSpeed)
                print("Need more Power spheres: ", needPower)
                print("Number of additional items needed before Home: ", itemsNeeded)
                print("-----------------------------Flag statuses (end)")
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def desert1():
    print("Starting Bikanel Island section")
    needSpeed = False
    if FFX_memory.getSpeed() < 9:
        FFX_memory.setSpeed(9)
        #needSpeed = True
        #nadeSlot = FFX_memory.getItemSlot(39)
        #if nadeSlot != 255:
        #    FFX_menu.itemPos(39, 8)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitTurn()
    tidusturns = 0
    while not FFX_memory.menuOpen():
        if FFX_Screen.BattleScreen():
            turnchar = FFX_memory.getBattleCharTurn()
            if turnchar == 0:
                if tidusturns < 2:
                    FFX_Battle.attack("none")
                elif FFX_memory.partySize() > 2:
                    FFX_Battle.tidusFlee()
                else:
                    FFX_Battle.defend()
                tidusturns += 1
            else:
                if checkpoint == 170 or checkpoint == 190:
                    print("Looking for Sandragoras")
                    battleId = FFX_Battle.desertFights(battleId)
                elif rikkuFound == False:
                    FFX_Battle.fleeAll()
                elif chargeState == [True,True]:
                    if needSpeed == True:
                        needSpeed = FFX_Battle.desertSpeed(chargeState)
                    else:
                        print("Don't need anything else. Moving on.")
                        FFX_Battle.fleeAll()
                else:
                    chargeState = FFX_Battle.bikanelCharge(chargeState)
                    FFX_memory.desertFormat(chargeState[0])
                    print("Current state variable: ", chargeState)
        else: FFX_Xbox.menuB() #Skip Dialog

    FFX_Screen.clickToMap1()
    FFX_menu.equipSonicSteel()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(0.4)
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', 1)
    #FFX_Xbox.SkipDialog(0.6)
    #FFXC.set_value('AxisLy', 0)
    #FFX_memory.clickToControl() #Picking up al bhed potions
    
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)

    chargeState = [False,False] #Rikku and Kimahri charge status
    orderFlip = False
    rikkuFound = False
    checkpoint = 0
    lastCP = 0
    battleId = 0
    
    while checkpoint != 200:
        if lastCP != checkpoint:
            print("Checkpoint: ", checkpoint)
            lastCP = checkpoint
        pos = FFX_memory.getCoords()
        if FFX_memory.userControl():
            cam = FFX_memory.getCamera()
            #if checkpoint > 150: print("Checkpoint: ", checkpoint)
            if checkpoint == 0:
                if FFX_memory.getStoryProgress() == 1718:
                    checkpoint = 5
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    
            elif checkpoint == 5:
                if cam[0] > -1.2:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0) #Leave Kimahri corner
            elif checkpoint == 10:
                if pos[1] < ((-0.75 * pos[0]) - 530.18):
                    checkpoint = 15
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 15:
                if pos[1] > ((2.41 * pos[0]) + 42.85):
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < ((-0.75 * pos[0]) - 530.18):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 20:
                if pos[0] > 120:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -190:
                        FFXC.set_value('AxisLx', 0)
                    elif pos[1] < ((-4.25 * pos[0]) -1040):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] > -30:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1) #Up to Rikku dialog
                    if pos[1] < ((3.03 * pos[0]) -619.85):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                print("We've reached Rikku.")
                FFXC.set_value('AxisLy', 1)
                time.sleep(1.8)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.touchSaveSphere()
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.3)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(1)
                
                #Around the tent
                FFX_memory.clickToControl()
                print("Left around the tent.")
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.4)
                print("Forward around the tent.")
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(1.5)
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(1.5)
                FFXC.set_value('AxisLx', 0)
                time.sleep(3.5)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 50
                rikkuFound = True
                
            elif checkpoint == 50:
                if pos[0] > 580:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if FFX_memory.getCamera()[0] > -0.8:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    time.sleep(0.3)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.3)
            elif checkpoint == 70:
                if pos[1] > 790:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 650:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 660:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                if pos[1] < -1:
                    checkpoint = 85
                else:
                    FFXC.set_value('AxisLy', 1) #Into the big open zone
                    if pos[0] < 680:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 85:
                if pos[1] > -430:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', 1) #Past tiny nub thing
                    if pos[0] > 400:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 90:
                if pos[1] > 210:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLy', 1) #Left of sign
                    if pos[1] > ((-1.50 * pos[0]) + 133.45):
                        FFXC.set_value('AxisLx', -1)
                    #elif pos[0] < -50:
                    #    FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 100:
                if pos[0] < -150:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 110:
                if pos[0] < -630:
                    checkpoint = 120
                else:
                    FFXC.set_value('AxisLy', 1) #Into the dangerous area
                    if pos[1] > 320:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 120:
                if pos[1] > 740:
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[0] > -670:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 130:
                if pos[1] < -1:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLy', 1) #To the Sandragora zone
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 140:
                if pos[0] > -250:
                    checkpoint = 150
                else:
                    FFXC.set_value('AxisLy', 0) #Avoid sign collision
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 150:
                if pos[0] > -180:
                    checkpoint = 155
                else:
                    FFXC.set_value('AxisLy', 0) #Avoid sign collision
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 155:
                if chargeState == [True, True]:
                    checkpoint = 170
                else:
                    FFXC.set_value('AxisLy', -1) #To the Sandragora zone
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.8)
            elif checkpoint == 170:
                    if pos[1] > 455:
                        FFXC.set_value('AxisLy', -1) #Up to Sandy and chest
                        print("Overshot. Backtracking.")
                    else:
                        FFXC.set_value('AxisLy', 1) #Up to Sandy and chest
                    if pos[0] < -45:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > -35:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
                    FFX_Xbox.menuB()
            elif checkpoint == 175: #Stall if we are short on speed spheres
                if needSpeed == False:
                    checkpoint = 180
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(2)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(2)
            elif checkpoint == 180:
                if pos[1] > 770:
                    checkpoint = 190 #Just before second Sandy
                else:
                    FFXC.set_value('AxisLy', 1) #Left towards second Sandy
                    if pos[0] > -220:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[0] < -270:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 190:
                if pos[1] < -1:
                    checkpoint = 200
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > -220:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[0] < -270:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                if checkpoint == 170 or checkpoint == 190:
                    print("Looking for Sandragoras")
                    battleId = FFX_Battle.desertFights(battleId)
                elif rikkuFound == False:
                    FFX_Battle.fleeAll()
                elif chargeState == [True,True]:
                    if needSpeed == True:
                        needSpeed = FFX_Battle.desertSpeed(chargeState)
                    else:
                        print("Don't need anything else. Moving on.")
                        FFX_Battle.fleeAll()
                else:
                    chargeState = FFX_Battle.bikanelCharge(chargeState)
                    FFX_memory.desertFormat(chargeState[0])
                    print("Current state variable: ", chargeState)
            elif FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif checkpoint == 170 and FFX_Screen.PixelTestTol(601,445,(210, 210, 210),5):
                print("Teleport Sphere chest.")
                FFX_memory.clickToControl()
                checkpoint = 175
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()

def findSummoners(blitzWin):
    FFX_memory.clickToControl()
    FFX_menu.homeGrid()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2.9)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3) #Enter Home
    FFXC.set_value('AxisLx', 0)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Battle.home1() #First battle
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.home2() #Second battle
    #FFX_menu.homeHeal() #Healing up
    FFXC.set_value('AxisLy', -1)
    time.sleep(2.8)
    
    #Big back track if we lost Blitz
    if blitzWin == False:
        FFXC.set_value('AxisLy', 0)
        time.sleep(0.3)
        FFXC.set_value('AxisLy', -1)
        time.sleep(3)
        FFXC.set_value('AxisLx', -1)
        time.sleep(2.5)
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', 0)
        
        FFX_Battle.home3() #Third battle (the spare room)
        time.sleep(0.5)
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 1)
        time.sleep(0.3)
        FFXC.set_value('AxisLx', 0)
        time.sleep(0.7)
        FFX_Xbox.menuB()
        FFXC.set_value('AxisLy', 0)
        time.sleep(1)
        FFX_Xbox.menuB()
        time.sleep(1)
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuB()
        time.sleep(1)
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuB()
        time.sleep(1)
        FFX_Xbox.menuRight()
        FFX_Xbox.menuRight()
        FFX_Xbox.menuRight()
        FFX_Xbox.menuRight()
        FFX_Xbox.menuB()
        time.sleep(3)
        FFX_Xbox.menuB()
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 1)
        time.sleep(1.5)
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', 0)
        
        FFX_memory.awaitControl()
    
    pos = FFX_memory.getCoords()
    while pos[0] > -150:
        if not FFX_memory.userControl():
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            else:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('BtnB',1)
                time.sleep(0.035)
                FFXC.set_value('BtnB',0)
                time.sleep(0.035)
        else:
            pos = FFX_memory.getCoords()
            if pos[1] < 300:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 1)
            elif pos[1] < 360:
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 1)
            else:
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.5)
    
    
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.home4()
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(2) #Pick up chest.
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(3)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(8)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Xbox.SkipDialog(90) #Start of the "Yuna will die" scene.
    FFX_memory.awaitControl()
    
    #FFX_Screen.clickToPixel(351,225,(64,193,64)) #40C140
    #FFX_Screen.awaitPixel(351,225,(64,193,64)) #40C140
    FFXC.set_value('AxisLy', -1) #Now to the airship.
    time.sleep(2.6)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    while not FFX_memory.cutsceneSkipPossible():
        FFX_Xbox.tapB()
    FFX_Xbox.skipScene()
    FFX_Xbox.SkipDialog(8.2) #For some reason, it thinks there's a cutscene to skip this whole time.
    FFX_Xbox.skipScene()
    
    while not FFX_memory.userControl():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()