import java.nio.file.{Files, Paths}
import scala.collection.mutable
import scala.io.Source

/*
    sokoban solver, Jason Zavaglia 22/12/2015

     representation of board:
    
     # - wall
     X - target square
     B - box
     ' ' - blank space
     * - person
    
    Note that two boards are encoded, contains
    location of X's, and the other contains
    location of boxes.
    
    Note any line starting with # is a map,
    any other line is ignored.  Two maps are expected,
    and walls must agree.
    
     e.g.
    
    #######
    ## X ##
    ## X ##
    ## X ##
    #  X ##
    #  X  #
    #  X  #
    ###  ##
    #######
    
    #######
    ## * ##
    ##B B##
    ## B ##
    #  B ##
    #  B  #
    #  B  #
    ###  ##
    #######
*/

if (args.length != 1 || Files.notExists(Paths.get(args(0)))) {
    println("usage: sokoban_solver.scala mapfile")
    System.exit(1)
}

val filename = args(0)

type Coord = (Int, Int)
case class Board(board: Vector[Vector[Char]])

case class BoardState(board: Vector[Vector[Char]], 
    targetLocations: Set[Coord],
    personLocation: Coord,
    boxLocations: Set[Coord]) {

    val isSolved = boxLocations == targetLocations

    // helper to determine if coordinate is within bounds
    def isWithinBounds(location: Coord) : Boolean = {
        val (r, c) = location
        ! (r < 0 || c < 0 || r > board.length-1 || c > board.head.length-1)
    }

    // helper function for a small piece of movement arithmetic
    def calculateMoveToCell(location: Coord, direction: Char) : Coord  = {
        var (r, c) = location
        direction match {
            case 'U' => r = r - 1
            case 'D' => r = r + 1
            case 'L' => c = c - 1
            case 'R' => c = c + 1
            case _ => throw new Exception(s"bad direction: '$direction'")
        }
        (r, c)
    }

    // determines if move is valid
    def canMove(direction: Char) : Boolean = {
        val coord = calculateMoveToCell(personLocation, direction)
        val (r, c) = coord

        // can't move off map
        if (!isWithinBounds(coord)) {
            false
        }

        // can't move into a wall
        else if (board(r)(c) == '#') {
            false
        }

        // can move into a box if the box can move in same direction
        else if (boxLocations contains coord) {
            boxCanMove(coord, direction)
        }
        else {
            true
        }
    }

    // determines if box can move in given direction
    def boxCanMove(boxLocation: Coord, direction: Char) = {
        val coord = calculateMoveToCell(boxLocation, direction)
        val (r, c) = coord

        // can't move box off map
        if (!isWithinBounds(coord)) {
            false
        }

        // can't move box into wall
        else if (board(r)(c) == '#') {
            false
        }

        // can't move box into another box
        else if (boxLocations contains coord) {
            false
        }
        else {
            true
        }
    }

    // return a new BoardState based upon valid move;
    // throw exception for invalid move
    def move(direction: Char) : BoardState = {
        val coord = calculateMoveToCell(personLocation, direction)

        // recalculate the box locations based upon move
        var newBoxLocations = boxLocations

        if (boxLocations contains coord) {
            val newCoord = calculateMoveToCell(coord, direction)
            newBoxLocations = boxLocations - coord
            newBoxLocations = newBoxLocations + newCoord
            if (newBoxLocations.size != boxLocations.size)
                throw new Exception("box locations size changed")
        }
        BoardState(board, targetLocations, coord, newBoxLocations)
    }
}


def readMapFile(fileContents: Source) : (Vector[Vector[Char]], Vector[Vector[Char]]) = {

    var board1 = Vector[Vector[Char]]()
    var board2 = Vector[Vector[Char]]()

    var processedBoard1 = false
    var processedBoard2 = false

    for (line <- fileContents.getLines()) {

      val isBoardLine = line.length > 0 && line.charAt(0) == '#'

        if (!isBoardLine) {
            if (board1.nonEmpty)
                processedBoard1 = true
            if (board2.nonEmpty)
                processedBoard2 = true
        }
        else {
            if (!processedBoard1)
                // append Vector[Char] element to board1
                board1 = board1 :+ line.toVector
            else if (!processedBoard2)
                // append Vector[Char] element to board2
                board2 = board2 :+ line.toVector
        }
    }

    (board1, board2)
}

