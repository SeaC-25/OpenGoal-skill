#!/usr/bin/env python3
"""
OpenGoal Skill - 图表绘制脚本
使用 matplotlib + networkx 绘制架构图、依赖图、流程图等

继承 nature-figure 的绘图风格和调色板
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import networkx as nx
import json
from typing import List, Dict, Any, Tuple
import os

# 调色板（继承自 nature-figure）
PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral_light": "#CFCECE",
    "neutral_mid": "#767676",
    "neutral_dark": "#4D4D4D",
    "neutral_black": "#272727",
    "gold": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "magenta": "#EA84DD",
}

DEFAULT_COLORS = [
    PALETTE["blue_main"],
    PALETTE["green_3"],
    PALETTE["red_strong"],
    PALETTE["teal"],
    PALETTE["violet"],
    PALETTE["neutral_light"],
]

# 配置 matplotlib 的默认样式（继承 nature-figure）
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'axes.linewidth': 1.5,
    'grid.linewidth': 0.8,
    'lines.linewidth': 2,
})


class DiagramDrawer:
    """图表绘制器"""

    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def draw_dependency_graph(self, dependencies: List[Dict[str, str]],
                              title: str = "依赖关系图",
                              detect_cycle: bool = True) -> str:
        """
        绘制依赖关系图

        Args:
            dependencies: 依赖关系列表，格式 [{"from": "A", "to": "B"}, ...]
            title: 图表标题
            detect_cycle: 是否检测循环依赖

        Returns:
            图片文件路径
        """
        G = nx.DiGraph()

        # 添加边
        for dep in dependencies:
            G.add_edge(dep["from"], dep["to"])

        # 检测循环依赖
        cycles = []
        if detect_cycle:
            try:
                cycles = list(nx.simple_cycles(G))
            except:
                pass

        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 8))

        # 使用层次布局
        try:
            pos = nx.spring_layout(G, k=2, iterations=50)
        except:
            pos = nx.shell_layout(G)

        # 绘制节点
        node_colors = []
        for node in G.nodes():
            # 如果节点在循环依赖中，标红
            in_cycle = any(node in cycle for cycle in cycles)
            node_colors.append(PALETTE["red_strong"] if in_cycle else PALETTE["blue_main"])

        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                              node_size=3000, alpha=0.9, ax=ax)

        # 绘制边
        edge_colors = []
        for edge in G.edges():
            # 如果边在循环依赖中，标红
            in_cycle = any(edge[0] in cycle and edge[1] in cycle for cycle in cycles)
            edge_colors.append(PALETTE["red_strong"] if in_cycle else PALETTE["neutral_mid"])

        nx.draw_networkx_edges(G, pos, edge_color=edge_colors,
                              arrows=True, arrowsize=20,
                              arrowstyle='->', width=2, ax=ax)

        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10,
                               font_color='white', font_weight='bold', ax=ax)

        # 标题
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

        # 如果有循环依赖，添加警告文本
        if cycles:
            cycle_text = "⚠️ 检测到循环依赖:\n" + "\n".join(
                [" → ".join(cycle + [cycle[0]]) for cycle in cycles]
            )
            ax.text(0.02, 0.98, cycle_text,
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor=PALETTE["red_1"], alpha=0.8))

        ax.axis('off')
        plt.tight_layout()

        # 保存
        output_path = os.path.join(self.output_dir, "dependency_graph.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def draw_architecture_diagram(self, layers: List[Dict[str, Any]],
                                  title: str = "系统架构图") -> str:
        """
        绘制系统架构图（分层架构）

        Args:
            layers: 层次列表，格式 [
                {"name": "前端层", "components": ["React", "Vue"]},
                {"name": "接口层", "components": ["API Gateway", "REST API"]},
                ...
            ]
            title: 图表标题

        Returns:
            图片文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 10))

        num_layers = len(layers)
        layer_height = 0.15
        layer_gap = 0.05
        start_y = 0.85

        colors = DEFAULT_COLORS[:num_layers]

        for i, layer in enumerate(layers):
            y = start_y - i * (layer_height + layer_gap)

            # 绘制层次框
            rect = FancyBboxPatch((0.05, y - layer_height), 0.9, layer_height,
                                 boxstyle="round,pad=0.01",
                                 edgecolor=colors[i], facecolor=colors[i],
                                 alpha=0.3, linewidth=2)
            ax.add_patch(rect)

            # 层次名称
            ax.text(0.03, y - layer_height/2, layer["name"],
                   fontsize=14, fontweight='bold', va='center',
                   color=PALETTE["neutral_black"])

            # 组件列表
            components_text = " | ".join(layer.get("components", []))
            ax.text(0.5, y - layer_height/2, components_text,
                   fontsize=11, va='center', ha='center',
                   color=PALETTE["neutral_dark"])

            # 绘制箭头（指向下一层）
            if i < num_layers - 1:
                arrow = FancyArrowPatch((0.5, y - layer_height),
                                       (0.5, y - layer_height - layer_gap),
                                       arrowstyle='->', mutation_scale=20,
                                       color=PALETTE["neutral_mid"], linewidth=2)
                ax.add_patch(arrow)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')

        plt.tight_layout()

        # 保存
        output_path = os.path.join(self.output_dir, "architecture_diagram.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def draw_service_map(self, services: List[Dict[str, Any]],
                        interactions: List[Dict[str, str]],
                        title: str = "服务关系图") -> str:
        """
        绘制服务关系图（微服务架构）

        Args:
            services: 服务列表，格式 [
                {"name": "UserService", "type": "core"},
                {"name": "OrderService", "type": "core"},
                {"name": "EmailService", "type": "support"},
                ...
            ]
            interactions: 交互关系，格式 [
                {"from": "OrderService", "to": "UserService", "type": "sync"},
                {"from": "OrderService", "to": "EmailService", "type": "async"},
                ...
            ]
            title: 图表标题

        Returns:
            图片文件路径
        """
        G = nx.DiGraph()

        # 添加节点
        for service in services:
            G.add_node(service["name"], service_type=service.get("type", "core"))

        # 添加边
        for interaction in interactions:
            G.add_edge(interaction["from"], interaction["to"],
                      interaction_type=interaction.get("type", "sync"))

        # 创建图形
        fig, ax = plt.subplots(figsize=(14, 10))

        # 布局
        pos = nx.spring_layout(G, k=3, iterations=50)

        # 绘制节点（根据服务类型着色）
        service_types = nx.get_node_attributes(G, 'service_type')
        node_colors = []
        for node in G.nodes():
            stype = service_types.get(node, 'core')
            if stype == 'core':
                node_colors.append(PALETTE["blue_main"])
            elif stype == 'support':
                node_colors.append(PALETTE["green_3"])
            else:
                node_colors.append(PALETTE["neutral_mid"])

        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                              node_size=4000, alpha=0.9, ax=ax)

        # 绘制边（根据交互类型样式不同）
        interaction_types = nx.get_edge_attributes(G, 'interaction_type')

        # 同步调用（实线）
        sync_edges = [e for e in G.edges() if interaction_types.get(e, 'sync') == 'sync']
        nx.draw_networkx_edges(G, pos, edgelist=sync_edges,
                              edge_color=PALETTE["neutral_dark"],
                              arrows=True, arrowsize=20, arrowstyle='->',
                              width=2, style='solid', ax=ax)

        # 异步消息（虚线）
        async_edges = [e for e in G.edges() if interaction_types.get(e, 'sync') == 'async']
        nx.draw_networkx_edges(G, pos, edgelist=async_edges,
                              edge_color=PALETTE["teal"],
                              arrows=True, arrowsize=20, arrowstyle='->',
                              width=2, style='dashed', ax=ax)

        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10,
                               font_color='white', font_weight='bold', ax=ax)

        # 图例
        legend_elements = [
            mpatches.Patch(facecolor=PALETTE["blue_main"], label='核心服务'),
            mpatches.Patch(facecolor=PALETTE["green_3"], label='支撑服务'),
            plt.Line2D([0], [0], color=PALETTE["neutral_dark"], linewidth=2, label='同步调用'),
            plt.Line2D([0], [0], color=PALETTE["teal"], linewidth=2, linestyle='--', label='异步消息'),
        ]
        ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9)

        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')

        plt.tight_layout()

        # 保存
        output_path = os.path.join(self.output_dir, "service_map.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path

    def draw_domain_model(self, aggregates: List[Dict[str, Any]],
                         title: str = "领域模型图") -> str:
        """
        绘制领域模型图（聚合、实体、值对象）

        Args:
            aggregates: 聚合列表，格式 [
                {
                    "name": "Order",
                    "type": "aggregate_root",
                    "entities": ["OrderItem"],
                    "value_objects": ["Money", "Address"]
                },
                ...
            ]
            title: 图表标题

        Returns:
            图片文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 10))

        num_aggregates = len(aggregates)
        box_width = 0.8 / num_aggregates
        start_x = 0.1

        for i, agg in enumerate(aggregates):
            x = start_x + i * (box_width + 0.05)
            y_start = 0.7

            # 聚合根框
            root_box = FancyBboxPatch((x, y_start), box_width, 0.15,
                                     boxstyle="round,pad=0.01",
                                     edgecolor=PALETTE["blue_main"],
                                     facecolor=PALETTE["blue_main"],
                                     alpha=0.3, linewidth=3)
            ax.add_patch(root_box)

            ax.text(x + box_width/2, y_start + 0.075, agg["name"],
                   fontsize=12, fontweight='bold', ha='center', va='center',
                   color=PALETTE["neutral_black"])

            # 实体
            entities = agg.get("entities", [])
            y_entity = y_start - 0.2
            for j, entity in enumerate(entities):
                entity_box = FancyBboxPatch((x, y_entity - j*0.08), box_width, 0.06,
                                          boxstyle="round,pad=0.005",
                                          edgecolor=PALETTE["green_3"],
                                          facecolor=PALETTE["green_1"],
                                          alpha=0.7, linewidth=2)
                ax.add_patch(entity_box)

                ax.text(x + box_width/2, y_entity - j*0.08 + 0.03, entity,
                       fontsize=9, ha='center', va='center',
                       color=PALETTE["neutral_dark"])

            # 值对象
            value_objects = agg.get("value_objects", [])
            y_vo = y_entity - len(entities)*0.08 - 0.1
            for j, vo in enumerate(value_objects):
                vo_box = FancyBboxPatch((x, y_vo - j*0.06), box_width, 0.04,
                                       boxstyle="round,pad=0.003",
                                       edgecolor=PALETTE["neutral_mid"],
                                       facecolor=PALETTE["neutral_light"],
                                       alpha=0.5, linewidth=1)
                ax.add_patch(vo_box)

                ax.text(x + box_width/2, y_vo - j*0.06 + 0.02, vo,
                       fontsize=8, ha='center', va='center',
                       color=PALETTE["neutral_dark"])

        # 图例
        legend_elements = [
            mpatches.Patch(facecolor=PALETTE["blue_main"], alpha=0.3,
                          edgecolor=PALETTE["blue_main"], linewidth=3, label='聚合根'),
            mpatches.Patch(facecolor=PALETTE["green_1"], alpha=0.7,
                          edgecolor=PALETTE["green_3"], linewidth=2, label='实体'),
            mpatches.Patch(facecolor=PALETTE["neutral_light"], alpha=0.5,
                          edgecolor=PALETTE["neutral_mid"], linewidth=1, label='值对象'),
        ]
        ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')

        plt.tight_layout()

        # 保存
        output_path = os.path.join(self.output_dir, "domain_model.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        return output_path


def main():
    """测试用例"""
    drawer = DiagramDrawer(output_dir=".")

    # 测试依赖关系图
    dependencies = [
        {"from": "OrderService", "to": "UserService"},
        {"from": "OrderService", "to": "ProductService"},
        {"from": "OrderService", "to": "PaymentService"},
        {"from": "PaymentService", "to": "UserService"},
    ]
    print("生成依赖关系图...")
    dep_path = drawer.draw_dependency_graph(dependencies, title="订单系统依赖关系图")
    print(f"✓ 已保存: {dep_path}")

    # 测试架构图
    layers = [
        {"name": "前端层", "components": ["React", "TypeScript", "Redux"]},
        {"name": "接口层", "components": ["API Gateway", "RESTful API", "GraphQL"]},
        {"name": "业务逻辑层", "components": ["UserService", "OrderService", "PaymentService"]},
        {"name": "数据访问层", "components": ["UserRepository", "OrderRepository"]},
        {"name": "基础设施层", "components": ["PostgreSQL", "Redis", "Kafka"]},
    ]
    print("生成架构图...")
    arch_path = drawer.draw_architecture_diagram(layers, title="电商系统架构图")
    print(f"✓ 已保存: {arch_path}")

    # 测试服务关系图
    services = [
        {"name": "UserService", "type": "core"},
        {"name": "OrderService", "type": "core"},
        {"name": "PaymentService", "type": "core"},
        {"name": "EmailService", "type": "support"},
        {"name": "LogService", "type": "support"},
    ]
    interactions = [
        {"from": "OrderService", "to": "UserService", "type": "sync"},
        {"from": "OrderService", "to": "PaymentService", "type": "sync"},
        {"from": "OrderService", "to": "EmailService", "type": "async"},
        {"from": "PaymentService", "to": "LogService", "type": "async"},
    ]
    print("生成服务关系图...")
    service_path = drawer.draw_service_map(services, interactions, title="微服务关系图")
    print(f"✓ 已保存: {service_path}")

    # 测试领域模型图
    aggregates = [
        {
            "name": "Order",
            "type": "aggregate_root",
            "entities": ["OrderItem", "PaymentInfo"],
            "value_objects": ["Money", "Address"]
        },
        {
            "name": "User",
            "type": "aggregate_root",
            "entities": ["UserProfile"],
            "value_objects": ["Email", "Password"]
        },
    ]
    print("生成领域模型图...")
    domain_path = drawer.draw_domain_model(aggregates, title="电商领域模型")
    print(f"✓ 已保存: {domain_path}")

    print("\n所有图表生成完成！")


if __name__ == "__main__":
    main()
