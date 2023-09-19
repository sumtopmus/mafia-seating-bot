from mafia_schedule.configuration import Configuration

Configurations = {
    "test_tournament":
        Configuration(numPlayers=25, numTables=2, numRounds=10,
                      numGames=20, numAttempts=8),
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

    "mlm2021-20":
        Configuration(numPlayers=20, numTables=2, numRounds=10,
                      numGames=20, numAttempts=10),

    "mlm2021-16":
        Configuration(numPlayers=16, numTables=1, numRounds=16,
                      numGames=16, numAttempts=10),

    "chicago2021":
        Configuration(numPlayers=28, numTables=2, numRounds=14,
                      numGames=28, numAttempts=10),

    "sacramento2021":
        Configuration(numPlayers=28, numTables=2, numRounds=14,
                      numGames=28, numAttempts=10),

    "blackfriday2021-20p":
        Configuration(numPlayers=20, numTables=2, numRounds=10,
                      numGames=20, numAttempts=10),

    "blackfriday2021-21p":
        Configuration(numPlayers=21, numTables=2, numRounds=11,
                      numGames=21, numAttempts=10),

    "rendezvouz-2022":
        Configuration(numPlayers=40, numTables=4, numRounds=15,
                      numGames=60, numAttempts=15, numTeams=20),

    "bigapple-2022":
        Configuration(numPlayers=25, numTables=2, numRounds=13,
                      numGames=25, numAttempts=10),

    "millenium-2022-30":
        Configuration(numPlayers=30, numTables=3, numRounds=10,
                      numGames=30, numAttempts=10),

    "millenium-2022-31":
        Configuration(numPlayers=31, numTables=3, numRounds=11,
                      numGames=31, numAttempts=10),

    "millenium-2022-32":
        Configuration(numPlayers=32, numTables=3, numRounds=11,
                      numGames=32, numAttempts=10),

    "wedding-2022":
        Configuration(numPlayers=20, numTables=2, numRounds=8,
                      numGames=16, numAttempts=8),

    "sacramento-2022-39":
        Configuration(numPlayers=39, numTables=3, numRounds=13,
                      numGames=39, numAttempts=10),

    "evergreen-2022":
        Configuration(numPlayers=20, numTables=2, numRounds=10,
                      numGames=20, numAttempts=10),

    "blackfriday-2022":
        Configuration(numPlayers=24, numTables=2, numRounds=12,
                      numGames=24, numAttempts=10),

    "rv-2023":
        Configuration(numPlayers=30, numTables=3, numRounds=14,
                      numGames=42, numAttempts=14, numTeams=15),

    "foreva-2023":
        Configuration(numPlayers=20, numTables=2, numRounds=10,
                      numGames=20, numAttempts=10),

    "kaa-15-2023":
        Configuration(numPlayers=15, numTables=1, numRounds=15,
                      numGames=15, numAttempts=10),
    "kaa-16-2023":
        Configuration(numPlayers=16, numTables=1, numRounds=16,
                      numGames=16, numAttempts=10),

    "kaa-20-2023":
        Configuration(numPlayers=20, numTables=2, numRounds=8,
                      numGames=16, numAttempts=8),

    "goldengate-2023":
        Configuration(numPlayers=30, numTables=3, numRounds=10,
                      numGames=30, numAttempts=10),

    "mafstart-2023":
        Configuration(numPlayers=24, numTables=2, numRounds=12,
                      numGames=24, numAttempts=10),
}
