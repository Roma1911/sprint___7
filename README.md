

Запустить тесты с отчётом Allure

    pytest tests/test_courier_login.py --alluredir=./allure-results
    allure serve ./allure-results

    pytest tests/test_creating_an_order.py --alluredir=./allure-results
    allure serve ./allure-results

    pytest tests/test_creating_courier.py --alluredir=./allure-results
    allure serve ./allure-results

    pytest tests/test_list_of_orders.py --alluredir=./allure-results
    allure serve ./allure-results
    
Запустить конкретный тест

    pytest tests/test_courier_login.py::TestCourierLogin::test_courier_can_login -v
    
    pytest tests/test_creating_an_order.py::TestOrder::test_create_order -v

    pytest tests/creating_courier.py::TestCourierCreation::test_courier_can_be_created -v
    
    pytest tests/list_of_orders.py::test_get_orders_returns_list -v
