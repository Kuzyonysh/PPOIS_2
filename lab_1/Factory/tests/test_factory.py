import pytest
from unittest.mock import patch, MagicMock

from models.material import Metal, Wood
from models.furniture import Furniture, FurnitureState
from models.people import Worker, Customer
from models.tool import Tool
from models.warehouse import Warehouse
from models.factory import Factory
from models.workshop import Workshop
from models.exceptions import InvalidAmountError, InvalidDataError, InvalidOperation
from models.orders import Order

from operations.operations import (
    PreparationOperation,
    AssemblyOperation,
    CheckOperation,
    PackingOperation,
    DeliveryOperation,
)

def test_material_validation():
    with pytest.raises(InvalidAmountError):
        Metal("Steel", 0)

    with pytest.raises(InvalidAmountError):
        Metal("Steel", -5)

    with pytest.raises(InvalidDataError):
        Metal("", 10)


def test_material_str():
    m = Metal("Steel", 10)
    assert "Steel" in str(m)

def test_furniture_creation():
    materials = [Metal("Steel", 5), Wood("Oak", 3)]
    f = Furniture("Table", materials)

    assert f.status == FurnitureState.CREATED
    assert f.material_count == 2


def test_furniture_invalid_status():
    f = Furniture("Chair", [])
    with pytest.raises(InvalidDataError):
        f.status = "WRONG"

def test_worker_creation():
    w = Worker("Ivan", 30, "assembler", 5)
    assert w.name == "Ivan"
    assert w.is_busy is False


def test_worker_invalid_age():
    with pytest.raises(InvalidDataError):
        Worker("Ivan", -1, "assembler", 3)

def test_tool_use_and_break():
    t = Tool("Hammer", 2)
    t.use()
    assert t.durability == 1

    with pytest.raises(Exception):
        t.use()

def test_warehouse_add_remove():
    w = Warehouse("Main", 100)
    metal = Metal("Steel", 20)
    wood = Wood("Oak", 10)

    w.add_material(metal)
    w.add_material(wood)

    assert w.metal_amount == 20
    assert w.wood_amount == 10

    w.remove_metal(10)
    w.remove_wood(5)

    assert w.metal_amount == 10
    assert w.wood_amount == 5


def test_warehouse_overflow():
    w = Warehouse("Main", 10)
    with pytest.raises(InvalidAmountError):
        w.add_material(Metal("Steel", 50))


def test_workshop():
    workshop = Workshop("Furniture")
    f = Furniture("Table", [])

    workshop.add_completed_furniture(f)
    assert workshop.get_completed_count() == 1


class DummyOperation:
    def execute(self, furniture):
        furniture.change_status(FurnitureState.MATERIALS_PREPARED)


def test_factory_process():
    worker = Worker("Ivan", 30, "assembler", 5)
    tool = Tool("Hammer", 10)
    f = Furniture("Chair", [])

    factory = Factory("Wood", [worker], [tool], DummyOperation())
    factory.process(f)

    assert f.status == FurnitureState.MATERIALS_PREPARED


def test_factory_no_workers():
    tool = Tool("Hammer", 10)
    f = Furniture("Chair", [])

    factory = Factory("Wood", [], [tool], DummyOperation())

    with pytest.raises(InvalidDataError):
        factory.process(f)

def test_order_str():
    customer = Customer("Alex", 35, "+79999999999")
    furniture = Furniture("Chair", [])
    order = Order(customer, furniture)

    assert isinstance(str(order), str)


def create_basic_setup():
    warehouse = Warehouse("Main", 100)
    worker = Worker("John", 30, "worker", 5)  
    tool = Tool("Hammer", 10)
    furniture = Furniture("Chair", [Wood("Oak", 10), Metal("Steel", 5)])
    return warehouse, worker, tool, furniture


