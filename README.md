# AI Python Grader

## Описание

AI Python Grader — это инструмент для автоматической оценки пользовательских решений на языке Python. 

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/valerialevitskaya1204/ai-grader.git

2. **Перейдите в директорию проекта**
   ```bash
   cd ai-grader
3. **Установите необходимые зависимости**
   ```bash
   poetry install
4. **Запустите API локально**:
   ```bash
   poetry run uvicorn app.main:app --reload
5. **Запустите приложение:**:
   ```bash
   streamlit run app/streamlit_interface.py

## Описание компонентов

- `app/`: Основной каталог приложения.
  - `app_streamlit.py`: Файл для запуска Streamlit интерфейса.
  - `data/`: Каталог с данными, включая задания и шаблоны.
     - `open_hidden.xlsx` - скрытые и открытые тесты для проверки пользовательского решения на соответствие эталонному
     - `tasks` - задания, эталонные решения для проверки
- `grader/`: Каталог для логики оценки пользовательских решений.
  - `user_solution_recs.py`: Рекомендации по решениям пользователей. (TBD)
  - `user_solution_tst.py`: Тесты для проверки пользовательских решений.
  - `main.py`: Основной файл API.


