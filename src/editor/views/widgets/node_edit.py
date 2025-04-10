from qtpy import QtWidgets, QtCore
from NodeGraphQt import NodeGraph, BaseNode, Port

from editor.models.editor_model import StatesModel
from editor.controllers.editor_controller import EditorController
from scenario.models import State, Point, Scenario


class ModifiedNodeGraph(NodeGraph):
    node_moved = QtCore.Signal(BaseNode)

    def _on_nodes_moved(self, node_data):
        super()._on_nodes_moved(node_data)

        for node_view, prev_pos in node_data.items():
            node = self.get_node_by_id(node_view.id)
            self.node_moved.emit(node)



class StateNode(BaseNode):
    __identifier__ = 'nodes'

    NODE_NAME = "Application State"

    def __init__(self):
        super(StateNode, self).__init__()

        self.add_input('in', multi_input=False)
        self.add_output('out', multi_output=True)

        self.set_port_deletion_allowed(mode=True)


class NodeEdit(QtWidgets.QWidget):
    state_selected = QtCore.Signal(Scenario, State)

    def __init__(
        self, 
        model: StatesModel | None,
        controller: EditorController,
    ):
        super().__init__()

        self._controller = controller

        self._graph = ModifiedNodeGraph()
        self._graph.register_node(StateNode)
        self._graph.port_connected.connect(self._on_port_connected)
        self._graph.node_double_clicked.connect(
            lambda n: self.state_selected.emit(
                self._model.get_scenario(),
                n.state
            )
        )
        self._graph.node_moved.connect(
            self._on_node_moved
        )
        self._graph.nodes_deleted.connect(
            self._on_nodes_deleted
        ) 

        self._add_node_button = QtWidgets.QPushButton("Add State")
        self._add_node_button.clicked.connect(self._on_add_node)
        self._add_node_button.setMinimumSize(QtCore.QSize(30, 30))

        if model is not None:
            self.set_model(model)
        else:
            self.disable()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._add_node_button)
        layout.addWidget(self._graph.widget)

        self.setLayout(layout)

    def enable(self) -> None:
        self._add_node_button.setEnabled(True)

    def disable(self) -> None:
        self._add_node_button.setEnabled(False)

    def set_model(self, model: StatesModel) -> None: 
        self._model = model
        self._model.states_changed.connect(
            self._update_nodes
        )
        self._update_nodes(self._model.get_states())

    @QtCore.Slot()
    def _on_node_moved(self, node: StateNode) -> None:
        pos = node.pos()
        self._controller.set_state_position(
            scenario=self._model.get_scenario(),
            state=node.state,
            pos=Point(x=pos[0], y=pos[1]),
        )

    @QtCore.Slot()
    def _on_nodes_deleted(self, nodes: list[str]) -> None:
        ...

    @QtCore.Slot()
    def _on_port_connected(self, port_in: Port, port_out: Port) -> None:
        self._controller.add_state_connection(
            scenario=self._model.get_scenario(),
            state_from=port_out.node().state,
            state_to=port_in.node().state
        )

    @QtCore.Slot()
    def _on_add_node(self) -> None:
        self._controller.create_state(
            self._model.get_scenario()
        )

    @QtCore.Slot()
    def _update_nodes(self, states: list[State]) -> None:
        print("nodes updated")
        self._graph.clear_session()

        nodes = dict()
        for state in states:
            print(state.position)
            node = self._graph.create_node(
                node_type="nodes.StateNode", 
                name=state.name,
                pos=(
                    state.position.x,
                    state.position.y
                ),
                push_undo=False,
            )
            if state.state_id == 0:
                node.delete_input("in")
            node.state = state
            nodes[state.state_id] = node

        for state in states:
            node = nodes[state.state_id]
            for s in state.next_states:
                node.set_output(0, nodes[s].input(0))

