import sys
import pytest
import os
from main import calculate, main


def test_examples():
    assert calculate("3 0 4 ~ 2 ~") == 47
    assert calculate("2 2 + 4 - 4 ~ 2 3 * +") == 22


def test_operations():
    assert calculate("5 3 +") == 8
    assert calculate("5 3 -") == 2
    assert calculate("5 3 *") == 15
    assert calculate("6 3 /") == 2
    assert calculate("5 2 /") == 2.5
    assert calculate("1.5 2.5 +") == 4.0


def test_tilde():
    assert calculate("3 10 ~") == 7
    assert calculate("1 2 0 3 ~") == 36  # (1 + 2 + 0 + 3)^2


def test_errors():
    with pytest.raises(ValueError):
        calculate("")
    with pytest.raises(ValueError):
        calculate("5 +")
    with pytest.raises(ValueError):
        calculate("5 abc +")
    with pytest.raises(ValueError):
        calculate("5 5 5 +")
    with pytest.raises(ZeroDivisionError):
        calculate("5 0 /")


def test_main(monkeypatch, capsys):
    # Запуск без аргументов
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "Вы забыли передать выражение." in (captured.out + captured.err)

    # Нормальный запуск в кавычках
    monkeypatch.setattr(sys, "argv", ["main.py", "2 3 +"])
    main()
    assert "2 3 + = 5" in capsys.readouterr().out

    # Имитация запуска `python3 main.py 2 3 ~` без кавычек в терминале
    # Оболочка заменяет ~ на путь к домашней директории до запуска скрипта
    home_dir = os.path.expanduser("~")
    monkeypatch.setattr(sys, "argv", ["main.py", "2", "3", home_dir])
    main()
    assert "2 3 ~ = 1" in capsys.readouterr().out

    # Запуск с ошибкой (деление на 0)
    monkeypatch.setattr(sys, "argv", ["main.py", "2 0 /"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "Ой, ошибка:" in (captured.out + captured.err)