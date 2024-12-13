import pytest

@pytest.fixture
def color_matcher():
    """创建一个不初始化GUI的颜色匹配器"""
    class ColorMatcher:
        def color_matches(self, color1, color2, tolerance):
            if not color1 or not color2:
                return False
            return all(abs(a - b) <= tolerance for a, b in zip(color1, color2))
    return ColorMatcher()

def test_color_matches(color_matcher):
    """测试颜色匹配功能"""
    # 测试完全相同的颜色
    assert color_matcher.color_matches((100, 100, 100), (100, 100, 100), 10) == True
    
    # 测试在容差范围内的颜色
    assert color_matcher.color_matches((100, 100, 100), (105, 105, 105), 10) == True
    
    # 测试超出容差范围的颜色
    assert color_matcher.color_matches((100, 100, 100), (120, 120, 120), 10) == False
    
    # 测试空值处理
    assert color_matcher.color_matches(None, (100, 100, 100), 10) == False
    assert color_matcher.color_matches((100, 100, 100), None, 10) == False