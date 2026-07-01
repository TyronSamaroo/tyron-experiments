import { useState } from "react";
type Player = "X" | "O" | null;

function calcuateWinner(s: Player[]){
  const winningLines = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6],
  ];
  for (const [x,y,z] of winningLines){
    if (
      s[x] &&
      s[x] === s[y] &&
      s[x] === s[z]
    ) return s[x];
  }
  return null
}

export default function App(){
  const [squares, setSquares] = useState<Player []>(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState(true);
  const winner = calcuateWinner(squares);
  const status = winner
    ? `Winner: ${winner}`
    : squares.every(Boolean)
    ? "Draw"
    : `Next player: ${xIsNext ? "X" : "O"}`;

  function handleClick(i: number){
    if (squares[i] || winner) return;
    const next = squares.slice();
    next[i] = xIsNext ? "X" : "O";
    setSquares(next);
    setXIsNext(!xIsNext);
  }

  function reset() {
    setSquares(Array(9).fill(null));
    setXIsNext(true);
  }

  return (
    <main>
      <h1>Tic-Tac-Toe</h1>
      <div style={{
        display:"grid",
        gridTemplateColumns: "repeat(3, 80px)",
        gap:8,
      }}>
        {squares.map((v, i) => (
          <button
            key={i}
            onClick={() => handleClick(i)}
            style={{
              width:80, height:80, fontSize:28, fontWeight:700,
              border:"2px solid #333", borderRadius:8, cursor:"auto"
            }}
            aria-label={`cell-${i}`}
          >
            {v}
          </button>
        ))}
      </div>
      <div style={{ fontSize:18 }}>{status}</div>
      <button data-testid="status"  onClick={reset} style={{ padding:"8px 14px", borderRadius:8, border:"1px solid #333" }}>
        Reset
      </button>
    </main>
  );

}