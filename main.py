import sys
from commands import *
from schedule import *
 
Configurations = {
    "VaWaCa-2017":
        Configuration(numPlayers=25, numTables=2, numRounds=10,
                      numGames=20, numAttempts=8),
    "VaWaCa-2019":
        Configuration(numPlayers=30, numTables=3, numRounds=10,
                      numGames=30, numAttempts=10),
    "MiniTournament12":
        Configuration(numPlayers=12, numTables=1, numRounds=12,
                      numGames=12, numAttempts=10),
    "GG-2021":
        Configuration(numPlayers=36, numTables=3, numRounds=12,
                      numGames=36, numAttempts=10),

    "VaWaCa-2021":
        Configuration(numPlayers=36, numTables=3, numRounds=12,
                      numGames=36, numAttempts=10),

    "mlm2021":
        Configuration(numPlayers=20, numTables=2, numRounds=10,
                      numGames=20, numAttempts=10),
}



def main():
    if len(sys.argv) < 2:
        print("Expected opponents|seats|show")
        return

    conf_name = "mlm2021"
    conf = Configurations[conf_name]
    print(f"Configuration name: {conf_name}\n{conf}")

    default_opponents = f"{conf_name}_opponents.txt"
    default_seats = f"{conf_name}_seats.txt"
    default_participants = f"{conf_name}_participants.txt"

    command = sys.argv[1]
    print(f"Command: {command}")

    if command == "opponents":
        filename_opponents = sys.argv[2] if len(sys.argv) > 2 else default_opponents
        print(f"Output opponents: {filename_opponents}")
        
        default_numRuns = 10
        default_numIterations = 10 * 1000
        numRuns = int(sys.argv[3]) if len(sys.argv) > 3 else default_numRuns
        numIterations = int(sys.argv[4]) if len(sys.argv) > 4 else default_numIterations
        print(f"numRuns: {numRuns}, numIterations: {numIterations}")

        default_zeroPairs = 0
        expectedZeroPairs = int(sys.argv[5]) if len(sys.argv) > 5 else default_zeroPairs
        print(f"ExpectedZeroPairs: {expectedZeroPairs}")

        optimizeOpponents(conf, filename_opponents, numRuns, numIterations, expectedZeroPairs)

    if command == "seats":
        filename_opponents = sys.argv[2] if len(sys.argv) > 2 else default_opponents
        filename_seats = sys.argv[3] if len(sys.argv) > 3 else default_seats
        print(f"Input opponents: {filename_opponents}")
        print(f"Output seats: {filename_seats}")

        default_numRuns = 10 
        default_numIterationsStageOne = 10 * 1000
        default_numIterationsStageTwo = 10 * 1000
        numRuns = int(sys.argv[4]) if len(sys.argv) > 4 else default_numRuns
        numIterationsStageOne = int(sys.argv[5]) if len(sys.argv) > 5 else default_numIterationsStageOne
        numIterationsStageTwo = int(sys.argv[6]) if len(sys.argv) > 6 else default_numIterationsStageTwo
        listIterations = [numIterationsStageOne, numIterationsStageTwo]
        print(f"numRuns: {numRuns}, iterations: {listIterations}")

        optimizeSeats(filename_opponents, filename_seats, numRuns, listIterations)
    
    if command == "participants":
        filename_participants = sys.argv[2] if len(sys.argv) > 2 else default_participants
        generateParticipants(conf, filename_participants)

    if command == "show":
        filename_schedule = sys.argv[2] if len(sys.argv) > 2 else default_seats
        filename_participants = sys.argv[3] if len(sys.argv) > 3 else default_participants
        showSchedule(filename_schedule, filename_participants)
    
if __name__ == '__main__':
    main()
