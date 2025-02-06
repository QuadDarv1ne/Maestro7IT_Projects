#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

class Student {
public:
    double money;
    int satiety;
    int sleep;
    int mood;
    int study_progress;
    int days_left;

    Student() {
        money = 4000;
        satiety = 100;
        sleep = 100;
        mood = 100;
        study_progress = 50;
        days_left = 365;
    }

    void showStatus() {
        std::cout << "\nСтатус студента:" << std::endl;
        std::cout << "Деньги: " << money << " руб" << std::endl;
        std::cout << "Сытость: " << satiety << "%" << std::endl;
        std::cout << "Сон: " << sleep << "%" << std::endl;
        std::cout << "Настроение: " << mood << "%" << std::endl;
        std::cout << "Успеваемость: " << study_progress << "%" << std::endl;
        std::cout << "Дней до конца курса: " << days_left << "\n" << std::endl;
    }

    void study() {
        std::cout << "Вы занимаетесь учебой..." << std::endl;
        study_progress += 10;
        mood -= 10;
        sleep -= 10;
        satiety -= 5;
    }

    void work() {
        std::cout << "Вы пошли работать..." << std::endl;
        money += 500;
        mood -= 10;
        sleep -= 15;
        satiety -= 10;
    }

    void eat() {
        std::cout << "Вы поели..." << std::endl;
        money -= 200;
        satiety = 100;
    }

    void sleepAction() {
        std::cout << "Вы поспали..." << std::endl;
        sleep = 100;
        mood += 10;
    }

    void relax() {
        std::cout << "Вы отдыхаете..." << std::endl;
        mood = 100;
        sleep += 10;
        satiety -= 5;
    }

    bool isAlive() {
        return (satiety > 0 && sleep > 0 && study_progress > 0);
    }
};

int main() {
    setlocale(LC_ALL, "ru");
    srand(time(0));
    Student player;
    std::cout << "Добро пожаловать в Симулятор Студента!" << std::endl;

    while (player.days_left > 0 && player.isAlive()) {
        std::cout << "\nДень " << (366 - player.days_left) << ":" << std::endl;
        for (int i = 0; i < 2; i++) { // Два действия в день
            player.showStatus();
            std::cout << "Выберите действие:\n1 - Учеба\n2 - Работа\n3 - Покушать\n4 - Поспать\n5 - Отдыхать\nВаш выбор: ";
            int choice;
            std::cin >> choice;
            
            switch (choice) {
                case 1: player.study(); break;
                case 2: player.work(); break;
                case 3: player.eat(); break;
                case 4: player.sleepAction(); break;
                case 5: player.relax(); break;
                default: std::cout << "Неверный выбор!" << std::endl;
            }
            
            if (!player.isAlive()) {
                std::cout << "Вы не смогли продолжить обучение. Игра окончена." << std::endl;
                return 0;
            }
        }
        player.days_left--;
    }

    if (player.study_progress >= 100) {
        std::cout << "Поздравляем! Вы успешно завершили учебу!" << std::endl;
    }
    return 0;
}
