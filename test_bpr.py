# coding: utf-8
"""
BPR 函数测试脚本
测试 BPR (Bureau of Public Roads) 阻抗函数的正确性
"""

import numpy as np
import sys

def bpr_fun(volumn, freeTime, capacity, alpha=0.15, beta=4):
    """
    BPR 阻抗函数
    travelTime = BPR_fun(volumn, freeTime, capacity, alpha=0.15, beta=4)
    
    参数:
        volumn: 交通流量 (可以是标量或 numpy 数组)
        freeTime: 自由流时间 (可以是标量或 numpy 数组)
        capacity: 道路容量 (可以是标量或 numpy 数组)
        alpha: BPR 参数，默认 0.15
        beta: BPR 参数，默认 4
    
    返回:
        travelTime: 行程时间 (与输入相同类型的 numpy 数组)
    
    公式:
        travelTime = freeTime + freeTime * alpha * (volumn / capacity) ** beta
    """
    travelTime = freeTime + freeTime * alpha * (volumn / capacity) ** beta
    return travelTime


def test_bpr_basic():
    """测试 1: 基本功能测试 - 零流量情况"""
    print("=" * 60)
    print("测试 1: 基本功能测试 - 零流量情况")
    print("=" * 60)
    
    volumn = 0
    freeTime = 10
    capacity = 100
    
    result = bpr_fun(volumn, freeTime, capacity)
    expected = 10.0  # 零流量时，行程时间应等于自由流时间
    
    print(f"输入：volumn={volumn}, freeTime={freeTime}, capacity={capacity}")
    print(f"输出：{result}")
    print(f"期望：{expected}")
    
    assert np.isclose(result, expected), f"测试失败：{result} != {expected}"
    print("✓ 测试通过\n")
    return True


def test_bpr_capacity_flow():
    """测试 2: 容量流量测试 - 流量等于容量"""
    print("=" * 60)
    print("测试 2: 容量流量测试 - 流量等于容量")
    print("=" * 60)
    
    volumn = 100
    freeTime = 10
    capacity = 100
    
    result = bpr_fun(volumn, freeTime, capacity)
    expected = freeTime + freeTime * 0.15 * (volumn / capacity) ** 4
    expected = 10 + 10 * 0.15 * 1**4  # = 11.5
    
    print(f"输入：volumn={volumn}, freeTime={freeTime}, capacity={capacity}")
    print(f"输出：{result}")
    print(f"期望：{expected}")
    
    assert np.isclose(result, expected), f"测试失败：{result} != {expected}"
    print("✓ 测试通过\n")
    return True


def test_bpr_array_input():
    """测试 3: 数组输入测试 - 批量计算"""
    print("=" * 60)
    print("测试 3: 数组输入测试 - 批量计算")
    print("=" * 60)
    
    volumn = np.array([0, 50, 100, 150, 200])
    freeTime = 10
    capacity = 100
    
    result = bpr_fun(volumn, freeTime, capacity)
    
    print(f"输入：volumn={volumn}")
    print(f"输出：{result}")
    
    # 验证每个值
    expected = []
    for v in volumn:
        t = freeTime + freeTime * 0.15 * (v / capacity) ** 4
        expected.append(t)
    expected = np.array(expected)
    
    print(f"期望：{expected}")
    
    assert np.allclose(result, expected), f"测试失败：{result} != {expected}"
    print("✓ 测试通过\n")
    return True


def test_bpr_custom_parameters():
    """测试 4: 自定义参数测试"""
    print("=" * 60)
    print("测试 4: 自定义参数测试")
    print("=" * 60)
    
    volumn = 100
    freeTime = 10
    capacity = 100
    alpha = 0.2
    beta = 3
    
    result = bpr_fun(volumn, freeTime, capacity, alpha, beta)
    expected = freeTime + freeTime * alpha * (volumn / capacity) ** beta
    expected = 10 + 10 * 0.2 * 1**3  # = 12.0
    
    print(f"输入：volumn={volumn}, freeTime={freeTime}, capacity={capacity}")
    print(f"参数：alpha={alpha}, beta={beta}")
    print(f"输出：{result}")
    print(f"期望：{expected}")
    
    assert np.isclose(result, expected), f"测试失败：{result} != {expected}"
    print("✓ 测试通过\n")
    return True


def test_bpr_over_capacity():
    """测试 5: 超容量测试 - 流量超过容量"""
    print("=" * 60)
    print("测试 5: 超容量测试 - 流量超过容量")
    print("=" * 60)
    
    volumn = 200  # 容量的 2 倍
    freeTime = 10
    capacity = 100
    
    result = bpr_fun(volumn, freeTime, capacity)
    expected = 10 + 10 * 0.15 * (200/100)**4
    expected = 10 + 10 * 0.15 * 16  # = 10 + 24 = 34
    
    print(f"输入：volumn={volumn} (容量的{volumn/capacity:.1f}倍)")
    print(f"输出：{result}")
    print(f"期望：{expected}")
    
    assert np.isclose(result, expected), f"测试失败：{result} != {expected}"
    print("✓ 测试通过\n")
    return True


def test_bpr_monotonicity():
    """测试 6: 单调性测试 - 流量增加，时间增加"""
    print("=" * 60)
    print("测试 6: 单调性测试 - 流量增加，时间增加")
    print("=" * 60)
    
    freeTime = 10
    capacity = 100
    volumes = [0, 25, 50, 75, 100, 125, 150]
    
    results = [bpr_fun(v, freeTime, capacity) for v in volumes]
    
    print(f"流量：{volumes}")
    print(f"时间：{results}")
    
    # 验证单调递增
    for i in range(len(results)-1):
        assert results[i] < results[i+1], f"单调性测试失败：{results[i]} >= {results[i+1]}"
    
    print("✓ 测试通过 - 行程时间随流量单调递增\n")
    return True


def main():
    """执行所有测试"""
    print("\n" + "=" * 60)
    print("BPR 函数测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        ("基本功能测试", test_bpr_basic),
        ("容量流量测试", test_bpr_capacity_flow),
        ("数组输入测试", test_bpr_array_input),
        ("自定义参数测试", test_bpr_custom_parameters),
        ("超容量测试", test_bpr_over_capacity),
        ("单调性测试", test_bpr_monotonicity),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"✗ {name} 失败：{e}\n")
            failed += 1
        except Exception as e:
            print(f"✗ {name} 出错：{e}\n")
            failed += 1
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试数：{passed + failed}")
    print(f"通过：{passed}")
    print(f"失败：{failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！BPR 函数工作正常。")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查代码。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
