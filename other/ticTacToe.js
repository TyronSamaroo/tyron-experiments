function createBoard2() {
    return Array.from({ length: 3}, () => Array(3).fill(null))
}

function checkWinner2(board){
    const lines = [
        ...board,
        // Columns
    [board[0][0], board[1][0], board[2][0]],
    [board[0][1], board[1][1], board[2][1]],
    [board[0][2], board[1][2], board[2][2]],
    // Diagonals
    [board[0][0], board[1][1], board[2][2]],
    [board[0][2], board[1][1], board[2][0]],
    ];

    for (const line of lines) {
        if (line[0] && line.every((cell) => cell === line[0])){
            return line[0];
        }
    }

    return board.flat().every(Boolean) ? 'Draw' : null;
}


let board = createBoard2();
board[0][0] = 'X';
board[1][1] = 'X';
board[2][2] = 'X';

console.log(board);
console.log(checkWinner2(board)); // "X"