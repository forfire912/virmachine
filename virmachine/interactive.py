#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式界面 - 虚拟样机系统
Interactive Interface - Virtual Prototyping Machine System

提供菜单驱动的交互式用户界面
Provides a menu-driven interactive user interface
"""

import os
import sys
from typing import Optional
from virmachine import VirtualPrototype, Component, Simulator, set_language, get_text


class VirMachineInteractive:
    """交互式虚拟样机系统 / Interactive Virtual Prototyping Machine System"""
    
    def __init__(self):
        """初始化交互式系统 / Initialize interactive system"""
        self.prototype: Optional[VirtualPrototype] = None
        self.simulator = Simulator()
        self.language = 'zh_CN'
        set_language(self.language)
    
    def _convert_to_number(self, value: str):
        """
        尝试将字符串转换为数字
        Try to convert string to number
        
        Returns the converted number or original string
        """
        if not value:
            return value
        
        # Try integer first
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string if conversion fails
        return value
        
    def clear_screen(self):
        """清屏 / Clear screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def print_header(self):
        """打印标题 / Print header"""
        print("\n" + "=" * 70)
        print("║" + " " * 68 + "║")
        if self.language == 'zh_CN':
            print("║" + "国产化虚拟样机系统 - 交互式界面".center(76) + "║")
            print("║" + "Virtual Prototyping Machine - Interactive Interface".center(68) + "║")
        else:
            print("║" + "Virtual Prototyping Machine - Interactive Interface".center(68) + "║")
            print("║" + "国产化虚拟样机系统 - 交互式界面".center(76) + "║")
        print("║" + " " * 68 + "║")
        print("=" * 70)
        
    def print_menu(self):
        """打印主菜单 / Print main menu"""
        if self.language == 'zh_CN':
            print("\n【主菜单】")
            print("  1. 创建新的虚拟样机")
            print("  2. 添加组件")
            print("  3. 查看虚拟样机信息")
            print("  4. 运行仿真测试")
            print("  5. 保存虚拟样机")
            print("  6. 加载虚拟样机")
            print("  7. 切换语言 (当前: 中文)")
            print("  0. 退出系统")
        else:
            print("\n【Main Menu】")
            print("  1. Create New Virtual Prototype")
            print("  2. Add Component")
            print("  3. View Prototype Information")
            print("  4. Run Simulation Tests")
            print("  5. Save Prototype")
            print("  6. Load Prototype")
            print("  7. Switch Language (Current: English)")
            print("  0. Exit System")
        print("-" * 70)
        
    def get_input(self, prompt: str, default: str = "") -> str:
        """获取用户输入 / Get user input"""
        try:
            value = input(f"{prompt}: ").strip()
            return value if value else default
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def create_prototype(self):
        """创建虚拟样机 / Create virtual prototype"""
        self.clear_screen()
        self.print_header()
        
        if self.language == 'zh_CN':
            print("\n【创建新的虚拟样机】")
            name = self.get_input("请输入样机名称")
            if not name:
                print("❌ 名称不能为空！")
                input("\n按回车键继续...")
                return
            description = self.get_input("请输入样机描述 (可选)", "")
            
            self.prototype = VirtualPrototype(name, description)
            print(f"\n✓ 成功创建虚拟样机: {name}")
        else:
            print("\n【Create New Virtual Prototype】")
            name = self.get_input("Enter prototype name")
            if not name:
                print("❌ Name cannot be empty!")
                input("\nPress Enter to continue...")
                return
            description = self.get_input("Enter prototype description (optional)", "")
            
            self.prototype = VirtualPrototype(name, description)
            print(f"\n✓ Successfully created virtual prototype: {name}")
        
        input("\n按回车键继续... / Press Enter to continue...")
    
    def add_component(self):
        """添加组件 / Add component"""
        if not self.prototype:
            if self.language == 'zh_CN':
                print("\n❌ 请先创建虚拟样机！")
            else:
                print("\n❌ Please create a virtual prototype first!")
            input("\n按回车键继续... / Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        
        if self.language == 'zh_CN':
            print("\n【添加组件】")
            name = self.get_input("组件名称")
            if not name:
                print("❌ 名称不能为空！")
                input("\n按回车键继续...")
                return
            
            comp_type = self.get_input("组件类型 (如: motor, sensor, controller)")
            if not comp_type:
                print("❌ 类型不能为空！")
                input("\n按回车键继续...")
                return
            
            print("\n添加组件属性 (输入空行结束):")
            properties = {}
            while True:
                key = self.get_input("  属性名 (空行结束)")
                if not key:
                    break
                value = self.get_input(f"  属性值 [{key}]")
                properties[key] = self._convert_to_number(value)
            
            component = Component(name, comp_type, properties)
            self.prototype.add_component(component)
            print(f"\n✓ 成功添加组件: {name} ({comp_type})")
        else:
            print("\n【Add Component】")
            name = self.get_input("Component name")
            if not name:
                print("❌ Name cannot be empty!")
                input("\nPress Enter to continue...")
                return
            
            comp_type = self.get_input("Component type (e.g., motor, sensor, controller)")
            if not comp_type:
                print("❌ Type cannot be empty!")
                input("\nPress Enter to continue...")
                return
            
            print("\nAdd component properties (empty line to finish):")
            properties = {}
            while True:
                key = self.get_input("  Property name (empty to finish)")
                if not key:
                    break
                value = self.get_input(f"  Property value [{key}]")
                properties[key] = self._convert_to_number(value)
            
            component = Component(name, comp_type, properties)
            self.prototype.add_component(component)
            print(f"\n✓ Successfully added component: {name} ({comp_type})")
        
        input("\n按回车键继续... / Press Enter to continue...")
    
    def view_prototype(self):
        """查看虚拟样机信息 / View prototype information"""
        if not self.prototype:
            if self.language == 'zh_CN':
                print("\n❌ 请先创建虚拟样机！")
            else:
                print("\n❌ Please create a virtual prototype first!")
            input("\n按回车键继续... / Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        
        if self.language == 'zh_CN':
            print("\n【虚拟样机信息】")
            print(f"\n名称: {self.prototype.name}")
            print(f"描述: {self.prototype.description or '无'}")
            print(f"版本: {self.prototype.version}")
            print(f"组件数量: {len(self.prototype.components)}")
            
            if self.prototype.components:
                print("\n组件列表:")
                for i, comp in enumerate(self.prototype.components, 1):
                    print(f"  {i}. {comp.name} ({comp.component_type})")
                    if comp.properties:
                        for key, value in comp.properties.items():
                            print(f"     - {key}: {value}")
            
            if self.prototype.metadata:
                print("\n元数据:")
                for key, value in self.prototype.metadata.items():
                    print(f"  • {key}: {value}")
        else:
            print("\n【Virtual Prototype Information】")
            print(f"\nName: {self.prototype.name}")
            print(f"Description: {self.prototype.description or 'None'}")
            print(f"Version: {self.prototype.version}")
            print(f"Component Count: {len(self.prototype.components)}")
            
            if self.prototype.components:
                print("\nComponent List:")
                for i, comp in enumerate(self.prototype.components, 1):
                    print(f"  {i}. {comp.name} ({comp.component_type})")
                    if comp.properties:
                        for key, value in comp.properties.items():
                            print(f"     - {key}: {value}")
            
            if self.prototype.metadata:
                print("\nMetadata:")
                for key, value in self.prototype.metadata.items():
                    print(f"  • {key}: {value}")
        
        input("\n按回车键继续... / Press Enter to continue...")
    
    def run_simulation(self):
        """运行仿真测试 / Run simulation tests"""
        if not self.prototype:
            if self.language == 'zh_CN':
                print("\n❌ 请先创建虚拟样机！")
            else:
                print("\n❌ Please create a virtual prototype first!")
            input("\n按回车键继续... / Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        
        if self.language == 'zh_CN':
            print("\n【仿真测试】")
            print("  1. 基础仿真")
            print("  2. 压力测试")
            print("  3. 性能测试")
            print("  0. 返回主菜单")
            choice = self.get_input("\n请选择测试类型")
            
            if choice == '1':
                print("\n运行基础仿真...")
                result = self.simulator.run_simulation(self.prototype, "basic")
                print(f"\n结果: {result}")
                print(f"状态: {'✓ 通过' if result.success else '✗ 失败'}")
                print(f"测试组件数: {result.data.get('component_count', 0)}")
            elif choice == '2':
                stress_level = self.get_input("输入压力级别 (0.0-10.0)", "5.0")
                try:
                    stress_level = float(stress_level)
                    print(f"\n运行压力测试 (级别: {stress_level})...")
                    result = self.simulator.run_stress_test(self.prototype, stress_level)
                    print(f"\n结果: {result}")
                    print(f"状态: {'✓ 通过' if result.success else '✗ 失败'}")
                except ValueError:
                    print("❌ 无效的压力级别！")
            elif choice == '3':
                print("\n运行性能测试...")
                result = self.simulator.run_performance_test(self.prototype)
                print(f"\n结果: {result}")
                print(f"状态: {'✓ 通过' if result.success else '✗ 失败'}")
            elif choice == '0':
                return
        else:
            print("\n【Simulation Tests】")
            print("  1. Basic Simulation")
            print("  2. Stress Test")
            print("  3. Performance Test")
            print("  0. Return to Main Menu")
            choice = self.get_input("\nSelect test type")
            
            if choice == '1':
                print("\nRunning basic simulation...")
                result = self.simulator.run_simulation(self.prototype, "basic")
                print(f"\nResult: {result}")
                print(f"Status: {'✓ Passed' if result.success else '✗ Failed'}")
                print(f"Components tested: {result.data.get('component_count', 0)}")
            elif choice == '2':
                stress_level = self.get_input("Enter stress level (0.0-10.0)", "5.0")
                try:
                    stress_level = float(stress_level)
                    print(f"\nRunning stress test (level: {stress_level})...")
                    result = self.simulator.run_stress_test(self.prototype, stress_level)
                    print(f"\nResult: {result}")
                    print(f"Status: {'✓ Passed' if result.success else '✗ Failed'}")
                except ValueError:
                    print("❌ Invalid stress level!")
            elif choice == '3':
                print("\nRunning performance test...")
                result = self.simulator.run_performance_test(self.prototype)
                print(f"\nResult: {result}")
                print(f"Status: {'✓ Passed' if result.success else '✗ Failed'}")
            elif choice == '0':
                return
        
        input("\n按回车键继续... / Press Enter to continue...")
    
    def save_prototype(self):
        """保存虚拟样机 / Save prototype"""
        if not self.prototype:
            if self.language == 'zh_CN':
                print("\n❌ 请先创建虚拟样机！")
            else:
                print("\n❌ Please create a virtual prototype first!")
            input("\n按回车键继续... / Press Enter to continue...")
            return
        
        if self.language == 'zh_CN':
            filename = self.get_input("\n输入文件名 (不含扩展名)", self.prototype.name)
        else:
            filename = self.get_input("\nEnter filename (without extension)", self.prototype.name)
        
        if not filename:
            filename = self.prototype.name
        
        filepath = f"{filename}.json"
        
        try:
            self.prototype.to_json(filepath)
            if self.language == 'zh_CN':
                print(f"\n✓ 成功保存到: {filepath}")
            else:
                print(f"\n✓ Successfully saved to: {filepath}")
        except Exception as e:
            if self.language == 'zh_CN':
                print(f"\n❌ 保存失败: {e}")
            else:
                print(f"\n❌ Save failed: {e}")
        
        input("\n按回车键继续... / Press Enter to continue...")
    
    def load_prototype(self):
        """加载虚拟样机 / Load prototype"""
        if self.language == 'zh_CN':
            filename = self.get_input("\n输入文件名")
        else:
            filename = self.get_input("\nEnter filename")
        
        if not filename:
            if self.language == 'zh_CN':
                print("❌ 文件名不能为空！")
            else:
                print("❌ Filename cannot be empty!")
            input("\n按回车键继续... / Press Enter to continue...")
            return
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            self.prototype = VirtualPrototype.from_json(filename)
            if self.language == 'zh_CN':
                print(f"\n✓ 成功加载: {self.prototype.name}")
                print(f"   组件数量: {len(self.prototype.components)}")
            else:
                print(f"\n✓ Successfully loaded: {self.prototype.name}")
                print(f"   Components: {len(self.prototype.components)}")
        except FileNotFoundError:
            if self.language == 'zh_CN':
                print(f"\n❌ 文件不存在: {filename}")
            else:
                print(f"\n❌ File not found: {filename}")
        except Exception as e:
            if self.language == 'zh_CN':
                print(f"\n❌ 加载失败: {e}")
            else:
                print(f"\n❌ Load failed: {e}")
        
        input("\n按回车键继续... / Press Enter to continue...")
    
    def switch_language(self):
        """切换语言 / Switch language"""
        if self.language == 'zh_CN':
            self.language = 'en_US'
            print("\n✓ Language switched to English")
        else:
            self.language = 'zh_CN'
            print("\n✓ 已切换为中文")
        
        set_language(self.language)
        input("\n按回车键继续... / Press Enter to continue...")
    
    def run(self):
        """运行交互式界面 / Run interactive interface"""
        while True:
            self.clear_screen()
            self.print_header()
            
            if self.prototype:
                if self.language == 'zh_CN':
                    print(f"\n当前样机: {self.prototype.name} ({len(self.prototype.components)} 个组件)")
                else:
                    print(f"\nCurrent Prototype: {self.prototype.name} ({len(self.prototype.components)} components)")
            
            self.print_menu()
            
            if self.language == 'zh_CN':
                choice = self.get_input("请选择操作")
            else:
                choice = self.get_input("Select operation")
            
            if choice == '1':
                self.create_prototype()
            elif choice == '2':
                self.add_component()
            elif choice == '3':
                self.view_prototype()
            elif choice == '4':
                self.run_simulation()
            elif choice == '5':
                self.save_prototype()
            elif choice == '6':
                self.load_prototype()
            elif choice == '7':
                self.switch_language()
            elif choice == '0':
                if self.language == 'zh_CN':
                    print("\n感谢使用国产化虚拟样机系统！再见！")
                else:
                    print("\nThank you for using VirMachine! Goodbye!")
                break
            else:
                if self.language == 'zh_CN':
                    print("\n❌ 无效的选项，请重新选择！")
                else:
                    print("\n❌ Invalid option, please try again!")
                input("\n按回车键继续... / Press Enter to continue...")


def main():
    """主函数 / Main function"""
    try:
        interface = VirMachineInteractive()
        interface.run()
    except KeyboardInterrupt:
        print("\n\n程序已终止 / Program terminated")
    except Exception as e:
        print(f"\n错误 / Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
