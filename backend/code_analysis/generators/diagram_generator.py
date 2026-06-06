import os


class DiagramGenerator:
    def __init__(self):
        self.diagrams = {}

    def generate_dependency_diagram(self, dependencies: dict) -> str:
        lines = ["graph TD;"]
        node_ids = {}
        node_counter = 0

        for module, info in dependencies.items():
            safe_id = self._safe_id(module, node_ids, node_counter)
            node_counter += 1
            label = os.path.splitext(os.path.basename(module))[0]
            lines.append(f"    {safe_id}[\"{label}\"];")

        node_counter = 0
        module_to_id = {}
        for module in dependencies:
            safe_id = self._safe_id(module, module_to_id, node_counter)
            node_counter += 1
            module_to_id[module] = safe_id

        for module, info in dependencies.items():
            source_id = module_to_id[module]
            for dep in info.get("dependencies", []):
                dep_clean = dep.split("/")[-1].split(".")[0] if "/" in dep else dep
                dep_clean = dep_clean.split("\\")[-1]
                if dep_clean not in [v.split("\"")[1] if "\"" in v else v for v in module_to_id.values()]:
                    dep_id = dep_clean.replace("-", "_").replace(".", "_")
                    lines.append(f"    {dep_id}[\"{dep_clean}\"];")
                target_id = module_to_id.get(dep, dep_clean.replace("-", "_").replace(".", "_"))
                lines.append(f"    {source_id} --> {target_id};")

        return "\n".join(lines)

    def _safe_id(self, name, id_map, counter):
        safe = name.replace("/", "_").replace("\\", "_").replace(".", "_").replace("-", "_").replace(":", "_")
        if safe in id_map:
            return f"{safe}_{counter}"
        return safe

    def generate_class_diagram(self, classes: list[dict]) -> str:
        lines = ["classDiagram;"]

        for cls in classes:
            class_name = cls.get("name", "Unknown")
            lines.append(f"    class {class_name} {{")

            for attr in cls.get("attributes", []):
                if isinstance(attr, dict):
                    visibility = "+" if attr.get("visibility", "public") == "public" else "-"
                    attr_name = attr.get("name", "attr")
                    attr_type = attr.get("type", "")
                    type_str = f" {attr_type}" if attr_type else ""
                    lines.append(f"        {visibility}{attr_name}{type_str}")
                else:
                    lines.append(f"        +{attr}")

            for method in cls.get("methods", []):
                if isinstance(method, dict):
                    visibility = "+" if method.get("visibility", "public") == "public" else "-"
                    method_name = method.get("name", "method")
                    params = method.get("parameters", [])
                    return_type = method.get("return_type", "")
                    param_str = ", ".join(str(p) for p in params) if params else ""
                    ret_str = f" {return_type}" if return_type else ""
                    lines.append(f"        {visibility}{method_name}({param_str}){ret_str}")
                else:
                    lines.append(f"        +{method}()")

            lines.append("    }")

            for base in cls.get("bases", []):
                base_name = base if isinstance(base, str) else base.get("name", str(base))
                lines.append(f"    {class_name} --|> {base_name} : extends")

        return "\n".join(lines)

    def generate_flow_diagram(self, flow: dict) -> str:
        lines = ["flowchart TD;"]

        call_graph = flow.get("call_graph", {})
        if call_graph:
            for func, callees in call_graph.items():
                func_id = func.replace("-", "_").replace(" ", "_")
                lines.append(f"    {func_id}[\"{func}\"];")
                for callee in callees:
                    callee_id = callee.replace("-", "_").replace(" ", "_")
                    lines.append(f"    {func_id} --> {callee_id}[\"{callee}\"];")

        control_flow = flow.get("control_flow", {})
        nodes = control_flow.get("nodes", [])
        edges = control_flow.get("edges", [])
        if nodes and not call_graph:
            for node in nodes:
                nid = node.get("id", 0)
                ntype = node.get("type", "block")
                label = node.get("keyword", ntype)
                lines.append(f"    N{nid}[{label}];")
            for edge in edges:
                frm = edge.get("from", 0)
                to = edge.get("to", 0)
                lbl = edge.get("label", "")
                if lbl:
                    lines.append(f"    N{frm} -- {lbl} --> N{to};")
                else:
                    lines.append(f"    N{frm} --> N{to};")

        return "\n".join(lines)

    def generate_architecture_diagram(self, project_data: dict) -> str:
        lines = ["graph TB;"]
        subgraph_count = 0

        files = project_data.get("files", {})
        if not files:
            return "graph TB;\n    Root[No Data];"

        dir_structure = {}
        for fpath in files:
            parts = fpath.replace("\\", "/").split("/")
            current = dir_structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = None

        def add_subgraph(structure, parent="Root"):
            nonlocal subgraph_count
            for key, value in structure.items():
                if value is None:
                    safe = key.replace(".", "_").replace("-", "_")
                    lines.append(f"    {safe}[\"{key}\"];")
                    lines.append(f"    {parent} --> {safe};")
                elif isinstance(value, dict):
                    sg_id = f"SG{subgraph_count}"
                    subgraph_count += 1
                    lines.append(f"    subgraph {sg_id}[\"{key}\"]")
                    add_subgraph(value, sg_id)
                    lines.append("    end")
                    lines.append(f"    {parent} --> {sg_id};")

        lines.append("    Root[\"Project Root\"];")
        add_subgraph(dir_structure)
        return "\n".join(lines)
