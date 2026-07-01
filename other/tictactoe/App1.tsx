import {useState} from "react";

function calculateWinner(p){
    const winningLines = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6],
    ];

    for (const [x,y,z] of winningLines){
        if (p[x] &&
            p[x] === p[y] &&
            p[x] === p[z]
        ) return p[x];
    }
    return null
}


export default function App(){
    const [squares, setSquares] = useState(Array(9).fill(null))
    const [xIsNext, setXIsNext] = useState(true)
    const winner = calculateWinner(squares);
    const status = winner
        ? `Winner: ${winner}`
        : squares.every(Boolean)
        ? "Draw"
        : `Next player: ${xIsNext} ? "X" : "O:`


    function handleClick(i: number){
        if (squares[i] || winner) return;
        const next = squares.slice()
        next[i] = xIsNext ? "X" : "O"
        setSquares(next)
        setXIsNext(!xIsNext)
    }

    function reset(){
        setSquares(Array(9).fill(null));
        setXIsNext(true)
    }

    return (
        <main>

        </main>
    )
}