def buildBoardState(board1: Vector[Vector[Char]], board2: Vector[Vector[Char]]) : BoardState = {
    if (board1.isEmpty) {
        throw new Exception("no boards present")
    }

    if (board2.isEmpty) {
        throw new Exception("second board not present")
    }

    if (board1.length != board2.length) {
        throw new Exception("board pair have different row count")
    }

    val rowCount = board1.length
    val columnCount = board1.head.length

    if (!board1.forall(_.length == columnCount)) {
        throw new Exception("column counts are inconsistent")
    }

    if (!board2.forall(_.length == columnCount)) {
        throw new Exception("column counts are inconsistent")
    }

    val board1elements = Set('#', ' ', 'X')
    val board2elements = Set('#', ' ', '*', 'B')

    var personLocation: Option[Coord] = None
    var targetLocations = Set[Coord]()
    var boxLocations = Set[Coord]()

    for (r <- 0 until rowCount; c <- 0 until columnCount)
    {
        val board1cell = board1(r)(c)
        val board2cell = board2(r)(c)
        // a few validation checks
        if (board1cell == '#' && board2cell != '#') {
            throw new Exception("walls are inconsistent")
        }
        if (!board1elements.contains(board1cell)) {
            throw new Exception(s"unexpected character '$board1cell' found in first board")
        }
        if (!board2elements.contains(board2cell)) {
            throw new Exception(s"unexpected character '$board2cell' found in second board")
        }

       if (board1cell == 'X')
           targetLocations = targetLocations + Tuple2(r, c)
       if (board2cell == '*')
           personLocation = Some((r, c))
       if (board2cell == 'B')
           boxLocations = boxLocations + Tuple2(r, c)
    }

    if (personLocation.isEmpty)
        throw new Exception("no person location found")

    // scrub out the special characters and leave just walls and blanks
    val cleanBoard = board1 map { row => row map { case '#' => '#' case ' ' => ' ' case _ => ' ' } }

    BoardState(cleanBoard, targetLocations, personLocation.get, boxLocations)
}

def breadthFirstSearch(boardState: BoardState) = {
    val moveToGetToBoardState = mutable.Map[BoardState, Char]()
    val parent = mutable.Map[BoardState, BoardState]()
    val queue = mutable.Queue[BoardState]()
    var solution: Option[BoardState] = None
    moveToGetToBoardState(boardState) = '*'
    parent(boardState) = null
    queue.enqueue(boardState)

    var cnt = 0
    while(queue.nonEmpty && solution.isEmpty) {
        cnt = cnt + 1
        val boardState = queue.dequeue()
        if (cnt % 10000 == 0)
            println(s"iteration $cnt, queuelength ${queue.length}")
        if(boardState.isSolved) {
            solution = Some(boardState)
        }
        else {
            for (direction <- List('U', 'D', 'L', 'R')) {
                if (boardState.canMove(direction)) {
                    val newBoardState = boardState.move(direction)
                    if (!moveToGetToBoardState.contains(newBoardState)) {
                        moveToGetToBoardState(newBoardState) = direction
                        parent(newBoardState) = boardState
                        queue.enqueue(newBoardState)
                    }
                }
            }
        }
    }

    println(s"total iterations = $cnt")

    var moves = List[Char]()
    if (solution.isEmpty) {
        throw new Exception("no solution found")
    }
    var soln = solution.get
    // walk the solution backward, and put the moves into a list
    while (soln != null) {
        // if guards against adding the "non-move" right in the first location
        if (moveToGetToBoardState(soln) != '*')
            moves = moveToGetToBoardState(soln) :: moves
        soln = parent(soln)
    }

    if (moves.isEmpty) {
        println("no solution found")
    }
    else {
        println("solution: ")
        for ((elem, i) <- moves.zipWithIndex)
            println(s"${i+1} $elem")
    }
}


val (board1, board2) = readMapFile(Source.fromFile(filename))
val boardState = buildBoardState(board1, board2)

breadthFirstSearch(boardState)


