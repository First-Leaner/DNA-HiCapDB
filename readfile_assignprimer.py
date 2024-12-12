import os
import csv

class PrimerNodeAssigner:
    def __init__(self, primer_file_path, binary_length=8):
        self.binary_length = binary_length  # 设置每层节点的固定二进制长度
        self.node_map = {}
        self.primers = self._load_primers(primer_file_path)  # 加载引物对库

    def _load_primers(self, primer_file_path):
        """从文件中加载引物对库，每一行表示一个引物对。"""
        primers = []
        with open(primer_file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                primers.append(row)  # 假设文件每行包含一个引物对
        return primers

    def assign_codes_and_primers(self, directory_path):
        """为每个文件分配节点编码和引物对。"""
        self._recursive_assign(directory_path, "", 0)

    def _recursive_assign(self, current_path, binary_prefix, primer_index):
        """递归分配节点编码和引物对。"""
        items = os.listdir(current_path)
        
        for index, item in enumerate(items):
            item_path = os.path.join(current_path, item)
            # 为当前层生成二进制编码
            binary_code = binary_prefix + format(index, f'0{self.binary_length}b')
            
            # 分配一个引物对
            if primer_index < len(self.primers):
                primer_pair = self.primers[primer_index]
                primer_index += 1  # 更新引物索引
            else:
                raise ValueError("引物对库不足，无法为所有节点分配唯一引物对。")

            if os.path.isdir(item_path):
                # 如果是目录，递归分配子节点
                self._recursive_assign(item_path, binary_code, primer_index)
            else:
                # 存储文件路径、节点编码和分配的引物对
                self.node_map[item_path] = (binary_code, primer_pair)

    def save_assignments_to_file(self, output_file="node_assignments.csv"):
        """将文件路径、节点编码和引物对保存到CSV文件中。"""
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Path", "Binary Code", "Primer1", "Primer2"])
            for file_path, (binary_code, primer_pair) in self.node_map.items():
                writer.writerow([file_path, binary_code, primer_pair[0], primer_pair[1]])

# 示例使用
primer_file = "primers.csv"  # 引物库文件路径
root_directory = "dataset"  # 数据集的根目录
binary_length = 8  # 每层节点的固定二进制编码长度

assigner = PrimerNodeAssigner(primer_file, binary_length=binary_length)
assigner.assign_codes_and_primers(root_directory)
assigner.save_assignments_to_file("node_assignments.csv")