def test_preparation_wrong_status():
    warehouse, worker, tool, furniture = create_basic_setup()
    furniture.change_status(FurnitureState.ASSEMBLED)

    op = PreparationOperation(warehouse, [worker], [tool])

    with pytest.raises(InvalidOperation):
        op.execute(furniture)

def test_assembly_success():
    warehouse, worker, tool, furniture = create_basic_setup()
    furniture.change_status(FurnitureState.ELEMENTS_MANUFACTURED)

    op = AssemblyOperation(warehouse, [worker])
    op.execute(furniture)

    assert furniture.status == FurnitureState.ASSEMBLED


@patch("operations.operations.random.randint")
@patch("operations.operations.random.sample")
def test_check_pass(mock_sample, mock_randint):
    warehouse, worker, tool, furniture = create_basic_setup()
    furniture.change_status(FurnitureState.ASSEMBLED)

    mock_randint.side_effect = [0, 85]
    mock_sample.return_value = []

    op = CheckOperation(worker)
    op.execute(furniture)

    assert furniture.status == FurnitureState.QUALITY_CHECKED
    assert furniture.quality_score == 85


@patch("operations.operations.random.randint")
@patch("operations.operations.random.sample")
def test_check_fail(mock_sample, mock_randint):
    warehouse, worker, tool, furniture = create_basic_setup()
    furniture.change_status(FurnitureState.ASSEMBLED)

    mock_randint.side_effect = [2, 60]
    mock_sample.return_value = ["Scratch", "Crack"]

    op = CheckOperation(worker)
    op.execute(furniture)

    assert furniture.status == FurnitureState.ELEMENTS_MANUFACTURED


@patch("operations.operations.random.randint", return_value=1)
@patch("operations.operations.random.sample", return_value=["Box"])
def test_packing_success(mock_sample, mock_randint):
    warehouse, worker, tool, furniture = create_basic_setup()
    furniture.change_status(FurnitureState.QUALITY_CHECKED)

    op = PackingOperation(worker)
    op.execute(furniture)

    assert furniture.status == FurnitureState.PACKED


def test_delivery_success():
    warehouse, worker, tool, furniture = create_basic_setup()
    furniture.change_status(FurnitureState.PACKED)

    op = DeliveryOperation(worker, address="Moscow")

    op.workshop = MagicMock()
    op.workshop.add_completed_furniture = MagicMock()
    op.workshop.workshop_type = "Main"

    op.execute(furniture)

    assert furniture.status == FurnitureState.DELIVERED

def test_tool_creation_valid():
    t = Tool("Hammer", 10)
    assert t.name == "Hammer"
    assert t.durability == 10
    assert not t.is_broken

def test_tool_creation_invalid_name():
    with pytest.raises(InvalidDataError):
        Tool("", 10)

def test_tool_creation_invalid_durability_type():
    with pytest.raises(InvalidAmountError):
        Tool("Hammer", "ten")

def test_tool_creation_invalid_durability_value():
    with pytest.raises(InvalidAmountError):
        Tool("Hammer", 0)
    with pytest.raises(InvalidAmountError):
        Tool("Hammer", -5)

def test_name_setter():
    t = Tool("Hammer", 5)
    t.name = "Axe"
    assert t.name == "Axe"
    with pytest.raises(InvalidDataError):
        t.name = ""

def test_durability_setter():
    t = Tool("Hammer", 5)
    t.durability = 10
    assert t.durability == 10
    with pytest.raises(InvalidAmountError):
        t.durability = -1
    with pytest.raises(InvalidAmountError):
        t.durability = 0
    with pytest.raises(InvalidAmountError):
        t.durability = "ten"

def test_repair_partial():
    t = Tool("Hammer", 5)
    msg = t.repair(10)
    assert t.durability == 15
    assert "repaired by 10" in msg

def test_repair_invalid_amount():
    t = Tool("Hammer", 5)
    with pytest.raises(InvalidAmountError):
        t.repair(-5)
    with pytest.raises(InvalidAmountError):
        t.repair("ten")