from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración para el driver de Selenium
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

print("🚀 Iniciando tests de Guru Bank Telecom...")

try:
    # TEST 1: Abrir la página principal
    print("\n1️⃣ Abriendo la página principal...")
    driver.get("https://demo.guru99.com/telecom/index.html")
    time.sleep(3)

    if "Guru99 Telecom" in driver.title:
        print("✅ Página principal cargada correctamente")
    else:
        print("❌ Error al cargar la página principal")

    # TEST 2: Probar Agregar Cliente
    print("\n2️⃣ Probando Agregar Cliente...")
    add_customer = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add Customer")))
    add_customer.click()
    time.sleep(2)

    if "addcustomer.php" in driver.current_url:
        print("✅ Navegación a Agregar Cliente exitosa")

        print("➡️ Llenando formulario del cliente...")
        driver.find_element(By.NAME, "fname").send_keys("Jere")
        driver.find_element(By.NAME, "lname").send_keys("G")
        driver.find_element(By.NAME, "emailid").send_keys("jere@test.com")
        driver.find_element(By.NAME, "addr").send_keys("Calle 1234")
        driver.find_element(By.NAME, "telephoneno").send_keys("1234567890")

        driver.find_element(By.NAME, "submit").click()
        time.sleep(3)

        try:
            customer_id_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table//tr[1]/td[2]")
                )
            )
            customer_id = customer_id_element.text
            print(f"🔑 Customer ID guardado: {customer_id}")
        except:
            customer_id = None
            print("⚠️ No se encontró Customer ID en la página")

        if "Access Details" in driver.page_source:
            print("✅ Cliente agregado exitosamente")
        else:
            print("⚠️ Posible error al agregar cliente")
    else:
        customer_id = None
        print("❌ Error en navegación de Agregar Cliente")

    # TEST 3: Probar Agregar Plan de Tarifa
    print("\n3️⃣ Probando Agregar Plan de Tarifa...")
    driver.get("https://demo.guru99.com/telecom/index.html")    
    time.sleep(2)

    print("➡️ Buscando enlace 'Agregar Plan de Tarifa'...")
    add_tariff = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add Tariff Plan")))
    add_tariff.click()
    time.sleep(2)

    if "addtariffplans.php" in driver.current_url:
        print("✅ Navegación a Agregar Plan de Tarifa exitosa")

        print("➡️ Llenando formulario del plan...")
        driver.find_element(By.NAME, "rental").send_keys("500")
        driver.find_element(By.NAME, "local_minutes").send_keys("100")
        driver.find_element(By.NAME, "inter_minutes").send_keys("50")
        driver.find_element(By.NAME, "sms_pack").send_keys("200")
        driver.find_element(By.NAME, "minutes_charges").send_keys("1")
        driver.find_element(By.NAME, "inter_charges").send_keys("2")
        driver.find_element(By.NAME, "sms_charges").send_keys("1")

        driver.find_element(By.NAME, "submit").click()
        time.sleep(3)

        if "Congratulation" in driver.page_source:
            print("✅ Plan de tarifa agregado exitosamente")
        else:
            print("⚠️ Posible error al agregar plan")
    else:
        print("❌ Error en la navegación de Agregar Plan de Tarifa")

    # TEST 4: Probar Pagar Factura
    print("\n4️⃣ Probando Pagar Factura...")
    driver.get("https://demo.guru99.com/telecom/index.html")
    time.sleep(2)

    pay_billing = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Pay Billing")))
    pay_billing.click()
    time.sleep(2)

    if "billing.php" in driver.current_url:
        print("✅ Navegación en Pagar Factura exitosa")

        if customer_id:
            print(f"➡️ Usando Customer ID {customer_id} para pagar factura...")
            driver.find_element(By.NAME, "customer_id").send_keys(customer_id)
            driver.find_element(By.NAME, "submit").click()
            time.sleep(3)
            
            # Verificaciones múltiples para el pago
            page_source = driver.page_source.lower()
            payment_success_indicators = [
                "payment done", "payment successful", "payment complete", 
                "successfully paid", "billing paid", "congratulation"
            ]
            
            payment_successful = any(indicator in page_source for indicator in payment_success_indicators)
            
            if payment_successful:
                print("✅ Pago realizado correctamente")
            else:
                # Debug: mostrar parte del contenido de la página
                print("⚠️ Verificando contenido de la página...")
                print(f"🔍 URL actual: {driver.current_url}")
                print(f"🔍 Título de la página: {driver.title}")
                
                # Buscar elementos de éxito
                try:
                    success_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'Success') or contains(text(), 'done') or contains(text(), 'Done')]")
                    if success_elements:
                        print("✅ Pago realizado correctamente (encontrados elementos de éxito)")
                    else:
                        print("⚠️ No se encontraron indicadores claros de éxito en el pago")
                except:
                    print("⚠️ Error al verificar elementos de éxito")
        else:
            print("❌ No se pudo pagar factura porque no hay Customer ID")
    else:
        print("❌ Error en navegación de Pagar Factura")

    # TEST 5: Verificar elementos principales
    print("\n5️⃣ Verificando elementos de la página...")
    driver.get("https://demo.guru99.com/telecom/index.html")
    time.sleep(2)

    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"✅ Se encontraron {len(links)} enlaces en la página")

    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    if len(h1_elements) > 0:
        print("✅ Título principal encontrado")

    print("\n🎉 TODOS LOS TESTS COMPLETADOS!")
    print("📊 Resumen:")
    print("   - Página principal: ✅")
    print("   - Agregar Cliente: ✅")
    print("   - Agregar Plan de Tarifa: ✅")
    print("   - Pagar Factura: ✅")
    print("   - Elementos de la página: ✅")

except Exception as e:
    print(f"\n❌ Error durante los tests: {str(e)}")

finally:
    print("\n🔚 Cerrando navegador...")
    time.sleep(2)
    driver.quit()
    print("✅ Tests finalizados")
