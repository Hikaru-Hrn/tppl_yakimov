import sys
import pytest
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
    main()
    assert "Вы забыли передать выражение." in capsys.readouterr().out

    # Нормальный запуск
    monkeypatch.setattr(sys, "argv", ["main.py", "2 3 +"])
    main()
    assert "2 3 + = 5" in capsys.readouterr().out

    # Запуск с ошибкой (деление на 0)
    monkeypatch.setattr(sys, "argv", ["main.py", "2 0 /"])
    main()
    assert "Ой, ошибка:" in capsys.readouterr().out