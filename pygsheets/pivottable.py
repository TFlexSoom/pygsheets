# -*- coding: utf-8 -*-.

"""
pygsheets.pivottable
~~~~~~~~~~~~~~

This module represents a pivottable within the worksheet.

"""
from enum import Enum
from typing import List, Dict, Any

from pygsheets.address import GridRange
from pygsheets.spreadsheet import Spreadsheet
from pygsheets.utils import format_addr
from pygsheets.custom_types import SortOrder, DateTimeRuleType
from pygsheets.exceptions import InvalidArgumentValue 

class PivotGroupValueMetadata(object):
    def __init__(self, value, collapsed: bool = None):
        self._value = value
        self._collapsed = collapsed
    
    def get_json(self):
        return {
            "value": self._value,
            "collapsed": self._collapsed
        }

class PivotGroupSortValueBucket(object):
    def __init__(self, values_index: int, buckets: list):
        self._values_index = values_index
        self._buckets = buckets
    
    def get_json(self):
        return {
            "valuesIndex": self._values_index,
            "buckets": self._buckets
        }

class PivotGroupRule(object):
    pass

class ManualRule(PivotGroupRule):
    def __init__(self, groups: Dict[str, Any]):
        self._groups = groups
    
    def get_json(self):
        return {
            "groups": self._groups,
        }

class HistogramRule(PivotGroupRule):
    def __init__(self, interval: float, start: float, end: float):
        self._interval = interval
        self._start = start
        self._end = end
    
    def get_json(self):
        return {
            "interval": self._interval,
            "start": self._start,
            "end": self._end,
        }

class DateTimeRule(PivotGroupRule):
    def __init__(self, time_rule_type: DateTimeRuleType):
        self._type = time_rule_type
    
    def get_json(self):
        return {
            "type": self._type
        }
    

class PivotGroupLimit:
    # (countLimit: int, applyOrder: int)
    def __init__(self, count_limit: int, apply_order: int):
        self._count_limit = count_limit
        self._apply_order = apply_order
    
    def get_json(self):
        return {
            "countLimit": self._count_limit,
            "applyOrder": self._apply_order,
        }

class PivotFilterCriteria:
    def __init__(self, visible_values: List[str], condition: BooleanCondition, visible_by_default: bool):
        self._visible_values = visible_values
        self._condition = condition
        self._visible_by_default = visible_by_default

    def get_json(self):
        return {
            "visibleValues": self._visible_values,
            "condition": self._condition,
            "visibleByDefault": self._visible_by_default,
        }

class PivotFilterSpec:
    def __init__(self, filter_criteria: PivotFilterCriteria, column_offset_index: int = None, data_source_column_reference: tuple = None):
        if (column_offset_index == None) == (data_source_column_reference == None):
            raise InvalidArgumentValue("Union Field Source Cannot have both values!")
        
        self._filter_criteria = filter_criteria
        self._column_offset_index = column_offset_index
        self._data_source_column_reference = data_source_column_reference
    
    def get_json(self):
        res = {
            "filterCriteria": self._filter_criteria
        }

        if self._column_offset_index:
            res["columnOffsetIndex"] = self._column_offset_index
        
        if self._data_source_column_reference:
            res["dataSourceColumnReference"] = self._data_source_column_reference
        
        return res

class PivotValueSummarizeFunction(Enum):
    SUM = "SUM"
    COUNTA = "COUNTA"
    COUNT = "COUNT"
    COUNTUNIQUE = "COUNTUNIQUE"
    AVERAGE = "AVERAGE"
    MAX = "MAX"
    MIN = "MIN"
    MEDIAN = "MEDIAN"
    PRODUCT = "PRODUCT"
    STDDEV = "STDDEV"
    STDDEVP = "STDDEVP"
    VAR = "VAR"
    VARP = "VARP"
    CUSTOM = "CUSTOM"

