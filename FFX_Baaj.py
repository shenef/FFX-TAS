import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_targetPathing
import FFX_menu
import FFX_vars

FFXC = FFX_Xbox.controllerHandle()
gameVars = FFX_vars.varsHandle()


def Entrance():
    FFX_memory.awaitControl()
    print("Starting Baaj exterior area")
    FFXC.set_neutral()
    FFX_menu.shortAeons()

    # Now back into the water
    checkpoint = 0
    while not FFX_memory.battleActive():
        if FFX_memory.userControl():
            if checkpoint == 6:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.baajRamp(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

    FFXC.set_neutral()

    # Battles
    while FFX_memory.getStoryProgress() < 48:
        if FFX_Screen.BattleScreen():
            if FFX_memory.getEncounterID() == 2:
                FFX_Battle.attack('none')
            else:
                FFX_Battle.defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()

    # Out of the frying pan, into the furnace
    FFX_memory.clickToControl()
    print("Hallway before main puzzle.")
    checkpoint = 0
    while FFX_memory.getMap() != 63:
        if FFX_memory.userControl():
            if checkpoint == 9:
                FFXC.set_movement(-1, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.baajHallway(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()


def Baaj_puzzle():
    FFX_memory.clickToControl()
    print("Ready for the main puzzle.")
    checkpoint = 0
    while not FFX_memory.battleActive():
        if FFX_memory.userControl():
            # Events
            if checkpoint == 3:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 5:  # Flint room
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 6:  # Obtain Flint
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 7:  # Exit Flint room
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 12:  # Bouquet hallway
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 21:  # Withered bouquet
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 32:  # Back to main room
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 33:  # To the fireplace
                FFX_targetPathing.setMovement([1, 1])
                FFX_Xbox.menuB()

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.baajPuzzle(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()


def Klikk_fight():
    # Before Rikku shows up, we're just going to spam the B button. Simple.
    FFXC.set_neutral()
    while not FFX_Screen.turnRikku():
        FFX_Xbox.tapB()

    FFX_Xbox.clickToBattle()
    FFX_Battle.useItem(0, 'none')

    # Tidus self-potion
    FFX_Screen.awaitTurn()
    FFX_Battle.Klikk()


def distance(n1, n2):
    try:
        player1 = FFX_memory.getActorCoords(actorNumber=n1)
        player2 = FFX_memory.getActorCoords(actorNumber=n2)
        return (abs(player1[1] - player2[1]) + abs(player1[0] - player2[0]))
    except Exception as x:
        print("Exception:", x)
        return 999


def ABboat1():
    print("Start of Al Bhed boat section.")
    FFX_memory.clearSaveMenuCursor2()
    FFXC.set_neutral()
    if gameVars.csr():
        FFX_memory.waitFrames(10)
    print("Control restored.")
    print("On the boat!")
    while FFX_memory.getActorCoords(actorNumber=0)[0] > -50:
        rikkuNum = FFX_memory.actorIndex(actorNum=41)
        target = FFX_memory.getActorCoords(actorNumber=rikkuNum)
        FFX_targetPathing.setMovement(target)
        if distance(0, rikkuNum) < 10:
            FFX_Xbox.tapB()
    print("In the water!")
    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(20)

    while FFX_memory.getMap() != 288:
        FFXC.set_value('BtnA', 1)
        FFXC.set_movement(0, -1)
        if FFX_memory.battleActive():
            FFXC.set_neutral()
            print("Battle Start (Al Bhed swimming section)")
            FFX_Battle.stealAndAttack()
            print("Battle End (Al Bhed swimming section)")
        elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            print("Battle Complete screen")
            FFX_Xbox.tapB()


def ABswimming1():
    print("Swimming down from the boat")
    while FFX_memory.getMap() != 288:
        if FFX_memory.userControl():
            FFX_targetPathing.setMovement([-300, -300])
            FFXC.set_value('BtnA', 1)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                print("Battle Start (Al Bhed swimming section)")
                FFX_Battle.stealAndAttack()
                print("Battle End (Al Bhed swimming section)")
            elif FFX_memory.menuOpen():
                print("Battle Complete screen")
                FFX_Xbox.menuB()

    FFXC.set_neutral()
    print("Swimming towards airship")
    while FFX_memory.getMap() != 64:
        pos = FFX_memory.getCoords()
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 71:
                FFXC.set_movement(0, -1)
                FFXC.set_value('BtnA', 1)
            else:
                FFXC.set_value('BtnA', 0)
                if pos[1] > -230:
                    FFX_targetPathing.setMovement([-343, -284])
                elif pos[1] > -410:
                    FFX_targetPathing.setMovement([-421, -463])
                else:
                    FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                print("Battle Start (Al Bhed swimming section)")
                FFX_Battle.stealAndAttack()
                print("Battle End (Al Bhed swimming section)")
            elif FFX_memory.menuOpen():
                print("Battle Complete screen")
                FFX_Xbox.menuB()


def ABswimming2():
    # Quick heal-up to make sure we're full HP on Rikku
    FFX_memory.awaitControl()
    FFXC.set_movement(1, -1)
    FFXC.set_value('BtnA', 1)
    FFX_memory.touchSaveSphere()

    FFX_memory.clearSaveMenuCursor2()
    # Now to get to it
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1)
    FFX_memory.clickToEvent()
    FFX_memory.waitFrames(30 * 0.2)
    FFX_memory.awaitControl()

    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] < 135:
            FFXC.set_movement(1, 1)
        else:
            FFXC.set_movement(0, 1)

        pos = FFX_memory.getCoords()
    FFXC.set_neutral()

    FFX_Screen.awaitTurn()
    # Final group of Piranhas
    FFX_Battle.stealAndAttackPreTros()
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    print("Technical Support Tidus")
    FFX_Xbox.SkipDialog(2)
    FFXC.set_movement(0, 0)
    FFX_memory.clickToControl()
    while not FFX_memory.battleActive():
        FFXC.set_movement(0, -1)
    print("Engaging Tros")
    FFXC.set_neutral()

    # Tros fight
    FFX_Xbox.clickToBattle()
    FFX_Battle.Tros()

    FFXC.set_neutral()
    while FFX_memory.getStoryProgress() < 111:
        if FFX_memory.userControl():
            if FFX_memory.diagProgressFlag() == 109 and not FFX_memory.userControl():
                FFXC.set_neutral()
                if FFX_memory.saveMenuCursor2() == 0:
                    FFX_Xbox.tapA()
                else:
                    FFX_Xbox.tapB()
                FFX_memory.waitFrames(4)
            elif FFX_memory.getMap() == 64:
                if FFX_memory.getCoords()[0] < -4:
                    FFX_targetPathing.setMovement([-2, 47])
                else:
                    FFX_targetPathing.setMovement([73, 1])
            elif FFX_memory.getMap() == 380:
                FFX_targetPathing.setMovement([700, 300])
            elif FFX_memory.getMap() == 71:
                rikkuNum = FFX_memory.actorIndex(actorNum=41)
                FFX_targetPathing.setMovement(FFX_memory.getActorCoords(rikkuNum))
                if distance(0,rikkuNum) < 30:
                    FFX_Xbox.tapB()
        else:
            FFXC.set_neutral()
            if FFX_memory.diagProgressFlag() == 109:
                FFX_memory.csrBaajSaveClear()
            elif FFX_memory.diagSkipPossible() and not gameVars.csr():
                FFX_Xbox.tapB()

    print("Should now be ready for Besaid")

    if not gameVars.csr():
        FFX_Xbox.clearSavePopup(0)
