# cerebro
Написать программу по поиску потенциальных директорий установки приложения по его названию locate_app.py, предназначенную для запуска из командной строки. Единственным входным аргументом является искомое название.
Пример вызова: python locate_app.py photoshop

Поиск происходит по:
стандартным каталогам установки ("Program Files", "Program Files (x86)") на всех доступных дисках.
реестру windows (список установленных программ находится по пути HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall). Ключ для сравнения: DisplayName.

Критерий равенства: регистронезависимое вхождение.
Предполагается функционирование на ОС Windows.
