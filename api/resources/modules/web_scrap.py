import asyncio
import math
import re
import threading
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from resources.modules.save_info import save_info


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(options=options)


def wait_for_element(driver, by, value):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))


def scrape_process(driver, process_link):
    wait_for_element(driver, By.CLASS_NAME, 'detalle')
    detalle = process_link.find_element(By.CLASS_NAME, 'detalle')
    detalle.find_element(By.TAG_NAME, 'a').click()

    wait_for_element(driver, By.CLASS_NAME, 'lista-movimiento-individual')
    wait_for_element(driver, By.CLASS_NAME, 'lista-movimiento')
    wait_for_element(driver, By.CLASS_NAME, 'filtros-busqueda')
    movimientos = []
    retry_element(driver, By.CSS_SELECTOR, '.filtros-busqueda > div:nth-of-type(2) > span:nth-of-type(1)', 5)
    fecha_ingreso = get_element_with_retry(driver=driver, by=By.CSS_SELECTOR,
                                           element=".filtros-busqueda > div > span:nth-of-type(2)",
                                           retries=5)

    details = {
        "fecha_ingreso": datetime.strptime(fecha_ingreso, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S'),
        "materia": get_element_with_retry(driver=driver, by=By.CSS_SELECTOR, element=".filtros-busqueda > div:nth-of-type(2) > span:nth-of-type(1)", retries=5),
        "tipo_accion": get_element_with_retry(driver=driver, by=By.CSS_SELECTOR, element=".filtros-busqueda > div:nth-of-type(2) > span:nth-of-type(2)", retries=5),
        "asunto": get_element_with_retry(driver=driver, by=By.CSS_SELECTOR, element=".filtros-busqueda > div:nth-of-type(3) > span:nth-of-type(1)", retries=5),
        #"tipo_ingreso": root_page.select_one(".filtros-busqueda > div:nth-of-type(4) > span:nth-of-type(1)").text,
        #"no_proceso_vinculado": root_page.select_one(".filtros-busqueda > div:nth-of-type(4) > span:nth-of-type(2)").text
    }

    retry_element(driver, By.CLASS_NAME, 'numero-incidente', 5)
    retry_element(driver, By.CLASS_NAME, 'lista-movimiento-individual', 5)
    action_links = driver.find_elements(By.CLASS_NAME, 'lista-movimiento-individual')

    for i in range(len(action_links)):
        action_link = action_links[i]
        movimiento_individual_payload = {
            "numero_incidente": action_link.find_element(By.CLASS_NAME, "numero-incidente").text,
            "ofendidos": action_link.find_element(By.CLASS_NAME, "lista-actores").text,
            "demandados": action_link.find_element(By.CLASS_NAME, "lista-demandados").text,
            "juditial_actions_info": scrape_judicial_actions(driver, action_link),
        }
        movimientos.append(movimiento_individual_payload)
        retry_element(driver, By.CLASS_NAME, 'numero-incidente', 5)
        action_links = driver.find_elements(By.CLASS_NAME, 'lista-movimiento-individual')

    driver.back()
    wait_for_element(driver, By.CLASS_NAME, 'causa-individual')
    details["movimientos"] = movimientos
    return details


def return_page(driver):
    details_html = driver.page_source
    details_soup = BeautifulSoup(details_html, 'html.parser')
    return details_soup


def scrape_judicial_actions(driver, action_link):
    wait_for_element(driver, By.CLASS_NAME, 'actuaciones-judiciales')
    action_link.find_element(By.CLASS_NAME, 'actuaciones-judiciales').find_element(By.TAG_NAME, 'a').click()
    wait_for_element(driver, By.CLASS_NAME, 'mat-expansion-panel')
    root_page = return_page(driver)
    retry_element(driver, By.CSS_SELECTOR, ".filtros-busqueda > div:nth-of-type(3) > span:nth-of-type(2)", 5)

    fecha_ingreso = get_element_with_retry(driver=driver, by=By.CSS_SELECTOR,
                                           element=".filtros-busqueda > div > span:nth-of-type(2)",
                                           retries=5)
    details = {
        "judicatura": root_page.select_one(".filtros-busqueda > div:nth-of-type(3) > span:nth-of-type(2)").text,
        "fecha": datetime.strptime(fecha_ingreso, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    }

    actuaciones = driver.find_elements(By.CLASS_NAME, 'mat-expansion-panel')
    actuaciones_list = []
    for actuacion in actuaciones:
        fecha = actuacion.find_element(By.CSS_SELECTOR, ".cabecera-tabla span:nth-child(1)").text
        actuacion_payload = {
            "fecha_ingreso": datetime.strptime(fecha, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S'),
            "detalle": actuacion.find_element(By.CSS_SELECTOR, ".cabecera-tabla span:nth-child(2)").text
        }
        actuaciones_list.append(actuacion_payload)

    driver.back()
    wait_for_element(driver, By.CLASS_NAME, 'lista-movimiento-individual')
    details["actuaciones"] = actuaciones_list
    return details


async def process_links_batches(driver, process_links, query_type, person_id):
    causas_individuales = []

    for i in range(len(process_links)):
        process_links = driver.find_elements(By.CLASS_NAME, 'causa-individual')
        process_link = process_links[i]

        causa_individual_payload = {
            "id_info": process_link.find_element(By.CLASS_NAME, "id").text,
            "num_proceso": process_link.find_element(By.CLASS_NAME, "numero-proceso").text,
            "accion": process_link.find_element(By.CLASS_NAME, "accion-infraccion").text,
            "process_link_info": scrape_process(driver, process_link),
            "tipo_proceso": query_type
        }
        causas_individuales.append(causa_individual_payload)

    return causas_individuales


async def scrape_page(page, input, person_id, query_type=None):
    try:
        driver = setup_driver()
        load_page(driver, person_id, input, 5)

        wait_for_element(driver, By.CLASS_NAME, 'causa-individual')

        for j in range(page):
            next_button = wait_for_element(driver, By.CLASS_NAME, 'mat-mdc-paginator-navigation-next')
            next_button.click()
            time.sleep(0.5)

        wait_for_element(driver, By.CLASS_NAME, 'causa-individual')

        process_links = driver.find_elements(By.CLASS_NAME, 'causa-individual')
        process_links_results = await process_links_batches(driver, process_links, query_type, person_id)
        driver.quit()
        print(f'finishing page {page}')
        return process_links_results
    except Exception as e:
        return []


def retry_element(driver, by, element, retries):

    for j in range(retries):
        try:
            wait_for_element(driver, by, element)
            break
        except Exception as e:
            driver.refresh()


def get_element_with_retry(driver, by, element, retries):
    retry_element(driver, by, element, retries)
    root_page = return_page(driver)
    return root_page.select_one(element).text


def load_page(driver, person_id, input, retries):
    driver.get('https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros')
    form = wait_for_element(driver, By.TAG_NAME, 'form')
    input_element = form.find_element(By.XPATH, input)
    submit_button = form.find_element(By.XPATH,
                                      '/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[6]/button[1]')

    input_element.send_keys(person_id)
    submit_button.click()

    retry_element(driver, By.CLASS_NAME, 'mat-mdc-paginator-navigation-next', retries)


def run_scraping(page, input, person_id, query_type):
    return asyncio.run(scrape_page(page, input, person_id, query_type))


async def calculate_pages(driver):
    pages_quantity = driver.find_element(By.CLASS_NAME, 'cantidadMovimiento').text
    pages_quantity = int(re.search(r'\d+', pages_quantity).group())
    pages_quantity = math.ceil(pages_quantity / 10)
    return pages_quantity


async def generate_pages_threads(input, person_id, query_type, save):
    try:
        driver = setup_driver()
        load_page(driver, person_id, input, 5)
        wait_for_element(driver, By.CLASS_NAME, 'cantidadMovimiento')

        pages_quantity = await calculate_pages(driver)
        driver.quit()

        queries = [(page, input, person_id, query_type) for page in range(pages_quantity)]

        results = []
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor(max_workers=17) as executor:
            tasks = [loop.run_in_executor(executor, run_scraping, *query) for query in queries]
            results.append(await asyncio.gather(*tasks))

        if save:
            for result in results:
                for batch in result:
                    if not batch:
                        continue
                    await save_info(batch, person_id)

        await asyncio.sleep(5)
        return results
    except Exception as e:
        return


async def execute_test_case():
    '''inputs =[('/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[2]/mat-form-field[1]/div[1]/div/div[2]/input', 'demandante'),
             ('/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[3]/mat-form-field[1]/div[1]/div/div[2]/input', 'demandado')]
'''
    inputs = [('/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[2]/mat-form-field[1]/div[1]/div/div[2]/input',
              'demandante')]
    queries = ['0968599020001']

    for query in queries:
        for input in inputs:
            start_time = time.time()

            await generate_pages_threads(input[0], query, input[1], True)

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")


async def fill_information(persona_ids):
    print('la informacion esta siendo procesada y guarda en base de datos, esperar un momento hasta que termine')
    inputs = [(
              '/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[2]/mat-form-field[1]/div[1]/div/div[2]/input',
              'demandante'),
              (
              '/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[3]/mat-form-field[1]/div[1]/div/div[2]/input',
              'demandado')]
    '''inputs = [('/html/body/app-root/app-expel-filtros-busqueda/expel-sidenav/mat-sidenav-container/mat-sidenav-content/section/form/div[2]/mat-form-field[1]/div[1]/div/div[2]/input',
              'demandante')]'''

    queries = persona_ids

    for query in queries:
        for input in inputs:
            start_time = time.time()
            await generate_pages_threads(input[0], query, input[1], True)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")

    print('La informacion ha sido completamente guardada en base de datos')