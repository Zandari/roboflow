from typing import TypeVar
from abc import ABC, abstractmethod, abstractclassmethod, ABCMeta
import xml.etree.ElementTree as ET
from enum import Enum


TBaseModel = TypeVar("TBaseModel", bound="BaseModel")
TXMLModel  = TypeVar("TXMLModel", bound="XMLModel")
TXMLSerializable = TypeVar("TXMLSerializable", bound="XMLSerializable")
TContainer = TypeVar("TContainer", bound="Container")
# TState = TypeVar("TState", bound="State")


class DisallowedType(Exception):
    pass


class InitMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):

        basic_types = {str, int, list, set, Enum}
        meta_types = {XmlAttr, Container}

        annotations = namespace.get('__annotations__', {})
        for t in annotations.values():
            if t in basic_types or \
                 isinstance(t, tuple(meta_types)) or \
                 issubclass(t, tuple(basic_types)) or \
                 issubclass(t, BaseModel):
                continue
            raise DisallowedType(
                f"{t} is not supported."  \
                f" Only {[i.__name__ for i in basic_types.union(meta_types)]} are allowed."
            )

        def __init__(self, **kwargs):
            for field, value in kwargs.items():
                setattr(self, field, value)

        def __str__(self) -> str:
            result = self.__class__.__name__ + '('
            for field, value in self.__dict__.items():
                if field.startswith('_'):
                    continue
                result += f"{field}={value},"
            result += ')'
            return result

        
        __init__.__annotations__ = namespace.get("__annotations__")

        if '__init__' not in namespace:
            namespace['__init__'] = __init__

        if '__str__' not in namespace:
            namespace['__str__'] = __str__

        cls = super().__new__(mcs, name, bases, namespace)
        
        return cls

class Container:
    def __init__(self, container_type: type, data_type: type):
        self.container_type = container_type
        self.data_type = data_type


class XmlAttr:
    def __init__(self, name: str, attr_type: type):
        self.name = name
        self.attr_type = attr_type



class ABCInitMeta(ABCMeta, InitMeta):   # resolving metaclass conflict
    pass


class BaseModel(metaclass=ABCInitMeta):
    @classmethod
    def get_fields(cls) -> dict[str, type]:
        annotations = cls.__annotations__

        fields = {
            name: field_type for name, field_type in annotations.items()
            if not name.startswith('_')
        }

        return fields


class XMLSerializable(ABC):

    @abstractclassmethod
    def from_xml(cls, data: str) -> TXMLSerializable:
        ...

    @abstractclassmethod
    def _from_xml_element(cls, root: ET.Element) -> TXMLSerializable:
        ...
        
    @abstractmethod
    def to_xml(self) -> str:
        ...

    @abstractmethod
    def _to_xml_element(self) -> ET.Element:
        ...


class XMLModel(BaseModel, XMLSerializable):
    @classmethod
    def from_xml(cls: TXMLModel, data: str, strict: bool = True) -> TXMLModel:
        root = ET.fromstring(data)
        return cls._from_xml_element(root)


    @classmethod
    def _from_xml_element(cls: TXMLModel, root: ET.Element) -> TXMLModel:
        if root.tag != cls.__name__:
            f = True
            for subclass in cls.__subclasses__():
                if root.tag == subclass.__name__:
                    cls = subclass
                    f = False
                    break
            if f:
                raise Exception("OOO")

        fields = cls.get_fields()
        parsed_fields = dict()

        for name, attr_field in filter(
            lambda item: isinstance(item[1], XmlAttr), fields.items()
        ):
            parsed_fields[name] = attr_field.attr_type(
                root.attrib.get(attr_field.name)
            )

        for child in root:
            field_type = fields.get(child.tag)

            if field_type is None or isinstance(field_type, XmlAttr):
                continue

            if isinstance(field_type, type) and \
                issubclass(field_type, XMLSerializable):
                parsed_fields[child.tag] = field_type._from_xml_element(child[0])

            elif isinstance(field_type, Container):
                parsed_fields[child.tag] = field_type.container_type(
                    cls._iterable_from_xml_element(
                        root=child, 
                        data_type=field_type.data_type,
                    )
                )

            else:
                parsed_fields[child.tag] = field_type(child.text)
        
        return cls(**parsed_fields)

    @classmethod
    def _iterable_from_xml_element(
        cls: TXMLModel, 
        root: ET.Element,
        data_type: type,
    ) -> list[TXMLModel]:

        result = list[TXMLModel]()

        for child in root:
            if issubclass(data_type, XMLSerializable):
                result.append(
                    data_type._from_xml_element(child)
                )
            else:
                result.append(
                    data_type(child.text)
                )

        return result


    def to_xml(self) -> str:
        return ET.tostring(self._to_xml_element(), encoding="unicode")

    def _to_xml_element(self) -> ET.Element:
        fields = self.get_fields()
        data = {
            k: v for k, v in self.__dict__.items()
            if not callable(v) and not k.startswith('_')
        }

        root = ET.Element(type(self).__name__)

        for name, value in data.items():
            field_type = fields[name]

            if isinstance(field_type, XmlAttr):
                root.attrib[name] = str(value)

            elif isinstance(field_type, Container):
                cont_el = ET.Element(name)
                for v in value:
                    if issubclass(field_type.data_type, XMLSerializable):
                        cont_el.append(v._to_xml_element())
                    else:
                        el = ET.Element('el')
                        el.text = str(v)
                        cont_el.append(el)
                root.append(cont_el)

            elif issubclass(field_type, XMLSerializable):
                el = ET.Element(name)
                el.append(
                    value._to_xml_element()
                )
                root.append(el)

            else:
                el = ET.Element(name)
                el.text = str(value)
                root.append(el)

        return root


class Model(XMLModel):
    pass