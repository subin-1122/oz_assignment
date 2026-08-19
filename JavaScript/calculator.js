const display = document.getElementById('display');
let currentFormula = "";
let isPowerOn = true;
let isCalculated = false;

// 초기 상태 설정
window.onload = function() {
    const onOffBtn = document.querySelector('.on-off');
    onOffBtn.classList.add('on');
};

function togglePower() {
    isPowerOn = !isPowerOn;
    const buttons = document.querySelectorAll('button:not(.on-off)');
    const onOffBtn = document.querySelector('.on-off');

    if (isPowerOn) {
        display.value = "0";
        display.style.backgroundColor = "#222";
        onOffBtn.classList.add('on');
        buttons.forEach(btn => btn.disabled = false);
    } else {
        display.value = "";
        display.style.backgroundColor = "#111";
        onOffBtn.classList.remove('on');
        buttons.forEach(btn => btn.disabled = true);
        currentFormula = "";
        isCalculated = false;
    }
}

function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    return a / b;
}

function appendNumber(number) {
    if (!isPowerOn) return;
    
    // 계산 완료 상태에서 숫자를 누르면 새 수식 시작
    if (isCalculated) {
        display.value = "";
        currentFormula = "";
        isCalculated = false;
    }

    if (display.value === "0" || display.value === "Error" || display.value === "DivBy0") {
        display.value = number;
        currentFormula = number;
    } else {
        display.value += number;
        currentFormula += number;
    }
}

function appendOperator(operator) {
    if (!isPowerOn) return;
    if (display.value === "Error" || display.value === "DivBy0") return;
    
    // 계산 직후 연산자를 누르면 결과값에 이어서 계산
    if (isCalculated) {
        isCalculated = false;
    }

    // 수식이 비어있으면 0부터 시작하게 처리
    if (currentFormula === "") {
        currentFormula = "0";
    }

    // 마지막 입력이 공백이면 연산자가 이미 있는 것이므로 교체
    if (currentFormula.endsWith(" ")) {
        currentFormula = currentFormula.slice(0, -3);
    }
    
    currentFormula += " " + operator + " ";
    display.value = currentFormula;
}

function clearDisplay() {
    if (!isPowerOn) return;
    display.value = "0";
    currentFormula = "";
    isCalculated = false;
}

function calculate(formula) {
    const tokens = formula.trim().split(/\s+/);
    if (tokens.length < 3 || tokens.length % 2 === 0) {
        return "Error";
    }

    // 1단계: 곱셈과 나눗셈 먼저 처리
    const intermediateTokens = [];
    let i = 0;
    while (i < tokens.length) {
        const token = tokens[i];
        if (token === "*" || token === "/") {
            const left = Number(intermediateTokens.pop());
            const operator = token;
            const right = Number(tokens[i + 1]);

            if (isNaN(left) || isNaN(right)) return "Error";

            let res;
            if (operator === "*") {
                res = multiply(left, right);
            } else {
                if (right === 0) return "DivBy0";
                res = divide(left, right);
            }
            intermediateTokens.push(res);
            i += 2;
        } else {
            intermediateTokens.push(token);
            i++;
        }
    }

    // 2단계: 덧셈과 뺄셈 처리
    let result = Number(intermediateTokens[0]);
    if (isNaN(result)) return "Error";

    for (let j = 1; j < intermediateTokens.length; j += 2) {
        const operator = intermediateTokens[j];
        const nextValue = Number(intermediateTokens[j + 1]);

        if (isNaN(nextValue)) return "Error";

        if (operator === "+") {
            result = add(result, nextValue);
        } else if (operator === "-") {
            result = subtract(result, nextValue);
        } else {
            return "Error";
        }
    }
    return result;
}

function performCalculate() {
    if (!isPowerOn || !currentFormula) return;
    
    // 연산자로 끝나는 경우 마지막 연산자 제거 후 계산
    if (currentFormula.endsWith(" ")) {
        currentFormula = currentFormula.trim();
    }

    const result = calculate(currentFormula);
    display.value = result;
    isCalculated = true;
    
    if (result === "Error" || result === "DivBy0") {
        currentFormula = "";
    } else {
        currentFormula = result.toString();
    }
}