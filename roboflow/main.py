from scenario.models import (
    Scenario, State, Action, ValueType, Condition, Statement,
    ClickCoordsAction, ClickTextAction, WaitAction, WriteAction, RunAppAction
)
from uiautomator import Device
from time import sleep
from lxml import etree

import logging

logger = logging.getLogger("roboflow")
logger.setLevel(logging.DEBUG)


def execute_action(
    device: Device,
    action: Action
):
    if isinstance(action, ClickCoordsAction):
        device.click(action.coords.x, action.coords.y)
    elif isinstance(action, ClickTextAction):
        device(text=action.text).click()
    elif isinstance(action, WaitAction):
        sleep(action.duration_ms / 1000)
    elif isinstance(action, WriteAction):
        device.server.adb.raw_cmd(f"shell input text {action.text}")
    elif isinstance(action, RunAppAction):
        device.server.adb.raw_cmd((
            "shell monkey "
            f"-p {action.package_name} "
            "-c android.intent.category.LAUNCHER 1"
        ))

def check_statements(
    device: Device,
    statements: list[State]
) -> bool:
    xml = device.dump().encode('utf-8')
    with open('a.xml', 'wb') as f:
        f.write(xml)
    root = etree.fromstring(xml)

    result = True
    for statement in statements:
        value1 = None    
        value2 = None

        if statement.value_type_1 is ValueType.XPATH:
            elements = root.xpath(statement.value1)
            if elements:
                value1 = elements[0]
        elif statement.value_type_1 is ValueType.CONST:
            value1 = statement.value1

        if statement.value_type_2 is ValueType.XPATH:
            elements = root.xpath(statement.value2)
            if elements:
                value2 = elements[0]
        elif statement.value_type_2 is ValueType.CONST:
            value2 = statement.value2
        
        comp = False
        if statement.condition is Condition.GREATER_THAN:
            comp = value1 > value2
        elif statement.condition is Condition.LOWER_THAN:
            comp = value1 < value2
        elif statement.condition is Condition.EQUAL:
            comp = value1 == value2
        elif statement.condition is Condition.NOT_EQUAL:
            comp = value1 != value2
        
        if not comp:
            result = False
            break
    
    return result


def execute_state(
    device: Device,
    state: State, 
) -> bool:

    print(state)
    for action in state.actions:
        execute_action(device=device, action=action)


def execute_scenario(
    scenario: Scenario,
    device: Device | None = None,
):
    logger.info("Starting")

    if device is None:
        device = Device()

    states = scenario.states
    initial_state = [
        s for s in states 
        if s.state_id == scenario.initial_state_id
    ][0]

    state = initial_state
    while state is not None:
        execute_state(device, state)

        if len(state.next_states) == 0:
            logger.info("Success")
            break
        next_states = [s for s in states if s.state_id in state.next_states]
        state_found = False
        for st in next_states:
            correct = check_statements(device, st.statements)
            if correct:
                state = st
                logger.info(f"Next state: {st.name}")
                state_found = True
                break
        
        if not state_found:
            logger.info("Failed")
            break

if __name__ == "__main__":
   device = Device()
   statements = [
     Statement(
        value_type_1=ValueType.CONST,
        value1="Настройки",
        value_type_2=ValueType.XPATH,
        value2="//node[@text='Настройки']/@text",
        condition=Condition.EQUAL
     )
   ]
   res = check_statements(
        device=device,
        statements=statements,
   )
   print(res)
