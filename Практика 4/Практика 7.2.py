import os
import inspect
from pathlib import Path
import ast
import graphviz


def visualize_project_structure(project_path: str, output_file: str = "project_structure"):
    """
    Визуализирует иерархию модулей в проекте.

    :param project_path: Путь к корневой директории проекта
    :param output_file: Имя файла для сохранения визуализации
    """
    dot = graphviz.Digraph(comment='Project Structure')

    for root, dirs, files in os.walk(project_path):
        # Игнорируем служебные директории
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]

        current_dir = os.path.relpath(root, project_path)
        if current_dir == '.':
            current_dir = os.path.basename(project_path)
            dot.node(current_dir, shape='folder')
        else:
            dot.node(current_dir, shape='folder')
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == '':
                parent_dir = os.path.basename(project_path)
            dot.edge(parent_dir, current_dir)

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = os.path.splitext(file)[0]
                full_path = os.path.join(root, file)
                module_id = f"{current_dir}/{module_name}" if current_dir != '.' else module_name

                # Анализ модуля
                with open(full_path, 'r', encoding='utf-8') as f:
                    try:
                        module_node = ast.parse(f.read())
                        classes = [n.name for n in module_node.body if isinstance(n, ast.ClassDef)]
                        functions = [n.name for n in module_node.body if isinstance(n, ast.FunctionDef)]

                        label = f"{module_name}\n"
                        if classes:
                            label += "Classes: " + ", ".join(classes) + "\n"
                        if functions:
                            label += "Funcs: " + ", ".join(functions)

                        dot.node(module_id, label=label, shape='box')
                        dot.edge(current_dir, module_id)
                    except Exception as e:
                        print(f"Error parsing {full_path}: {e}")

    dot.render(output_file, format='png', cleanup=True)
    print(f"Визуализация сохранена в {output_file}.png")


# Пример использования
if __name__ == "__main__":
    visualize_project_structure("C:/Users/vovat/PycharmProjects/Питон1/Практика 4")