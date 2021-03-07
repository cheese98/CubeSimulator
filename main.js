const fs = require('fs');
const redJSON = JSON.parse(fs.readFileSync('./red_cube.json', 'utf8'));
const blackJSON = JSON.parse(fs.readFileSync('./black_cube.json', 'utf8'));
const addiJSON = JSON.parse(fs.readFileSync('./addi_cube.json', 'utf8'));

const equipList = ["무기", "엠블렘", "보조무기 (포스실드, 소울링 제외)", "포스실드, 소울링", "방패",
                   "모자", "상의", "한벌옷", "하의", "신발", "장갑", "망토", "벨트", "어깨장식",
                   "얼굴장식", "눈장식", "귀고리", "반지", "펜던트", "기계심장"]

/*
큐브 옵션을 돌리기 전 업그레이드 여부를 판단합니다.
cube: 큐브 종류 (레드=0, 블랙=1, 에디=2)
level: 현재 잠재등급 (레어=0, 에픽=1, 유니크=2)
*/
let upgrade_table = [[0.06, 0.018, 0.003], [0.15, 0.035, 0.01], [0.047619, 0.019608, 0.004975]];

function evaluate_upgrade(cube, level){
    if(level == 3) return false;
    let seed = Math.random();
    return seed < upgrade_table[cube][level];
}

function roll(table){
    let sum = 0;
    let seed = Math.random() * 100;
    for(let item in table){
        sum += table[item];
        if (seed <= sum) return item;
    }
    // 예외상황 발생시 마지막값 출력
    return Object.keys(table)[Object.keys(table).length - 1];
}

function evaluate_option(res){
    // 유효한 값이면 true, 유효하지 않은 값이면 false
    let counts = [0, 0, 0, 0, 0, 0, 0, 0];
    let options = ["모든 스킬레벨", "피격 후 무적시간", "몬스터 방어율 무시", "확률로 데미지의", "초간 무적", "보스 몬스터 공격", "아이템 드롭률"];

    for(let line of res){
        for(let i=0; i<7; i++){
            if(line.indexOf(options[i]) > -1) counts[i]++;
        }
    }
    // 1줄 제한 거름
    if(counts[0] > 1 || counts[1] > 1) return false;
    // 2줄 제한 거름
    for(let i=2;i<7;i++){
        if(counts[i] > 2) return false;
    }
    return true;
}

/*
큐브를 돌리는 함수입니다.
level: 현재 잠재등급
equip: 아이템 타입
*/
function red_cube(level, equip){
    let result = [];

    // 중복값이 없을 때까지 계속 돌립니다.
    do{
        result = [];
        result.push(roll(redJSON[equip*4 + level]["first"]));
        result.push(roll(redJSON[equip*4 + level]["second"]));
        result.push(roll(redJSON[equip*4 + level]["third"]));
    } while(!evaluate_option(result));

    return result;
}

function black_cube(level, equip){
    let result = [];

    // 중복값이 없을 때까지 계속 돌립니다.
    do{
        result = [];
        result.push(roll(blackJSON[equip*4 + level]["first"]));
        result.push(roll(blackJSON[equip*4 + level]["second"]));
        result.push(roll(blackJSON[equip*4 + level]["third"]));
    } while(!evaluate_option(result));

    return result;
}

function addi_cube(level, equip){
    let result = [];

    // 중복값이 없을 때까지 계속 돌립니다.
    do{
        result = [];
        result.push(roll(addiJSON[equip*4 + level]["first"]));
        result.push(roll(addiJSON[equip*4 + level]["second"]));
        result.push(roll(addiJSON[equip*4 + level]["third"]));
    } while(!evaluate_option(result));

    return result;
}

let potentialLevel = 3; // 레어=0, 에픽=1, 유니크=2, 레전드리=3
let equipType = "무기";


console.log(red_cube(potentialLevel, equipList.indexOf(equipType)));