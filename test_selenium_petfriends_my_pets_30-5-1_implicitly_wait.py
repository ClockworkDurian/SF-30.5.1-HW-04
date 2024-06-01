import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # добавляем неявное ожидание в 10 секунд
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('vasya@bk.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345678_$')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # time.sleep(5)
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Переходим на страницу "мои питомцы"
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    yield driver

    driver.quit()


# 1. Присутствуют все питомцы
def test_30_3_1_1(driver):
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    pet_qty = driver.find_element(By.CLASS_NAME, 'task3').text.split('\n')[1].split(' ')[-1]
    for i in range(len(pets_count)):
        if len(pets_count) > i:
            assert len(pets_count) == int(pet_qty)


# 2. Хотя бы у половины питомцев есть фото
def test_30_3_1_2(driver):
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    # Находим питомцев у которых есть фото
    image_count = driver.find_elements(By.XPATH, '//img[starts-with(@src, "data:image/")]')
    # Проверяем, что хотя бы у половины питомцев есть фото:
    assert len(image_count) >= len(pets_count) / 2


# 3. У всех питомцев есть имя, возраст и порода
def test_30_3_1_3(driver):
    # Находим все элементы, содержащие имена питомцев
    names = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[1]")

    # Находим все элементы, содержащие породы питомцев
    breeds = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[2]")

    # Находим все элементы, содержащие возраст питомцев
    ages = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[3]")

    # Проверяем, что количество элементов, содержащих имена, породы и возраст, равно между собой
    assert len(names) == len(breeds) == len(ages)

    # Проверяем, что у каждого питомца есть имя, порода и возраст
    for i in range(len(names)):
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''


# 4. У всех питомцев разные имена.
def test_30_3_1_4(driver):
    names = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[1]")
    list_names = [name.text for name in names]  # имена в списке

    # Проверка уникальности имен
    unique_names = set(list_names)
    assert len(unique_names) == len(list_names)


# 5. В списке нет повторяющихся питомцев.
def test_30_3_1_5(driver):
    # Переходим на страницу "мои питомцы"
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Находим все элементы, содержащие имена питомцев
    names = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[1]")

    # Находим все элементы, содержащие породы питомцев
    breeds = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[2]")

    # Находим все элементы, содержащие возраст питомцев
    ages = driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[3]")

    # Создаем список кортежей, содержащих имя, породу и возраст каждого питомца
    pets = [(name.text, breed.text, age.text) for name, breed, age in zip(names, breeds, ages)]

    # Преобразуем список кортежей в множество, чтобы удалить дубликаты
    pets_set = set(pets)

    # Проверяем, что количество элементов в множестве равно количеству элементов в списке
    assert len(pets_set) == len(pets)