class PivotValueCalculatedDisplayType(Enum):
    PERCENT_OF_ROW_TOTAL = "PERCENT_OF_ROW_TOTAL"
    PERCENT_OF_COLUMN_TOTAL = "PERCENT_OF_COLUMN_TOTAL"
    PERCENT_OF_GRAND_TOTAL = "PERCENT_OF_GRAND_TOTAL"

class PivotValueLayout(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"

class PivotValue:
    # (
    ##  summarizeFunction: PivotValueSummarizeFunction, 
    ##  name: string,  
    ##  calculatedDisplayType: PivotValueCalculatedDisplayType, 
    ##  sourceColumnOffset: int,
    ##  formula: string,
    ##  dataSourceColumnReference: DataSourceColumnReference,
    # )
    def __init__(
            self, 
            summarize_function: PivotValueSummarizeFunction,
            name: str,
            calculated_display_type: PivotValueCalculatedDisplayType,
            source_column_offset: int,
            formula: str,
            data_source_column_reference: tuple 
        ):
        self._summarize_function = summarize_function
        self._name = name
        self._calculated_display_type = calculated_display_type
        self._source_column_offset = source_column_offset
        self._formula = formula
        self._data_source_column_reference = data_source_column_reference
    
    def get_json(self):
        return {
            "summarizeFunction": self._summarize_function,
            "name": self._name,
            "calculatedDisplayType": self._calculated_display_type,
            "sourcecolumnOffset": self._source_column_offset,
            "formula": self._formula,
            "dataSourceColumnReference": self._data_source_column_reference
        }

class PivotGroup(object):
    """
    PivotTables exist within a range of cells exhibiting mathematical groupings of the data within
    the cells. This could be an aggregation of specific rows. This could be a count of specific data
    within the cells. The PivotTable acts as a window or statistical display of the given data.

    :param source:          reference to the cell data for the grouping
    :param show_totals:     True if the pivot table should include totals for the row/column
    :param repeat_headings: True if the pivot table should repeat prefix groupings for row/column
    :param sort_order:      Value of SortOrder enum
    :param value_bucket:    Sorting Definition otherwise None to use default Alphabetical Sort
    :param label:           String label
    :param group_rule:      Defines how the aggregation is calculated
    :param group_limit:     TODO
    :param metadata:        list of tuples detailing values in the pivot grouping. Check 
        `<https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/pivot-tables#pivotgroupvaluemetadata>`__.
    :param json_obj:        Represents a json structure of the chart as given in `api 
        <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#BasicChartSpec>`__.

    """
    def __init__(
        self,
        label: str,
        source: tuple,
        group_rule: PivotGroupRule,
        show_totals: bool = True,
        repeat_headings: bool = True,
        sort_order: SortOrder = SortOrder.ASCENDING,
        value_bucket: PivotGroupSortValueBucket = None,
        group_limit: PivotGroupLimit = None,
        metadata: List[PivotGroupValueMetadata] = [],
        json_obj = None,
    ):
        self._label = label
        self._group_rule = group_rule
        self._source = source
        if source:
            self._source = (format_addr(source[0], 'tuple'), format_addr(source[1], 'tuple'))

        self._show_totals = show_totals
        self._repeat_headings = repeat_headings
        self._sort_order = sort_order
        self._value_bucket = value_bucket
        self._group_limit = group_limit
        self._metadata = metadata
        if json_obj is None:
            self._create()
        else:
            self.set_json(json_obj)
    
    def _create(self):
        pass

    def set_json(self, json_obj: dict):
        pass

    def to_json(self) -> dict:
        return {}


class PivotTable(object):
    """
    PivotTables exist within a range of cells exhibiting mathematical groupings of the data within
    the cells. This could be an aggregation of specific rows. This could be a count of specific data
    within the cells. The PivotTable acts as a window or statistical display of the given data.

    :param worksheet:       Worksheet object in which the chart resides
    :param rows:            Row Groupings For the Pivot Table
    :param columns:         Column Groupings For the Pivot Table
    :param values:          Value Calculation From Source on how the values should be calculated
    :param source:          Cell range of the desired pivot table data in the form of tuple of tuples
    :param layout:          Horizontal/Vertical Layout of Pivot Table Data
    :param filter_specs:    Filtering Settings for unwanted data to be included in table
    :param anchor_cell:     Position of the left corner of the chart in the form of cell address or cell object
    :param json_obj:        Represents a json structure of the chart as given in `api <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/pivot-tables>`__.

    >>> pivot = PivotTable(source=("A1", "B2"), worksheet=wks)
    TODO
    >>> pivot.source = ("A1", "B2") # Change the values of the pivot table
    TODO


    """
    def __init__(
        self,
        worksheet : Spreadsheet | None = None,
        source: GridRange | None = None,
        data_source_id: str = None,
        rows: List[PivotGroup] = [],
        columns: List[PivotGroup] = [],
        values:  List[PivotValue] = [],
        layout: PivotValueLayout = PivotValueLayout.HORIZONTAL,
        filter_specs: List[PivotFilterSpec] = [],
        json_obj = {},
    ):
        if (source == None) == (data_source_id == None):
            raise InvalidArgumentValue("Source and Datasource cannot be none!")
        
        self._worksheet = worksheet
        self._source = source
        self._data_source_id = data_source_id
        self._rows = rows
        self._columns = columns
        self._values = values
        self._layout = layout
        self._filter_specs = filter_specs
        self.set_json(json_obj)
    

    @classmethod
    def from_json(worksheet: Spreadsheet, json_obj: dict):
        source = json_obj.get("source", None)
        grange = None
        if source:
            grange = GridRange(worksheet=worksheet, propertiesjson=source)
        
        return PivotTable(
            worksheet=worksheet, 
            source=grange, 
            data_source_id=json_obj.get("dataSourceId", None),
            json_obj=json_obj
        )

    @property
    def source(self) -> GridRange:
        return self._source

    @source.setter
    def source(self, value: GridRange | None):
        self._source = value
    
    @property
    def data_source_id(self) -> str:
        return self._data_source_id

    @data_source_id.setter
    def data_source_id(self, value: str):
        self._data_source_id = value

    @property
    def rows(self) -> List[PivotGroup]:
        return self._rows

    @rows.setter
    def rows(self, value: List[PivotGroup]):
        self._rows = value
    
    @property
    def columns(self) -> List[PivotGroup]:
        return self._columns
    
    @columns.setter
    def columns(self, value: List[PivotGroup]):
        self._columns = value
    
    @property
    def values(self) -> List[PivotValue]:
        return self._values
    
    @values.setter
    def values(self, value: List[PivotValue]):
        self._values = value
    
    @property
    def layout(self) -> PivotValueLayout:
        return self._layout
    
    @layout.setter
    def layout(self, value: PivotValueLayout):
        self._layout = value
    
    @property
    def filter_specs(self):
        return self.filter_specs

    @filter_specs.setter
    def filter_specs(self, value: List[PivotFilterSpec]):
        self._filter_specs = value
    
    @property
    def json_obj(self):
        return self._json_obj
    
    @json_obj.setter
    def json_obj(self, value: dict):
        self._json_obj = value

    def set_json(self, json_obj: dict):
        self._json_obj = {
            "rows": json_obj.get("rows", lambda : list(map(PivotGroup.to_json, self._rows))),
            "columns": json_obj.get("columns", lambda : list(map(PivotGroup.to_json, self._columns))),
            "filterSpecs": json_obj.get("filterSpecs", lambda: list(map(PivotFilterSpec.get_json, self._filter_specs))),
            "values": json_obj.get("values", lambda: list(map(PivotValue.get_json, self._values))),
            "valueLayout": json_obj.get("valueLayout", self._layout.value)
        }

        if json_obj["source"] or self._source:
            self._json_obj["source"] = json_obj.get("source", self._source.to_json())
        
        if json_obj["dataSourceId"] or self._data_source_id:
            self._json_obj["dataSourceId"] = json_obj.get("dataSourceId", self._data_source_id)
        
        if (self._json_obj["source"] != None) and (self._json_obj["dataSourceId"] != None):
            raise InvalidArgumentValue("source and dataSourceId are both defined")

