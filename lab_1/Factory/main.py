import sys
import json
import os
from models.people import Worker, Customer
from models.tool import Tool
from models.material import Metal, Wood
from models.warehouse import Warehouse
from models.workshop import Workshop
from models.furniture import Furniture, FurnitureState
from operations.operations import (
    PreparationOperation, CreateElementOperation, AssemblyOperation,
    CheckOperation, PackingOperation
)
from models.exceptions import InvalidDataError, InvalidAmountError, InvalidOperation

SAVE_FILE = "factory_save.json"


def save_game(material_storage, finished_storage, workshop, workers, tools, customers, furnitures):
    data = {
        "material_storage": {
            "name": material_storage.name,
            "capacity": material_storage.capacity,
            "metal_amount": material_storage.metal_amount,
            "wood_amount": material_storage.wood_amount
        },
        "finished_storage": {
            "name": finished_storage.name,
            "capacity": finished_storage.capacity,
            "metal_amount": finished_storage.metal_amount,
            "wood_amount": finished_storage.wood_amount
        },
        "workshop": {
            "name": workshop.workshop_type,
            "completed": [f.type for f in workshop.completed_furnitures]
        },
        "workers": [
            {
                "name": w.name,
                "age": w.age,
                "specialization": w.specialization,
                "experience": w.experience,
                "is_busy": w.is_busy
            } for w in workers
        ],
        "tools": [
            {
                "name": t.name,
                "durability": t.durability
            } for t in tools
        ],
        "customers": [
            {
                "name": c.name,
                "age": c.age,
                "phone": c.phone
            } for c in customers
        ],
        "furnitures": [
            {
                "type": f.type,
                "customer": f.customer if hasattr(f, 'customer') else "",
                "status": f.status.value,
                "materials": [
                    {
                        "type": m.__class__.__name__,
                        "name": m.type if hasattr(m, 'type') else "",
                        "amount": m.amount
                    } for m in f.materials
                ]
            } for f in furnitures
        ]
    }
    
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(" Данные сохранены")


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    
    with open(SAVE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    material_storage = Warehouse(
        data["material_storage"]["name"],
        data["material_storage"]["capacity"]
    )
    material_storage.metal_amount = data["material_storage"]["metal_amount"]
    material_storage.wood_amount = data["material_storage"]["wood_amount"]
    
    finished_storage = Warehouse(
        data["finished_storage"]["name"],
        data["finished_storage"]["capacity"]
    )
    finished_storage.metal_amount = data["finished_storage"]["metal_amount"]
    finished_storage.wood_amount = data["finished_storage"]["wood_amount"]
    
    workshop = Workshop(data["workshop"]["name"])
    
    workers = []
    for w_data in data["workers"]:
        worker = Worker(
            w_data["name"],
            w_data["age"],
            w_data["specialization"],
            w_data["experience"]
        )
        worker.is_busy = w_data["is_busy"]
        workers.append(worker)
    
    tools = [Tool(t["name"], t["durability"]) for t in data["tools"]]
    
    customers = [Customer(c["name"], c["age"], c["phone"]) for c in data["customers"]]
    
    furnitures = []
    for f_data in data["furnitures"]:
        materials = []
        for m_data in f_data["materials"]:
            if m_data["type"] == "Metal":
                materials.append(Metal(m_data["name"], m_data["amount"]))
            elif m_data["type"] == "Wood":
                materials.append(Wood(m_data["name"], m_data["amount"]))
        
        furniture = Furniture(f_data["type"], materials)
        if f_data.get("customer"):
            furniture.customer = f_data["customer"]
        for state in FurnitureState:
            if state.value == f_data["status"]:
                furniture.status = state
                break
        
        furnitures.append(furniture)
    
    for f_type in data["workshop"]["completed"]:
        for f in furnitures:
            if f.type == f_type and f.status == FurnitureState.STORED:
                workshop.add_completed_furniture(f)
                break
    
    return material_storage, finished_storage, workshop, workers, tools, customers, furnitures


def show_banner():
    print("\n" + "=" * 50)
    print("      МЕБЕЛЬНАЯ ФАБРИКА")
    print("=" * 50)


def show_menu():
    print("\n1. Новый клиент и заказ")
    print("2. Произвести мебель")
    print("3. Посмотреть склад готовой продукции")
    print("4. Посмотреть всех клиентов")
    print("5. Посмотреть всех работников")
    print("6. Посмотреть все инструменты")
    print("7. Выход")
    print("-" * 30)


def initialize_system():
    storage = Warehouse("Склад материалов", 10000.0)
    workshop = Workshop("Сборочный цех")
    finished_goods = Warehouse("Склад готовой продукции", 5000.0)
    
    storage.metal_amount = 5000.0
    storage.wood_amount = 8000.0
    
    workers = [
        Worker("Иван Петров", 35, "универсал", 8),
        Worker("Анна Сидорова", 28, "столяр", 5),
        Worker("Петр Иванов", 42, "сборщик", 12),
        Worker("Мария Козлова", 30, "контролер", 6),
        Worker("Сергей Николаев", 38, "водитель", 10)
    ]
    
    tools = [
        Tool("Молоток", 100),
        Tool("Пила", 80),
        Tool("Шуруповерт", 90),
        Tool("Рубанок", 70),
        Tool("Кисть", 50)
    ]
    
    customers = []
    furnitures = []
    
    print("\nСистема запущена")
    print(f"Материалы на складе: металл {storage.metal_amount}, дерево {storage.wood_amount}")
    print(f"Рабочих: {len(workers)}, Инструментов: {len(tools)}")
    
    return storage, finished_goods, workshop, workers, tools, customers, furnitures


def main():
    loaded = load_game()
    
    if loaded:
        print("\n Найдено сохранение!")
        load_choice = input("Загрузить предыдущую сессию? (y/n): ").lower()
        if load_choice == 'y':
            material_storage, finished_storage, workshop, workers, tools, customers, furnitures = loaded
            print(" Данные загружены")
            print(f"Материалы на складе: металл {material_storage.metal_amount}, дерево {material_storage.wood_amount}")
            print(f"Готовой продукции: {len(workshop.completed_furnitures)}")
        else:
            material_storage, finished_storage, workshop, workers, tools, customers, furnitures = initialize_system()
    else:
        material_storage, finished_storage, workshop, workers, tools, customers, furnitures = initialize_system()
    
    show_banner()
    
    while True:
        show_menu()
        choice = input("Выберите действие > ")
        
        try:
            if choice == "7":
                save_game(material_storage, finished_storage, workshop, workers, tools, customers, furnitures)
                print("Состояние автоматически сохранено.")
                print("До свидания!")
                sys.exit()
            elif choice == "1":
                name = input("Имя клиента: ")
                phone = input("Телефон: ")
                customer = Customer(name, 30, phone)
                customers.append(customer)
                
                prod_type = input("Что хотите заказать? (стул/стол/шкаф): ").lower()
                components = []
                
                if prod_type == "стул":
                    components.append(Wood("Дуб", 10.0))
                    print("Для стула нужно: дерево 10 ед.")
                elif prod_type == "стол":
                    components.append(Wood("Сосна", 20.0))
                    components.append(Metal("Сталь", 5.0))
                    print("Для стола нужно: дерево 20 ед., металл 5 ед.")
                elif prod_type == "шкаф":
                    components.append(Wood("Дуб", 30.0))
                    components.append(Metal("Сталь", 8.0))
                    print("Для шкафа нужно: дерево 30 ед., металл 8 ед.")
                else:
                    print("Неизвестный тип изделия")
                    continue
                
                new_item = Furniture(prod_type.capitalize(), components)
                new_item.customer = name
                furnitures.append(new_item)
                print(f"Заказ принят! ID заказа: {len(furnitures)-1}")
            
            elif choice == "2":
                if not furnitures:
                    print("Нет заказов! Сначала создайте заказ.")
                    continue
                
                print("\nТекущие заказы:")
                for idx, furn in enumerate(furnitures):
                    if furn.status == FurnitureState.STORED:
                        status_display = "НА СКЛАДЕ"
                    elif furn.status == FurnitureState.QUALITY_CHECKED:
                        status_display = "ГОТОВ К УПАКОВКЕ"
                    elif furn.status == FurnitureState.ASSEMBLED:
                        status_display = "СОБРАН (ждет проверки)"
                    elif furn.status == FurnitureState.ELEMENTS_MANUFACTURED:
                        status_display = "ДЕТАЛИ ГОТОВЫ"
                    elif furn.status == FurnitureState.MATERIALS_PREPARED:
                        status_display = "МАТЕРИАЛЫ ГОТОВЫ"
                    else:
                        status_display = "НОВЫЙ"
                    
                    customer_info = f" (клиент: {furn.customer})" if hasattr(furn, 'customer') else ""
                    print(f"  {idx}. {furn.type}{customer_info} - {status_display}")
                
                prod_id = int(input("ID заказа для производства: "))
                if prod_id >= len(furnitures):
                    print("Неверный ID")
                    continue
                
                furniture = furnitures[prod_id]
                
                if furniture.status == FurnitureState.STORED:
                    print("Этот заказ уже готов и на складе!")
                    continue
                
                print(f"\n--- Начинаем производство {furniture.type} ---")
                print(f"Текущий статус: {furniture.status.value}")
                
                if furniture.status == FurnitureState.CREATED:
                    print("\nЭТАП 1: Подготовка материалов")
                    prep_op = PreparationOperation(material_storage, workers, tools)
                    prep_op.execute(furniture)
                    input("Нажмите Enter для продолжения...")
                
                if furniture.status == FurnitureState.MATERIALS_PREPARED:
                    print("\nЭТАП 2: Изготовление деталей")
                    elem_op = CreateElementOperation(material_storage, workers, tools)
                    elem_op.execute(furniture)
                    input("Нажмите Enter для продолжения...")
                
                if furniture.status == FurnitureState.ELEMENTS_MANUFACTURED:
                    print("\nЭТАП 3: Сборка")
                    assembly_op = AssemblyOperation(material_storage, workers)
                    assembly_op.execute(furniture)
                    input("Нажмите Enter для продолжения...")
                
                if furniture.status == FurnitureState.ASSEMBLED:
                    print("\nЭТАП 4: Контроль качества")
                    inspector = None
                    for w in workers:
                        if w.specialization == "контролер" and not w.is_busy:
                            inspector = w
                            break
                    
                    if inspector:
                        check_op = CheckOperation(inspector, workers)
                        check_op.execute(furniture)
                    else:
                        print("Нет свободного контролера, пропускаем этап")
                    input("Нажмите Enter для продолжения...")
                
                if furniture.status == FurnitureState.QUALITY_CHECKED:
                    print("\nЭТАП 5: Упаковка")
                    packer = None
                    for w in workers:
                        if not w.is_busy:
                            packer = w
                            break
                    
                    if packer:
                        pack_op = PackingOperation(packer, workers)
                        pack_op.execute(furniture)
                    else:
                        print("Нет свободного рабочего для упаковки")
                    input("Нажмите Enter для продолжения...")
                
                if furniture.status == FurnitureState.PACKED:
                    print("\nЭТАП 6: Доставка на склад")
                    furniture.change_status(FurnitureState.STORED)
                    workshop.add_completed_furniture(furniture)
                    print(f"{furniture.type} готов и отправлен на склад!")
                
                if furniture.status == FurnitureState.ASSEMBLED:
                    print("\nКачество не пройдено. Запустите производство еще раз для этого же заказа.")
            
            elif choice == "3":
                print("\n" + "=" * 40)
                print("СКЛАД ГОТОВОЙ ПРОДУКЦИИ")
                print("=" * 40)
                
                if workshop.completed_furnitures:
                    for idx, item in enumerate(workshop.completed_furnitures):
                        customer_info = f" (клиент: {item.customer})" if hasattr(item, 'customer') else ""
                        print(f"{idx+1}. {item.type}{customer_info}")
                else:
                    print("Склад пуст")
                
                print(f"\nВсего изделий: {len(workshop.completed_furnitures)}")
            
            elif choice == "4":
                print("\n" + "=" * 40)
                print("КЛИЕНТЫ И ИХ ЗАКАЗЫ")
                print("=" * 40)
                
                if not customers:
                    print("Нет клиентов")
                else:
                    for idx, customer in enumerate(customers):
                        print(f"\n{idx+1}. {customer.name} | {customer.phone}")
                        customer_orders = [f for f in furnitures if hasattr(f, 'customer') and f.customer == customer.name]
                        if customer_orders:
                            for order in customer_orders:
                                status_display = "ГОТОВ" if order.status == FurnitureState.STORED else "В ПРОИЗВОДСТВЕ"
                                print(f"   - {order.type} | {status_display}")
                        else:
                            print("   Нет заказов")
            
            elif choice == "5":
                print("\n" + "=" * 40)
                print("РАБОТНИКИ")
                print("=" * 40)
                
                for idx, worker in enumerate(workers):
                    status = "ЗАНЯТ" if worker.is_busy else "СВОБОДЕН"
                    print(f"{idx+1}. {worker.name}")
                    print(f"   Специализация: {worker.specialization}")
                    print(f"   Опыт: {worker.experience} лет")
                    print(f"   Статус: {status}")
            
            elif choice == "6":
                print("\n" + "=" * 40)
                print("ИНСТРУМЕНТЫ")
                print("=" * 40)
                
                for idx, tool in enumerate(tools):
                    status = "СЛОМАН" if tool.is_broken else "ИСПРАВЕН"
                    print(f"{idx+1}. {tool.name}")
                    print(f"   Прочность: {tool.durability}")
                    print(f"   Состояние: {status}")
            
            else:
                print("Неверный выбор")
        
        except ValueError:
            print("\nОшибка: введите число")
        except InvalidDataError as e:
            print(f"\nОшибка данных: {e}")
        except InvalidAmountError as e:
            print(f"\nОшибка количества: {e}")
        except InvalidOperation as e:
            print(f"\nОшибка операции: {e}")
        except Exception as e:
            print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()