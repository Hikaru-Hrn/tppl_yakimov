import sys
import os


def calculate(expression):
    tokens = expression.split()
    if not tokens:
        raise ValueError("Пустое выражение! Пожалуйста, введите числа и операторы.")

    stack = []

    for token in tokens:
        if token in ("+", "-", "*", "/", "~"):
            if len(stack) < 2:
                raise ValueError(f"Для оператора '{token}' не хватает чисел в стеке. Проверьте выражение!")

            y = stack.pop()
            x = stack.pop()

            if token == "+":
                stack.append(x + y)
            elif token == "-":
                stack.append(x - y)
            elif token == "*":
                stack.append(x * y)
            elif token == "/":
                if y == 0:
                    raise ZeroDivisionError("На ноль делить нельзя!")
                res = x / y
                # Если поделилось без остатка, сохраняем как целое число
                stack.append(int(res) if res.is_integer() else res)
            elif token == "~":
                if x != 0 and y != 0:
                    stack.append(abs(x - y))
                else:
                    total = sum(stack) + x + y
                    stack.clear()
                    stack.append(total ** 2)
        else:
            # Пробуем превратить токен в целое или дробное число
            try:
                num = int(token)
            except ValueError:
                try:
                    num = float(token)
                except ValueError:
                    raise ValueError(f"Неизвестный символ: {token}. Используйте только числа и +, -, *, /, ~.")
            stack.append(num)

        print(f"Шаг '{token}': стек {stack}")

    if len(stack) != 1:
        raise ValueError(f"В стеке остались лишние числа: {stack}. Кажется, вы забыли оператор!")

    return stack[0]


def main():
    if len(sys.argv) < 2:
        print("Вы забыли передать выражение.", file=sys.stderr)
        print('Пример: python main.py "3 0 4 ~ 2 ~"', file=sys.stderr)
        sys.exit(1)  # Завершаем программу с кодом ошибки 1

    # Защита от раскрытия тильды при запуске без кавычек
    home_dir = os.path.expanduser("~")
    raw_args = ["~" if arg == home_dir else arg for arg in sys.argv[1:]]

    # Собираем аргументы в одну строку и убираем лишние пробелы
    expr = " ".join(raw_args)
    clean_expr = " ".join(expr.split())

    try:
        result = calculate(clean_expr)
        print(f"{clean_expr} = {result}")
    except Exception as e:
        print(f"Ой, ошибка: {e}", file=sys.stderr)
        sys.exit(1)  # 1 при любой ошибке вычисления


if __name__ == "__main__":
    main()