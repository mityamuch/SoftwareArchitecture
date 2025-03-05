workspace {
    name "Budgeting System"
    !identifiers hierarchical

    model {
        user = person "Пользователь"

        budgetSystem = softwareSystem "Система Бюджетирования" {
            description "Приложение для управления планируемыми доходами и расходами."\

            userService = container "User Service" {
                technology "Python / FastAPI"
                description "Сервис для управления пользователями."
            }

            incomeService = container "Income Service" {
                technology "Python / FastAPI"
                description "Сервис для управления доходами."
            }

            expenseService = container "Expense Service" {
                technology "Python / FastAPI"
                description "Сервис для управления расходами."
            }

            budgetCalculationService = container "Budget Calculation Service" {
                technology "Python / FastAPI"
                description "Сервис для расчета динамики бюджета."
            }

            userDatabase = container "User Database" {
                technology "PostgreSQL"
                description "База данных для хранения информации о пользователях."
            }

            incomeDatabase = container "Income Database" {
                technology "MongoDB"
                description "База данных для хранения информации о доходах."
            }

            expenseDatabase = container "Expense Database" {
                technology "MongoDB"
                description "База данных для хранения информации о расходах."
            }

            user -> budgetSystem "Хочет управалять своими финансами"

            // Взаимодействие
            user -> userService "Запрашивает создание пользователя" "REST"
            userService -> userDatabase "Сохраняет информацию о пользователе" "JDBC"
            
            user -> incomeService "Запрашивает создание планируемого дохода" "REST"
            incomeService -> incomeDatabase "Сохраняет информацию о доходах" "MongoDB"
            
            user -> expenseService "Запрашивает создание планируемого расхода" "REST"
            expenseService -> expenseDatabase "Сохраняет информацию о расходах" "MongoDB"
            
            userService -> incomeService "Запрашивает перечень планируемых доходов" "REST"
            incomeService -> incomeDatabase "Получает перечень доходов" "MongoDB"
            
            userService -> expenseService "Запрашивает перечень планируемых расходов" "REST"
            expenseService -> expenseDatabase "Получает перечень расходов" "MongoDB"
            
            user -> budgetCalculationService "Запрашивает расчет динамики бюджета" "REST"
            budgetCalculationService -> incomeDatabase "Читает данные для расчета" "MongoDB"
            budgetCalculationService -> expenseDatabase "Читает данные для расчета" "MongoDB"
        }
    }

    views {
        themes default

        // Диаграмма System Context
        systemContext budgetSystem {
            include *
            autolayout lr
        }

        // Диаграмма Container
        container budgetSystem {
            include *
            autolayout lr
        }

        // Диаграмма Dynamic (Создание нового пользователя)
        dynamic budgetSystem "create_new_user" "Создание нового пользователя" {
            autoLayout lr
            user -> budgetSystem.userService "Отправляет запрос на создание нового пользователя"
            budgetSystem.userService -> budgetSystem.userDatabase "Сохраняет данные"
            budgetSystem.userService -> user "Отправляет ответ о регистрации"
        }

        // Диаграмма Dynamic (Создание дохода)
        dynamic budgetSystem "create_income" "Создание планируемого дохода" {
            autoLayout lr
            user -> budgetSystem.incomeService "Отправляет запрос на создание дохода"
            budgetSystem.incomeService -> budgetSystem.incomeDatabase "Сохраняет информацию о доходе"
            budgetSystem.incomeService -> user "Отправляет подтверждение"
        }

        // Диаграмма Dynamic (Создание расхода)
        dynamic budgetSystem "create_expense" "Создание планируемого расхода" {
            autoLayout lr
            user -> budgetSystem.expenseService "Отправляет запрос на создание расхода"
            budgetSystem.expenseService -> budgetSystem.expenseDatabase "Сохраняет информацию о расходе"
            budgetSystem.expenseService -> user "Отправляет подтверждение"
        }

        // Диаграмма Dynamic (Поиск пользователя по логину)
        dynamic budgetSystem "search_user_by_login" "Поиск пользователя по логину" {
            autoLayout lr
            user -> budgetSystem.userService "Запрашивает поиск по логину"
            budgetSystem.userService -> budgetSystem.userDatabase "Получает данные пользователя"
            budgetSystem.userService -> user "Отправляет данные"
        }

        // Диаграмма Dynamic (Поиск пользователя по имени и фамилии)
        dynamic budgetSystem "search_user_by_name" "Поиск пользователя по имени и фамилии" {
            autoLayout lr
            user -> budgetSystem.userService "Запрашивает поиск по имени и фамилии"
            budgetSystem.userService -> budgetSystem.userDatabase "Получает данные пользователя"
            budgetSystem.userService -> user "Отправляет данные"
        }

        // Диаграмма Dynamic (Получение перечня доходов)
        dynamic budgetSystem "get_expenses" "Получение перечня планируемых расходов" {
            autoLayout lr
            user -> budgetSystem.expenseService "Запрашивает перечень расходов"
            budgetSystem.expenseService -> budgetSystem.expenseDatabase "Получает перечень расходов"
            budgetSystem.expenseService -> user "Отправляет данные"
        }

        // Диаграмма Dynamic (Расчет динамики бюджета)
        dynamic budgetSystem "calculate_budget" "Расчет динамики бюджета" {
            autoLayout lr
            user -> budgetSystem.budgetCalculationService "Запрашивает расчет динамики бюджета"
            budgetSystem.budgetCalculationService -> budgetSystem.incomeDatabase "Читает данные для расчета"
            budgetSystem.budgetCalculationService -> budgetSystem.expenseDatabase "Читает данные для расчета"
            budgetSystem.budgetCalculationService -> user "Отправляет расчет"
        }
    }
}
