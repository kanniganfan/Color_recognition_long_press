import pytest
from color_picker import ColorPicker

def test_color_matches():
    """测试颜色匹配功能"""
    picker = ColorPicker()
    
    # 测试完全相同的颜色
    assert picker.color_matches((100, 100, 100), (100, 100, 100), 10) == True
    
    # 测试在容差范围内的颜色
    assert picker.color_matches((100, 100, 100), (105, 105, 105), 10) == True
    
    # 测试超出容差范围的颜色
    assert picker.color_matches((100, 100, 100), (120, 120, 120), 10) == False
    
    # 测试空值处理
    assert picker.color_matches(None, (100, 100, 100), 10) == False
    assert picker.color_matches((100, 100, 100), None, 10) == False 