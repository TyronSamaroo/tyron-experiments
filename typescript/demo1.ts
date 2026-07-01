const questions = [
    "Would you rather have unlimited coffee or unlimited naps?",
    "Would you rather fight 1 horse-zied duck or 100 duck-sized horses?",
    "Would you rather know all languages or play all instruments?"
] as const;

function randomQuestion(exclude: Set<number>){
    let idx;
    do{
        idx = Math.floor(Math.random() * questions.length);
    } while (exclude.has(idx));

    exclude.add(idx)
    return questions[idx];
}

const used = new Set<number>();
console.log(randomQuestion(used));




interface FoodEntry{
    name: string;
    calories: number;
    time: string;
}

let log: FoodEntry[] = [];
function addFood(name: string, calories: number){
    log.push({
        name,
        calories,
        time: new Date().toISOString()
    });
}

function total(){
    return log.reduce((sum,f) => sum + f.calories, 0);
}

addFood("Greek Yogurt", 100)
addFood("Protein Shake", 100)
console.log(log);
console.log("Total:", total());


async function rest(seconds: number){
    for (let i = seconds; i> 0; i--){
        console.log(`Rest: ${i}s`);
        await new Promise(r => setTimeout(r, 250));
    }
    console.log("Go!");
}
rest(10);