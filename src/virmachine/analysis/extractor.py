#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据提取器 (Data Extractor)

实现多种格式的试验数据提取并转换，包括 XML、JSON、CSV 等文件格式
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from enum import Enum
import json
import csv
import io


class DataFormat(Enum):
    """数据格式"""
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    YAML = "yaml"


class DataExtractor(ABC):
    """数据提取器基类"""
    
    @abstractmethod
    def extract(self, data: Any) -> str:
        """提取数据并转换为目标格式"""
        pass
    
    @abstractmethod
    def parse(self, content: str) -> Any:
        """解析目标格式的数据"""
        pass


class JSONExtractor(DataExtractor):
    """JSON格式提取器"""
    
    def __init__(self, pretty: bool = True, indent: int = 2):
        self.pretty = pretty
        self.indent = indent
    
    def extract(self, data: Any) -> str:
        """提取为JSON格式"""
        if self.pretty:
            return json.dumps(data, indent=self.indent, ensure_ascii=False, default=str)
        return json.dumps(data, ensure_ascii=False, default=str)
    
    def parse(self, content: str) -> Any:
        """解析JSON数据"""
        return json.loads(content)


class XMLExtractor(DataExtractor):
    """XML格式提取器"""
    
    def __init__(self, root_tag: str = "data", indent: str = "  "):
        self.root_tag = root_tag
        self.indent = indent
    
    def extract(self, data: Any) -> str:
        """提取为XML格式"""
        xml_content = [f'<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append(f'<{self.root_tag}>')
        xml_content.extend(self._convert_to_xml(data, 1))
        xml_content.append(f'</{self.root_tag}>')
        return '\n'.join(xml_content)
    
    def _convert_to_xml(self, data: Any, level: int = 0) -> List[str]:
        """递归转换为XML"""
        indent = self.indent * level
        lines = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f'{indent}<{key}>')
                    lines.extend(self._convert_to_xml(value, level + 1))
                    lines.append(f'{indent}</{key}>')
                else:
                    lines.append(f'{indent}<{key}>{self._escape_xml(str(value))}</{key}>')
        elif isinstance(data, list):
            for item in data:
                lines.append(f'{indent}<item>')
                lines.extend(self._convert_to_xml(item, level + 1))
                lines.append(f'{indent}</item>')
        else:
            lines.append(f'{indent}{self._escape_xml(str(data))}')
        
        return lines
    
    def _escape_xml(self, text: str) -> str:
        """转义XML特殊字符"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))
    
    def parse(self, content: str) -> Any:
        """解析XML数据"""
        # 简化实现，实际应使用xml.etree.ElementTree
        import xml.etree.ElementTree as ET
        root = ET.fromstring(content)
        return self._xml_to_dict(root)
    
    def _xml_to_dict(self, element) -> Any:
        """XML转字典"""
        result = {}
        for child in element:
            if len(child) > 0:
                result[child.tag] = self._xml_to_dict(child)
            else:
                result[child.tag] = child.text
        return result if result else element.text


class CSVExtractor(DataExtractor):
    """CSV格式提取器"""
    
    def __init__(self, delimiter: str = ',', with_header: bool = True):
        self.delimiter = delimiter
        self.with_header = with_header
    
    def extract(self, data: Any) -> str:
        """提取为CSV格式"""
        if not isinstance(data, list):
            data = [data]
        
        if not data:
            return ""
        
        output = io.StringIO()
        
        # 获取字段名
        if isinstance(data[0], dict):
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=self.delimiter)
            
            if self.with_header:
                writer.writeheader()
            
            for row in data:
                if isinstance(row, dict):
                    writer.writerow(row)
        else:
            writer = csv.writer(output, delimiter=self.delimiter)
            for row in data:
                if isinstance(row, (list, tuple)):
                    writer.writerow(row)
                else:
                    writer.writerow([row])
        
        return output.getvalue()
    
    def parse(self, content: str) -> List[Dict[str, Any]]:
        """解析CSV数据"""
        input_stream = io.StringIO(content)
        reader = csv.DictReader(input_stream, delimiter=self.delimiter)
        return list(reader)


class DataExportService:
    """数据导出服务"""
    
    def __init__(self):
        self.extractors: Dict[DataFormat, DataExtractor] = {
            DataFormat.JSON: JSONExtractor(),
            DataFormat.XML: XMLExtractor(),
            DataFormat.CSV: CSVExtractor(),
        }
    
    def register_extractor(self, format_type: DataFormat, extractor: DataExtractor) -> None:
        """注册提取器"""
        self.extractors[format_type] = extractor
    
    def export(self, data: Any, format_type: DataFormat) -> str:
        """导出数据"""
        if format_type not in self.extractors:
            raise ValueError(f"Unsupported format: {format_type}")
        
        return self.extractors[format_type].extract(data)
    
    def import_data(self, content: str, format_type: DataFormat) -> Any:
        """导入数据"""
        if format_type not in self.extractors:
            raise ValueError(f"Unsupported format: {format_type}")
        
        return self.extractors[format_type].parse(content)
    
    def export_to_file(self, data: Any, filepath: str, format_type: DataFormat) -> bool:
        """导出到文件"""
        try:
            content = self.export(data, format_type)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Export to file failed: {e}")
            return False
    
    def import_from_file(self, filepath: str, format_type: DataFormat) -> Any:
        """从文件导入"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.import_data(content, format_type)
        except Exception as e:
            print(f"Import from file failed: {e}")
            return None


__all__ = [
    "DataFormat",
    "DataExtractor",
    "JSONExtractor",
    "XMLExtractor",
    "CSVExtractor",
    "DataExportService",
]
