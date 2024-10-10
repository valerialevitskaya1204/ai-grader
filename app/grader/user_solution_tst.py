import logging
import unittest
from typing import List, Dict, Tuple


FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(
    filename='logs_tests.log',  
    level=logging.INFO, 
    format=FORMAT
    )
logger = logging.getLogger(__name__)


class UserSolutionTest(unittest.TestCase):
    def __init__(self, methodName: str, test_input: any, expected_output: any, user_solution: str):
        """
        Конструктор для класса тестов.

        :param methodName: Название метода тестирования (обычно передается 'runTest').
        :param test_input: Входные данные для теста.
        :param expected_output: Ожидаемый результат.
        :param user_solution: Пользовательское решение в виде строки кода.
        """
        super().__init__(methodName)
        self.test_input = test_input
        self.expected_output = expected_output
        self.user_solution = user_solution

    def runTest(self):
        result = None
        try:
            exec_globals = {'input_data': self.test_input}
            logger.info(self.user_solution)
            exec(self.user_solution, exec_globals)
            
            result = exec_globals.get('result', None)

            self.assertEqual(result, self.expected_output,
                             f"input: {self.test_input}, expected: {self.expected_output}, got: {result}")
            logger.info(f"Test passed: input={self.test_input}, output={result}")
        except AssertionError as e:
            logger.error(f"Test failed: input={self.test_input}, expected={self.expected_output}, got={result}")
            raise e  
        except Exception as e:
            logger.error(f"Test execution error: input={self.test_input}, error={str(e)}")
            raise e 

class TestUserSolution:
    def __init__(self, 
                 test_cases: List[Dict[str, any]], 
                 user_solution: str):
        """
        :param test_cases: Список из словарей с тестами (input) и ожидаемыми результатами (expected_output).
        :param user_solution: Пользовательское решение в виде строки с разделителями \n.
        """
        self.test_cases = test_cases
        self.user_solution = user_solution

    def run_tests_with_unittest(self) -> Tuple[List[str], bool]:
        """
        Функция для прогонки набора пользовательских решений через тесты с использованием unittest.

        :return: Список строк с результатами выполнения тестов.
        """
        results = []
        is_fail = True
        suite = unittest.TestSuite()

        for case in self.test_cases:
            test_input = case['input']
            expected_output = case['expected_output']

            logger.info(f"Running test with input: {test_input}")
            test = UserSolutionTest('runTest', test_input, expected_output, self.user_solution)
            suite.addTest(test)

        try:
            runner = unittest.TextTestRunner()
            result = runner.run(suite)
            
            if result.wasSuccessful():
                is_fail = False
            else:
                for failure in result.failures:
                    logger.error(f"Failure: {failure[1]}")
                    results.append(f"Failure: {failure[1]}")
                for error in result.errors:
                    logger.error(f"Error: {error[1]}")
                    results.append(f"Error: {error[1]}")
        except Exception as e:
            error_message = f"Unittest execution error: {str(e)}"
            logger.error(error_message)
            results.append(error_message)

        return results, is_fail


class TestExtractor:
    def __init__(self, sheet, task_id: int):
        """
        Инициализация класса для извлечения тестов.
        
        :param sheet: Лист с тестами.
        :param task_id: Идентификатор задачи.
        """
        self.sheet = sheet
        self.task_id = task_id

    def extract_tests(self) -> List[dict]:
        """
        Извлекает тесты для задачи из заданного листа.
        Каждый тест возвращается как словарь с 'input' и 'expected_output'.
        
        :return: Список тестов в виде словарей.
        """
        tests = []
        for row in self.sheet.iter_rows(min_row=1, max_row=self.sheet.max_row):
            task_name = row[0].value
            if task_name in [f"Задача № {self.task_id}", f"Задача №{self.task_id}"]:
                input_value = row[1].value
                expected_output = row[2].value
                if isinstance(expected_output, str):
                    if expected_output in ['True', 'False']:
                        expected_output = expected_output == 'True'
                    elif expected_output.isdigit():
                        expected_output = int(expected_output)
                tests.append({'input': input_value, 'expected_output': expected_output})
        return tests


