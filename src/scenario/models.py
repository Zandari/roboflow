from scenario.base import Model, Container, XmlAttr
from enum import Enum


class Point(Model):
    x: XmlAttr("x", float)
    y: XmlAttr("y", float)


class Action(Model):
    ...

class ClickCoordsAction(Action):
    coords: Point
    duration_ms: int

class ClickTextAction(Action):
    text: str
    duration_ms: int

class WaitAction(Action):
    duration_ms: int

class WriteAction(Action):
    text: str

class RunAppAction(Action):
    package_name: str

class Condition(Enum):
    GREATER_THAN = "gt"
    LOWER_THAN   = "lt"
    EQUAL        = "eq"
    NOT_EQUAL    = "ne"

class ValueType(Enum):
    XPATH = "XPath"
    CONST = "Const"


class Statement(Model):
    value_type_1: ValueType
    value1: str
    value_type_2: ValueType
    value2: str
    condition: Condition

    @staticmethod
    def get_blank_instance():
        return Statement(
            value_type_1=ValueType.CONST,
            value1="asdf",
            value_type_2=ValueType.XPATH,
            value2="//",
            condition=Condition.EQUAL
        )


class TState(Model):
    ...


class State(TState):
    name: str
    state_id: int
    description: str
    statements: Container(set, Statement)
    actions: Container(list, Action)
    next_states: Container(set, int)   # state_id
    priority: int
    position: Point

    @staticmethod
    def get_blank_instance():
        return State(
            name="",
            state_id=0,
            description="",
            statements=set(),
            actions=list(),
            next_states=set(),
            priority=100,
            position=Point(x=0, y=0),
        )


class Scenario(Model):
    name: str
    initial_state_id: int  # state_id
    states: Container(list, State)


class Project(Model):
    version: XmlAttr("ver", str)
    scenaries: Container(list, Scenario)
