import streamlit as st
import requests
from streamlit_ace import st_ace

API_URL = "http://localhost:8000"

default_code = """
#Пример того как должно выглядеть ваше решение
def solution(input_data):
    # Название функции может быть любым
    pass
    
result = solution(input_data) # обязательно добавьте эту строчку и не забудьте поменять название функции на вашу!
"""

def get_all_tasks():
    response = requests.get(f"{API_URL}/all_tasks/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Ошибка при получении списка задач")
        return []

def get_task(task_id):
    response = requests.get(f"{API_URL}/task/{task_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Ошибка при получении задачи")
        return None

def submit_solution(task_id, solution_code):
    data = {
        "task_id": task_id,
        "solution_code": solution_code
    }
    response = requests.post(f"{API_URL}/submit_solution/", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"{response}")
        return None

st.title(":blue[Задачи и решения]")

tasks = get_all_tasks()
if tasks:
    task_id = st.selectbox("Выберите задачу", tasks)
    
    task = get_task(task_id)
    if task:
        st.title(":blue[Условие задачи]")
        link = st.write(f"_Ссылка на задачу_: {task['link_to_task']}")
        formulation = st.write(task['formulation'])
        example_code = st.code(language='python', body=default_code)
        solution_code = st_ace(language='python', theme='monokai', height=300, value=task['example_code'])
        if st.button("Отправить решение"):
            result = submit_solution(task_id, "\n".join(solution_code.splitlines()))
            user_status = st.title(f":blue[Статус вашего решения]: {result['status']}")
            usr_sts = result["status"]
            if usr_sts == "passed":
                explanation = st.write(result['message'])
                title_user_code = st.title(":red[Ваш код]")
                user_code = st.code(language='python', body=result['user_code'])
                title_user_code = st.title(":green[Идеальное решение]")
                ideal_code = st.code(language='python', body=result['ideal_code'])
                recs = st.title(":blue[Рекомендации]")
            elif usr_sts == "failed":
                recs = st.title(":red[Ошибки]")
                explanation = st.write(result['message'])
                recs = st.title(":blue[Рекомендации]")
            else:
                explanation = st.write(result['message'])

