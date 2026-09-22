import sys
import pytest
from src.toolkit.__main__ import main


# 1. Тест проверяет, что при --help программа выходит с кодом 0
def test_cli_help(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["__main__.py", "--help"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0


# 2. Тест проверяет, что при любой ошибке (например, деление на 0)
# ошибка будет перехватываться в __main__.py
def test_cli_error_handling(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["__main__.py", "calc", "5 / 0"])
    with pytest.raises(ValueError, match="Деление на 0 недопустимо"):
        main()

# 3. Проверка работы CLI при работе calc и правильный вывод
def test_cli_correct_answer(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['__main__.py', 'calc', '2+3/3*5+1'])
    main()
    answer = capsys.readouterr()
    assert answer.out.strip() == '8'
