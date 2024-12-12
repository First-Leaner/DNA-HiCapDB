import random
import csv

# 定义DNA的碱基
bases = ['A', 'T', 'C', 'G']

# 检查均聚物
def has_homopolymer(seq, max_len=5):
    """检查序列中是否存在长度超过max_len的均聚物"""
    for base in bases:
        if base * (max_len + 1) in seq:
            return True
    return False

# 计算GC含量
def gc_content(seq):
    """计算GC含量"""
    return (seq.count('C') + seq.count('G')) / len(seq) * 100

# 判断互补性
def is_orthogonal(seq1, seq2):
    """判断两条引物是否正交，可以通过减少完全互补性来确定"""
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    mismatches = sum(1 for a, b in zip(seq1, seq2) if complement[a] != b)
    # 如果错配碱基数高于阈值，则认为正交
    return mismatches >= len(seq1) * 0.7

# 为引物生成正交序列
def generate_orthogonal_primer(primer):
    """生成与给定引物正交的序列"""
    orthogonal_primer = ''.join(random.choice(bases) for _ in range(len(primer)))
    # 检查生成的序列是否正交，不正交则重新生成
    while not is_orthogonal(primer, orthogonal_primer):
        orthogonal_primer = ''.join(random.choice(bases) for _ in range(len(primer)))
    return orthogonal_primer

# 生成满足条件的引物
primers = []
while len(primers) < 10000:
    # 随机生成20nt序列
    primer = ''.join(random.choice(bases) for _ in range(20))
    # 筛选条件
    if has_homopolymer(primer) or not (40 <= gc_content(primer) <= 60):
        continue
    # 添加符合条件的引物
    orthogonal_primer = generate_orthogonal_primer(primer)
    primers.append((primer, orthogonal_primer))

# 将筛选后的引物对写入CSV文件
with open('primers_and_orthogonal.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Primer", "Orthogonal Primer"])  # 写入表头
    for primer, orthogonal in primers:
        writer.writerow([primer, orthogonal])

print(f"共生成 {len(primers)} 对正交引物，已保存到 'primers_and_orthogonal.csv' 文件中。")
